# Giau tin video bang DC/AC block-pair drift

## Muc dich

Bai thuc hanh giup sinh vien hieu va ap dung ky thuat giau/tach tin trong video. Sinh vien se su dung `ffmpeg` de xem thong so video, chay chuong trinh Python de nhung thong diep vao video, sau do tach lai thong diep tu video da duoc tao.

Ky thuat chinh cua bai nay: dieu chinh quan he DC/AC giua hai block lan can va lap bit de tang do ben.

## Yeu cau doi voi sinh vien

Sinh vien can nam cac noi dung sau:

(1) Khai niem co ban ve giau tin trong video.

(2) Vai tro cua video lossless khi can bao toan du lieu an.

(3) Cach doc va chay code Python su dung OpenCV.

## Cau hinh bai Lab

Bai lab gom 1 container. Trong container co san 4 file:

- `input.mp4`: video dung de giau tin.
- `secret.txt`: thong diep bi mat.
- `tao_tin.py`: chuong trinh nhung tin vao video.
- `tach_tin.py`: chuong trinh tach tin tu video da nhung.

Bai lab da cai san `ffmpeg`, Python 3, OpenCV va NumPy.

## Chuan bi moi truong

Vao thu muc Labtainer student:

```bash
cd /home/student/labtainer/labtainer-student
```

Khoi tao bai lab:

```bash
labtainer dcac-blockpair-drift-embed
```

Khi duoc hoi email, sinh vien nhap ma sinh vien cua minh.

## Cac nhiem vu can thuc hien

### Task 1: Xem thong so ky thuat cua file video

Muc tieu: xac dinh dinh dang, do phan giai, fps, bitrate va thoi luong cua video.

```bash
ffmpeg -hide_banner -i input.mp4
```

### Task 2: Thuc hien giau tin

Mo file code de quan sat cac tham so:

```bash
nano tao_tin.py
```

Chay chuong trinh:

```bash
python3 tao_tin.py
```

Sau khi thanh cong, man hinh se hien `DONE EMBED` va tao file `output.avi`.

### Task 3: Kiem tra video da duoc tao

```bash
ls -lh output.avi
ffmpeg -hide_banner -i output.avi
```

### Task 4: Thuc hien tach tin

```bash
nano tach_tin.py
python3 tach_tin.py
```

Neu chuong trinh in ra link trong `secret.txt`, qua trinh giau va tach tin da thanh cong.

## Kiem tra bai lam

```bash
checkwork
```

Checkwork gom 4 muc:

- `cw1`: da xem thong so video bang ffmpeg.
- `cw2`: da chay chuong trinh nhung tin.
- `cw3`: chuong trinh nhung tin da tao `output.avi`.
- `cw4`: da tach lai thong diep bi mat.

## Ket thuc bai Lab

```bash
stoplab dcac-blockpair-drift-embed
```

## Khoi dong lai bai Lab

```bash
labtainer -r dcac-blockpair-drift-embed
```
