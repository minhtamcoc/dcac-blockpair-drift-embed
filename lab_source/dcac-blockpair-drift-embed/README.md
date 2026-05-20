# Huong dan nhanh

Bai lab nay giau thong diep trong `secret.txt` vao video `input.mp4` bang ky thuat DC/AC block-pair drift va tao video dau ra `output.avi`.

Thuc hien cac lenh sau:

```bash
ffmpeg -hide_banner -i input.mp4
cat secret.txt
nano tao_tin.py
python3 tao_tin.py
ls -lh output.avi
ffmpeg -hide_banner -i output.avi
nano tach_tin.py
python3 tach_tin.py
```

Sau khi lam xong, chay `checkwork` tren terminal Labtainer de kiem tra `cw1` den `cw4`.
