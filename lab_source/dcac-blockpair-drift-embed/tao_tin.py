import cv2
import numpy as np
import os

# ==================================================
# CONFIG
# ==================================================
VIDEO_IN = "input.mp4"
VIDEO_OUT = "output.avi"
SECRET_FILE = "secret.txt"

BLOCK = 8

DC_MARGIN = 120.0
AC_MARGIN = 50.0

# Lặp mỗi bit 5 lần để chống lỗi lật bit
REPEAT = 5

MAGIC = b"DCACPAIR"


# ==================================================
# BYTES -> BITS
# ==================================================
def bytes_to_bits(data: bytes) -> str:
    bits = ""

    for b in data:
        bits += format(b, "08b")

    return bits


def repeat_bits(bits: str, repeat: int) -> str:
    out = ""

    for bit in bits:
        out += bit * repeat

    return out


# ==================================================
# BLOCK PAIR UTILS
# ==================================================
def get_block_pair_positions(h, w):
    pairs = []

    for y in range(0, h - BLOCK + 1, BLOCK):
        for x in range(0, w - 2 * BLOCK + 1, 2 * BLOCK):
            pos_a = (y, x)
            pos_b = (y, x + BLOCK)
            pairs.append((pos_a, pos_b))

    return pairs


# ==================================================
# DC BLOCK-PAIR EMBED
# ==================================================
def embed_dc_blockpair(dct_a, dct_b, bit):
    dc_a = dct_a[0, 0]
    dc_b = dct_b[0, 0]

    diff = dc_a - dc_b

    if bit == "1":
        if diff < DC_MARGIN:
            delta = (DC_MARGIN - diff) / 2.0
            dct_a[0, 0] += delta
            dct_b[0, 0] -= delta

    else:
        if diff > -DC_MARGIN:
            delta = (diff + DC_MARGIN) / 2.0
            dct_a[0, 0] -= delta
            dct_b[0, 0] += delta

    return dct_a, dct_b


# ==================================================
# AC BLOCK-PAIR EMBED
# ==================================================
def embed_ac_blockpair(dct_a, dct_b, bit):
    ac_a = dct_a[2, 3]
    ac_b = dct_b[2, 3]

    diff = ac_a - ac_b

    if bit == "1":
        if diff < AC_MARGIN:
            delta = (AC_MARGIN - diff) / 2.0
            dct_a[2, 3] += delta
            dct_b[2, 3] -= delta

    else:
        if diff > -AC_MARGIN:
            delta = (diff + AC_MARGIN) / 2.0
            dct_a[2, 3] -= delta
            dct_b[2, 3] += delta

    return dct_a, dct_b


# ==================================================
# EMBED 1 BIT INTO 1 BLOCK PAIR
# ==================================================
def embed_bit_into_block_pair(block_a, block_b, bit):
    dct_a = cv2.dct(np.float32(block_a))
    dct_b = cv2.dct(np.float32(block_b))

    # DC giữa 2 block lân cận
    dct_a, dct_b = embed_dc_blockpair(dct_a, dct_b, bit)

    # AC giữa 2 block lân cận
    dct_a, dct_b = embed_ac_blockpair(dct_a, dct_b, bit)

    new_block_a = cv2.idct(dct_a)
    new_block_b = cv2.idct(dct_b)

    new_block_a = np.clip(new_block_a, 0, 255).astype(np.uint8)
    new_block_b = np.clip(new_block_b, 0, 255).astype(np.uint8)

    return new_block_a, new_block_b


# ==================================================
# MAIN EMBED
# ==================================================
def main():
    if not os.path.exists(VIDEO_IN):
        print(f"[!] Không thấy video input: {VIDEO_IN}")
        return

    if not os.path.exists(SECRET_FILE):
        print(f"[!] Không thấy file secret: {SECRET_FILE}")
        return

    with open(SECRET_FILE, "rb") as f:
        secret_data = f.read()

    # Payload format:
    # MAGIC 8 bytes + LENGTH 4 bytes + DATA
    payload = MAGIC + len(secret_data).to_bytes(4, "big") + secret_data

    raw_bits = bytes_to_bits(payload)
    payload_bits = repeat_bits(raw_bits, REPEAT)

    cap = cv2.VideoCapture(VIDEO_IN)

    if not cap.isOpened():
        print("[!] Không mở được video input")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    pairs = get_block_pair_positions(h, w)
    pairs_per_frame = len(pairs)

    capacity_bits = pairs_per_frame * total_frames

    print(f"[*] Video: {w}x{h}, frames={total_frames}, fps={fps}")
    print(f"[*] Block size: {BLOCK}x{BLOCK}")
    print(f"[*] Block pairs per frame: {pairs_per_frame}")
    print(f"[*] Capacity: {capacity_bits} bits / {capacity_bits // 8} bytes")
    print(f"[*] Payload raw: {len(raw_bits)} bits / {len(payload)} bytes")
    print(f"[*] Payload repeated: {len(payload_bits)} bits, REPEAT={REPEAT}")

    if len(payload_bits) > capacity_bits:
        print("[!] Secret quá dài, video không đủ capacity")
        cap.release()
        return

    fourcc = cv2.VideoWriter_fourcc(*"FFV1")
    out = cv2.VideoWriter(VIDEO_OUT, fourcc, fps, (w, h), False)

    if not out.isOpened():
        print("[!] Không tạo được output với codec FFV1")
        print("[!] Thử đổi VIDEO_OUT = 'output.mkv' rồi chạy lại")
        cap.release()
        return

    bit_idx = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        for pos_a, pos_b in pairs:
            if bit_idx >= len(payload_bits):
                break

            y1, x1 = pos_a
            y2, x2 = pos_b

            bit = payload_bits[bit_idx]

            block_a = gray[y1:y1 + BLOCK, x1:x1 + BLOCK]
            block_b = gray[y2:y2 + BLOCK, x2:x2 + BLOCK]

            new_block_a, new_block_b = embed_bit_into_block_pair(
                block_a,
                block_b,
                bit
            )

            gray[y1:y1 + BLOCK, x1:x1 + BLOCK] = new_block_a
            gray[y2:y2 + BLOCK, x2:x2 + BLOCK] = new_block_b

            bit_idx += 1

        out.write(gray)

        if bit_idx >= len(payload_bits):
            while True:
                ret2, frame2 = cap.read()

                if not ret2:
                    break

                gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
                out.write(gray2)

            break

    cap.release()
    out.release()

    print("[+] DONE EMBED")
    print(f"[+] Đã nhúng {bit_idx} repeated bits")
    print(f"[+] Output: {VIDEO_OUT}")


if __name__ == "__main__":
    main()