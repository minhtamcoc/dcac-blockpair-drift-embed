# Giau tin video bang DC/AC block-pair drift

## Muc dich

Bai thuc hanh giup sinh vien hieu cach giau tin trong video bang cach dieu chinh quan he giua hai block lan can trong tung frame. Sinh vien se su dung `ffmpeg` de xem thong so video, chay chuong trinh Python de nhung thong diep, sau do tach lai thong diep tu video da nhung.

Ky thuat chinh cua bai nay la `DC/AC block-pair drift`: moi bit duoc nhung vao quan he DC va AC cua hai block 8x8 nam canh nhau. De tang do ben, moi bit duoc lap lai nhieu lan va khi tach tin se giai ma bang majority vote.

## Yeu cau doi voi sinh vien

Sinh vien can nam cac noi dung sau:

(1) Khai niem co ban ve giau tin trong video.

(2) Cach chia anh/video frame thanh block 8x8.

(3) Vai tro cua DCT, he so DC va he so AC.

(4) Y tuong lap bit va majority vote de giam loi khi tach tin.

(5) Cach doc va chay code Python su dung OpenCV.

## Cau hinh bai lab

Bai lab gom 1 container. Trong container co cac file:

- `input.mp4`: video goc.
- `secret.txt`: thong diep bi mat.
- `tao_tin.py`: chuong trinh nhung tin bang DC/AC block-pair drift.
- `tach_tin.py`: chuong trinh tach tin tu video da nhung.

Moi truong da cai san:

- Python 3.
- OpenCV.
- NumPy.
- ffmpeg.
- nano.

## Chuan bi moi truong

Tren terminal cua may Labtainer, vao thu muc:

```bash
cd /home/student/labtainer/labtainer-student
```

Tai bai lab:

```bash
imodule https://github.com/minhtamcoc/dcac-blockpair-drift-embed/raw/main/dcac-blockpair-drift-embed.tar.gz
```

Khoi tao bai lab:

```bash
labtainer dcac-blockpair-drift-embed
```

Khi duoc hoi e-mail, sinh vien nhap ma sinh vien cua minh.

## Cac nhiem vu can thuc hien

### Task 1: Xem thong so ky thuat cua video

Muc tieu: xac dinh thong tin co ban cua file `input.mp4` nhu do phan giai, fps, codec va thoi luong.

Thuc hien lenh:

```bash
ffmpeg -hide_banner -i input.mp4
```

### Task 2: Doc va chay chuong trinh giau tin

Xem thong diep can giau:

```bash
cat secret.txt
```

Mo file `tao_tin.py`:

```bash
nano tao_tin.py
```

Trong file nay can chu y:

- `BLOCK = 8`: kich thuoc block DCT.
- `DC_MARGIN`: do lech DC giua hai block.
- `AC_MARGIN`: do lech AC giua hai block.
- `REPEAT = 5`: so lan lap lai moi bit.
- `MAGIC = b"DCACPAIR"`: dau hieu nhan dien du lieu da nhung.
- `VIDEO_OUT = "output.avi"`: video dau ra.

Chay chuong trinh giau tin:

```bash
python3 tao_tin.py
```

Khi thanh cong, chuong trinh se hien:

```text
DONE EMBED
Output: output.avi
```

### Task 3: Kiem tra video da nhung tin

Kiem tra file dau ra:

```bash
ls -lh output.avi
```

Xem thong so cua video dau ra:

```bash
ffmpeg -hide_banner -i output.avi
```

Chu y: video dau ra can giu lossless. Neu nen lai bang mp4 thong thuong, quan he DC/AC co the thay doi va tach tin that bai.

### Task 4: Tach lai thong diep bi mat

Mo file `tach_tin.py`:

```bash
nano tach_tin.py
```

Trong file tach tin, chu y:

- Video duoc doc theo tung frame.
- Moi frame duoc chia thanh cac cap block 8x8 nam canh nhau.
- Bit duoc doc tu quan he DC cua cap block.
- Moi bit da duoc lap `REPEAT` lan, sau do giai ma bang majority vote.

Chay chuong trinh tach tin:

```bash
python3 tach_tin.py
```

Neu thanh cong, chuong trinh se in ra thong diep bi mat trong `secret.txt`.

## Kiem tra bai lam

Chay lenh:

```bash
checkwork
```

Bai lab co 4 muc cham:

- `cw1`: da xem thong so video bang `ffmpeg`.
- `cw2`: da chay `python3 tao_tin.py` va chuong trinh bao `DONE EMBED`.
- `cw3`: da tao file `output.avi`.
- `cw4`: da chay `python3 tach_tin.py` va tach duoc thong diep.

## Ket thuc bai lab

```bash
stoplab dcac-blockpair-drift-embed
```

## Khoi dong lai bai lab

```bash
labtainer -r dcac-blockpair-drift-embed
```
