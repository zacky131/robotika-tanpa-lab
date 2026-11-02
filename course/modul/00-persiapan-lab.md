# Modul 0 — Persiapan Lab di Laptopmu

> **Estimasi:** 2 jam · **Hasil akhir:** ROS 2 Jazzy + Gazebo berjalan, skrip `cek_lab.sh` hijau semua

Selamat datang di **Lab Robotika Tanpa Lab**! Di kursus ini kamu tidak perlu membeli robot.
Lab-mu adalah laptopmu sendiri. Modul ini memastikan "lab" itu siap dipakai.

## Tujuan pembelajaran

Setelah modul ini kamu bisa:
1. Memilih cara instalasi yang cocok dengan laptopmu.
2. Menginstal ROS 2 Jazzy dan Gazebo Harmonic.
3. Memverifikasi instalasi dengan demo `talker`/`listener`, turtlesim, dan Gazebo.
4. Mengatasi masalah instalasi yang paling sering muncul.

## Kenapa ROS 2 Jazzy dan Gazebo Harmonic?

- **ROS 2** (Robot Operating System 2) adalah kerangka kerja standar untuk perangkat lunak robot,
  dipakai di riset, industri, dan kompetisi.
- **Jazzy Jalisco** adalah rilis *LTS* (dukungan jangka panjang), jadi materi ini tetap relevan
  selama bertahun-tahun.
- **Gazebo Harmonic** adalah simulator yang dipasangkan resmi dengan Jazzy.

Keduanya gratis dan *open source*.

## Kebutuhan laptop

| | Minimum | Disarankan |
|---|---|---|
| RAM | 8 GB | 16 GB |
| Ruang disk kosong | 30 GB | 50 GB |
| Prosesor | 4 core (Intel i5 / Ryzen 5 generasi beberapa tahun terakhir) | lebih baru lebih baik |
| Kartu grafis | **tidak perlu** GPU khusus | — |

## Langkah 1 — Pilih jalur instalasi

ROS 2 Jazzy berjalan paling baik di **Ubuntu 24.04**. Pilih satu jalur:

| Jalur | Cocok untuk | Catatan |
|---|---|---|
| **A. Ubuntu 24.04 langsung / dual boot** | Performa terbaik | Disarankan jika kamu berani mempartisi disk |
| **B. Windows 11 + WSL2** | Pengguna Windows yang tidak mau dual boot | Paling praktis; Gazebo sedikit lebih lambat |
| **C. Docker** | Yang sudah biasa memakai Docker | Butuh pengaturan tampilan GUI tambahan |

Pengguna Mac: gunakan mesin virtual (misalnya UTM) dengan Ubuntu 24.04, atau ikuti jalur C.

### Jalur A — Ubuntu 24.04

Unduh Ubuntu 24.04 LTS dari situs resmi Ubuntu, buat USB bootable, lalu instal
(pilih "Install alongside Windows" untuk dual boot). **Cadangkan data penting sebelum mempartisi disk.**

### Jalur B — Windows 11 + WSL2

Buka **PowerShell sebagai Administrator**, lalu:

```powershell
wsl --install -d Ubuntu-24.04
```

Mulai ulang laptop, buka aplikasi **Ubuntu 24.04**, lalu buat nama pengguna dan kata sandi.
Windows 11 sudah mendukung aplikasi grafis Linux (WSLg), jadi RViz dan Gazebo bisa tampil di layar.

Agar WSL tidak memakan semua RAM, buat berkas `C:\Users\<nama>\.wslconfig`:

```ini
[wsl2]
memory=6GB
swap=4GB
```

## Langkah 2 — Siapkan Ubuntu

