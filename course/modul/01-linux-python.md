# Modul 1 — Linux & Python Secukupnya untuk Robotika

> **Estimasi:** 3 jam · **Hasil akhir:** skrip Python analisis log sensor di repo GitHub-mu sendiri

Insinyur robotika menghabiskan banyak waktu di terminal dan menulis Python.
Modul ini **bukan** kursus Linux atau Python lengkap — hanya bagian yang benar-benar
akan kamu pakai di modul-modul berikutnya.

## Tujuan pembelajaran

Setelah modul ini kamu bisa:
1. Bergerak di antara folder, mengelola berkas, dan membaca isi berkas lewat terminal.
2. Memahami variabel lingkungan dan peran `~/.bashrc` dalam ROS 2.
3. Memakai Git untuk menyimpan dan mengunggah pekerjaan ke GitHub.
4. Menulis program Python dengan fungsi, kelas, dan modul.
5. Membaca pesan error Python dan menemukan penyebabnya.

---

## Bagian A — Terminal Linux

### Perintah yang wajib hafal

| Perintah | Arti | Contoh |
|---|---|---|
| `pwd` | Di folder mana aku sekarang? | `pwd` |
| `ls` | Lihat isi folder | `ls -la` (termasuk berkas tersembunyi) |
| `cd` | Pindah folder | `cd ~/ros2_ws` · `cd ..` (naik satu tingkat) |
| `mkdir` | Buat folder | `mkdir -p ~/ros2_ws/src` |
| `cp` / `mv` / `rm` | Salin / pindah / hapus | `cp a.py b.py` · `rm -r folder_lama` |
| `cat` / `less` | Tampilkan isi berkas | `less log.txt` (keluar dengan `q`) |
| `nano` / `code` | Edit berkas | `nano ~/.bashrc` |
| `grep` | Cari teks | `grep -r "Twist" ~/ros2_ws/src` |
| `\|` (pipe) | Sambungkan output ke perintah lain | `ros2 topic list \| grep turtle` |

> ⚠️ `rm` di Linux **tidak** memindahkan ke Recycle Bin. Berkas yang dihapus langsung hilang.

### Trik yang menghemat waktu

- **Tab** untuk melengkapi nama perintah, folder, bahkan nama topic ROS 2.
- **↑ / ↓** untuk memanggil perintah sebelumnya. **Ctrl+R** untuk mencari riwayat perintah.
- **Ctrl+C** menghentikan program yang sedang berjalan.
- Di terminal, **salin = Ctrl+Shift+C** dan **tempel = Ctrl+Shift+V**.

### Izin berkas

```bash
ls -l cek_lab.sh
# -rw-r--r--  → belum bisa dijalankan langsung
chmod +x cek_lab.sh
./cek_lab.sh
```

`chmod +x` memberi izin *execute*. Kamu akan sering melakukannya untuk skrip robot.

### Variabel lingkungan — kunci memahami ROS 2

Variabel lingkungan adalah pengaturan yang dibaca program saat berjalan.

```bash
echo $HOME           # folder rumahmu
echo $ROS_DISTRO     # jazzy (setelah source setup.bash)
export ROS_DOMAIN_ID=7
```

`source /opt/ros/jazzy/setup.bash` sebenarnya hanya mengatur banyak variabel lingkungan
agar terminal tahu di mana perintah dan paket ROS 2 berada. Berkas `~/.bashrc` dijalankan
setiap kali terminal baru dibuka — itulah kenapa kita menaruh perintah `source` di sana.

> 💡 `ROS_DOMAIN_ID` memisahkan "jaringan" ROS 2. Saat kelas berlangsung di satu Wi-Fi,
> tiap peserta memakai angka berbeda (0–101) agar robot simulasi tidak saling tertukar.

### Menginstal perangkat lunak

```bash
sudo apt install nama-paket       # paket sistem
apt search opencv                  # cari paket
```

**Penting untuk Python di Ubuntu 24.04:** perintah `pip install` ke sistem akan ditolak
(error `externally-managed-environment`). Gunakan urutan prioritas ini:

1. Paket apt bila tersedia: `sudo apt install python3-numpy python3-opencv`
2. Jika tidak ada di apt, buat *virtual environment* yang tetap bisa melihat paket ROS 2:
   ```bash
   python3 -m venv --system-site-packages ~/venv_robot
   source ~/venv_robot/bin/activate
   pip install nama-paket
   ```

---

## Bagian B — Git & GitHub

Semua latihan kursus ini kamu simpan di GitHub. Repo itu akan menjadi **portofolio** yang
bisa ditunjukkan saat melamar magang, kerja, atau seleksi tim robot.

