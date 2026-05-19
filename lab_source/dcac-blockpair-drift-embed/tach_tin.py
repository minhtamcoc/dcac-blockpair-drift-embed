import cv2
import numpy as np
import os

# ==================================================
# CONFIG
# ==================================================
VIDEO = "output.avi"

BLOCK = 8

REPEAT = 5

MAGIC = b"DCACPAIR"
HEADER_SIZE = len(MAGIC) + 4


# ==================================================
# BITS -> BYTES
# ==================================================
def bits_to_bytes(bits: str) -> bytes:
    data = bytearray()

    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]

        if len(byte) == 8:
            data.append(int(byte, 2))

    return bytes(data)


def majority_decode_repeated_bits(raw_bits: str, repeat: int) -> str:
    bits = ""

    for i in range(0, len(raw_bits), repeat):
        chunk = raw_bits[i:i + repeat]

        if len(chunk) < repeat:
            break

        ones = chunk.count("1")
        zeros = chunk.count("0")

        bits += "1" if ones > zeros else "0"

    return bits


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
# EXTRACT BIT SOURCES
# ==================================================
def extract_dc_blockpair(dct_a, dct_b):
    diff = dct_a[0, 0] - dct_b[0, 0]
    return "1" if diff >= 0 else "0"


def extract_ac_blockpair(dct_a, dct_b):
    diff = dct_a[2, 3] - dct_b[2, 3]
    return "1" if diff >= 0 else "0"


def extract_bit_from_block_pair(block_a, block_b):
    dct_a = cv2.dct(np.float32(block_a))
    dct_b = cv2.dct(np.float32(block_b))

    # DC ổn định hơn sau IDCT + ghi video nên dùng DC làm kênh chính.
    # AC vẫn được tính để đúng mô hình DC + AC block-pair.
    b_dc = extract_dc_blockpair(dct_a, dct_b)
    _b_ac = extract_ac_blockpair(dct_a, dct_b)

    return b_dc


# ==================================================
# BIT STREAM GENERATOR
# ==================================================
def bit_stream_from_video(cap):
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame

        h, w = gray.shape
        pairs = get_block_pair_positions(h, w)

        for pos_a, pos_b in pairs:
            y1, x1 = pos_a
            y2, x2 = pos_b

            block_a = gray[y1:y1 + BLOCK, x1:x1 + BLOCK]
            block_b = gray[y2:y2 + BLOCK, x2:x2 + BLOCK]

            bit = extract_bit_from_block_pair(block_a, block_b)

            yield bit


def read_n_raw_bits(bit_gen, n_bits):
    bits = ""

    for _ in range(n_bits):
        try:
            bits += next(bit_gen)
        except StopIteration:
            break

    return bits


def read_n_decoded_bits(bit_gen, n_decoded_bits):
    """
    Muốn đọc N bit gốc thì cần đọc N * REPEAT bit thô,
    sau đó majority decode.
    """

    raw_needed = n_decoded_bits * REPEAT
    raw_bits = read_n_raw_bits(bit_gen, raw_needed)

    if len(raw_bits) < raw_needed:
        return ""

    decoded_bits = majority_decode_repeated_bits(raw_bits, REPEAT)

    return decoded_bits


# ==================================================
# MAIN EXTRACT
# ==================================================
def main():
    if not os.path.exists(VIDEO):
        print(f"[!] Không thấy video: {VIDEO}")
        return

    cap = cv2.VideoCapture(VIDEO)

    if not cap.isOpened():
        print("[!] Không mở được video")
        return

    bit_gen = bit_stream_from_video(cap)

    # Header gốc = MAGIC + LENGTH
    header_bits_needed = HEADER_SIZE * 8

    # Vì mỗi bit được lặp REPEAT lần,
    # hàm này sẽ tự đọc header_bits_needed * REPEAT bit thô.
    header_bits = read_n_decoded_bits(bit_gen, header_bits_needed)

    if len(header_bits) < header_bits_needed:
        print("[!] Không đọc đủ header")
        cap.release()
        return

    header = bits_to_bytes(header_bits)

    magic = header[:len(MAGIC)]
    msg_len_bytes = header[len(MAGIC):len(MAGIC) + 4]

    if magic != MAGIC:
        print("[!] Magic không hợp lệ")
        print(f"[DEBUG] Magic đọc được: {magic}")
        print("[!] Video không chứa tin ẩn hoặc đã bị codec nén phá hệ số")
        cap.release()
        return

    msg_len = int.from_bytes(msg_len_bytes, "big")
    msg_bits_needed = msg_len * 8

    print(f"[*] Message length: {msg_len} bytes")

    # Đọc message, cũng decode theo REPEAT
    msg_bits = read_n_decoded_bits(bit_gen, msg_bits_needed)

    cap.release()

    if len(msg_bits) < msg_bits_needed:
        print("[!] Không đọc đủ message")
        return

    secret_data = bits_to_bytes(msg_bits)

    try:
        secret_text = secret_data.decode("utf-8")
    except UnicodeDecodeError:
        secret_text = secret_data.decode("utf-8", errors="replace")

    print("===== SECRET MESSAGE =====")
    print(secret_text)
    print("==========================")


if __name__ == "__main__":
    main()