Semua perintah berikut dijalankan di **terminal Ubuntu** (Ctrl+Alt+T di Ubuntu, atau aplikasi Ubuntu di Windows).

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y software-properties-common curl git
sudo add-apt-repository universe -y
```

Pastikan *locale* mendukung UTF-8:

```bash
locale   # pastikan ada tulisan UTF-8
```

## Langkah 3 — Instal ROS 2 Jazzy

Tambahkan sumber paket ROS 2 resmi:

```bash
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo $VERSION_CODENAME)_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
```

Instal ROS 2 (versi *desktop* sudah termasuk RViz, turtlesim, dan contoh-contoh):

```bash
sudo apt update
sudo apt install -y ros-jazzy-desktop ros-dev-tools
```

Proses ini bisa memakan waktu 10–30 menit tergantung koneksi internet.

> 💡 Jika langkah di atas gagal, cek panduan instalasi resmi di dokumentasi ROS 2 Jazzy
> (docs.ros.org) — kadang ada pembaruan kecil pada cara menambahkan sumber paket.

Agar ROS 2 aktif otomatis setiap kali terminal dibuka:

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## Langkah 4 — Instal Gazebo Harmonic

```bash
sudo apt install -y ros-jazzy-ros-gz python3-opencv
```

Paket `ros-jazzy-ros-gz` memasang Gazebo Harmonic sekaligus "jembatan" antara ROS 2 dan Gazebo.

## Langkah 5 — Uji coba pertama 🎉

**Uji 1: dua program saling bicara.** Buka dua terminal.

```bash
# Terminal 1
ros2 run demo_nodes_py talker
```
```bash
# Terminal 2
ros2 run demo_nodes_py listener
```

Kalau terminal 2 mencetak `I heard: [Hello World: ...]`, selamat — dua program ROS 2 sudah
berkomunikasi. Hentikan dengan **Ctrl+C**.

**Uji 2: kura-kura.**

```bash
# Terminal 1
ros2 run turtlesim turtlesim_node
```
```bash
# Terminal 2
ros2 run turtlesim turtle_teleop_key
```

Klik terminal 2, lalu gerakkan kura-kura dengan tombol panah.

**Uji 3: simulator 3D.**

```bash
gz sim shapes.sdf
```

Jendela Gazebo terbuka dengan beberapa bentuk 3D. Tekan tombol ▶ (play) di kiri bawah.

## Langkah 6 — Cek kesehatan lab

Unduh repo kursus dan jalankan skrip pengecekan:

```bash
cd ~
git clone https://github.com/zacky131/robotika-tanpa-lab.git
bash ~/robotika-tanpa-lab/course/kode/cek_lab.sh
```

Semua baris harus **[ OK ]**. Baris **[AWAS]** boleh dilewati dulu; baris **[GAGAL]** harus diperbaiki.

## Tips laptop RAM 8 GB

- Tutup browser dan aplikasi berat saat menjalankan Gazebo.
- Jalankan Gazebo tanpa jendela grafis jika tidak perlu melihatnya: `gz sim -s -r shapes.sdf`.
- Di WSL2, jangan memberi `memory` lebih dari ~75% RAM laptop.
- Jika Gazebo tetap berat, simulator **Webots** bisa jadi alternatif (dibahas di modul simulasi).

## Pemecahan masalah

| Gejala | Penyebab umum | Solusi |
|---|---|---|
| `ros2: command not found` | `setup.bash` belum di-*source* | `source /opt/ros/jazzy/setup.bash`, lalu cek `~/.bashrc` |
| `Unable to locate package ros-jazzy-desktop` | Bukan Ubuntu 24.04, atau sumber paket belum ditambahkan | Cek versi: `lsb_release -a`; ulangi Langkah 3 |
| Listener tidak menerima pesan | Firewall atau jaringan kantor/kampus | `export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST` di kedua terminal |
| Gazebo hitam / langsung tertutup (WSL2) | Masalah akselerasi grafis | `export LIBGL_ALWAYS_SOFTWARE=1` lalu jalankan ulang |
| Gazebo sangat lambat | RAM/CPU terbatas | Lihat "Tips laptop RAM 8 GB" |
| Pesan error lain | — | Salin **seluruh** pesan error ke forum kursus, sertakan hasil `cek_lab.sh` |

## Latihan

Kerjakan **[Latihan 00](../latihan/00-persiapan/)**.

## Kuis singkat

1. Kenapa kursus ini memakai ROS 2 Jazzy, bukan rilis lain?
2. Apa fungsi baris `source /opt/ros/jazzy/setup.bash`?
3. Pada uji `talker`/`listener`, mana yang mengirim dan mana yang menerima?
4. Paket apa yang memasang Gazebo Harmonic beserta jembatannya ke ROS 2?
5. Laptopmu RAM 8 GB dan Gazebo terasa berat. Sebutkan dua hal yang bisa kamu lakukan.

<details><summary>Kunci jawaban</summary>

1. Jazzy adalah rilis LTS (dukungan jangka panjang) dan dipasangkan resmi dengan Gazebo Harmonic.
2. Mengaktifkan perintah dan paket ROS 2 di terminal tersebut (mengatur variabel lingkungan).
3. `talker` mengirim (publisher), `listener` menerima (subscriber).
4. `ros-jazzy-ros-gz`.
5. Contoh: menutup aplikasi lain, menjalankan Gazebo tanpa GUI (`-s`), membatasi memori WSL, memakai Webots.
</details>