```bash
git config --global user.name "Nama Kamu"
git config --global user.email "email@kamu.com"

mkdir -p ~/latihan-robotika && cd ~/latihan-robotika
git init
# ... buat atau ubah berkas ...
git status                 # apa yang berubah?
git add .                  # siapkan semua perubahan
git commit -m "Latihan 01: analisis log sensor"
```

Unggah ke GitHub:
1. Buat repo baru (kosong) di github.com, misalnya `latihan-robotika`.
2. Jalankan:
   ```bash
   git remote add origin https://github.com/<username>/latihan-robotika.git
   git branch -M main
   git push -u origin main
   ```
   GitHub akan meminta login. Gunakan *Personal Access Token* sebagai kata sandi
   (Settings → Developer settings di GitHub), atau instal GitHub CLI dan jalankan `gh auth login`.

Kebiasaan baik: **commit kecil dan sering**, dengan pesan yang menjelaskan *apa* yang berubah.

---

## Bagian C — Python untuk robotika

### Fungsi

```python
def jarak_euclid(x1, y1, x2, y2):
    """Jarak lurus antara dua titik."""
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

print(jarak_euclid(0, 0, 3, 4))   # 5.0
```

### Kelas — kenapa penting?

Setiap node ROS 2 yang akan kamu tulis berbentuk **kelas**. Kelas menggabungkan data
(misalnya status baterai) dan perilaku (misalnya cara mengisi ulang).

```python
class Baterai:
    def __init__(self, kapasitas_wh):
        self.kapasitas_wh = kapasitas_wh
        self.sisa_wh = kapasitas_wh

    def pakai(self, daya_w, detik):
        self.sisa_wh = max(0.0, self.sisa_wh - daya_w * detik / 3600)

    def persen(self):
        return 100 * self.sisa_wh / self.kapasitas_wh


bat = Baterai(kapasitas_wh=50)
bat.pakai(daya_w=20, detik=1800)   # 20 watt selama 30 menit
print(f'{bat.persen():.0f}%')      # 80%
```

Perhatikan pola `self.` — di Modul 2 kamu akan melihat `self.create_publisher(...)`
dengan pola yang sama persis.

### Modul dan import

```python
import math                       # modul bawaan
from math import pi, atan2        # ambil bagian tertentu saja
import csv                        # membaca berkas CSV
```

Program robot juga sering memecah kode ke beberapa berkas, lalu saling `import`.

### Membaca pesan error

```
Traceback (most recent call last):
  File "analisis_log.py", line 21, in baca_log
    nilai = float(baris['jarak_lidar_m'])
ValueError: could not convert string to float: ''
```

Baca dari **bawah ke atas**:
1. Baris terakhir = *jenis* dan *isi* error (`ValueError`: teks kosong tidak bisa jadi angka).
2. Di atasnya = *lokasi* error (berkas, nomor baris, fungsi).

Tangani error yang memang mungkin terjadi dengan `try`/`except`:

```python
try:
    nilai = float(teks)
except ValueError:
    nilai = None   # data rusak/kosong, lewati
```

Data sensor sungguhan **sering** berisi nilai kosong atau rusak — program robot harus tahan terhadapnya.

---

## Latihan

Kerjakan **[Latihan 01 — Analisis Log Sensor](../latihan/01-log-sensor/)**, lalu unggah
hasilnya ke repo GitHub-mu sendiri.

## Kuis singkat

1. Perintah apa untuk melihat semua berkas, termasuk yang tersembunyi?
2. Kenapa perintah `source /opt/ros/jazzy/setup.bash` ditaruh di `~/.bashrc`?
3. Apa gunanya `ROS_DOMAIN_ID` saat belajar bersama di satu jaringan?
4. `pip install numpy` ditolak dengan error `externally-managed-environment`. Apa yang sebaiknya kamu lakukan?
5. Dalam traceback Python, di bagian mana kamu menemukan jenis error-nya?
6. Kenapa node ROS 2 ditulis dalam bentuk kelas?

<details><summary>Kunci jawaban</summary>

1. `ls -la`
2. Agar ROS 2 otomatis aktif setiap kali membuka terminal baru.
3. Memisahkan komunikasi ROS 2 tiap peserta agar tidak saling tertukar.
4. Pakai `sudo apt install python3-numpy`, atau virtual environment dengan `--system-site-packages`.
5. Baris paling bawah.
6. Kelas menyatukan data (status node) dan perilakunya (callback, timer) dalam satu wadah.
</details>
