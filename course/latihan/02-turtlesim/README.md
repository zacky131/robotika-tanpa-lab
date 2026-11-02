# Latihan 02 — Kura-kura Otonom

**Modul:** [2 — Node & Topic](../../modul/02-node-topic.md) · **Waktu:** 90–120 menit

## Persiapan

Pastikan paket `rtl_dasar` sudah terhubung dan ter-*build* (Modul 2, Bagian C):

```bash
cd ~/ros2_ws && colcon build --symlink-install && source install/setup.bash
```

## Tugas

**1. Selidiki (15 menit).** Jalankan turtlesim dan `kura_spiral`, lalu jawab di berkas `jawaban.md`:
- Node apa saja yang aktif? (`ros2 node list`)
- Berapa frekuensi `/turtle1/cmd_vel` yang dikirim `kura_spiral`? (`ros2 topic hz`)
- Tempel tangkapan layar `rqt_graph`.

**2. Persegi loop terbuka (20 menit).** Jalankan `kura_persegi` dengan tiga ukuran sisi
(1, 2, dan 4), masing-masing **dua kali**. Sebelum tiap percobaan, kembalikan kura-kura ke
tengah dengan `ros2 service call /reset std_srvs/srv/Empty`. Catat seberapa jauh titik akhir
dari titik awal (5,54; 5,54) dan arah akhirnya (pakai `pemantau_kura`).
Apakah galatnya selalu sama? Apakah makin besar untuk persegi yang lebih besar? Kenapa?

**3. Node buatanmu: segitiga (30 menit).** Buat paketmu sendiri:
```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python --license MIT \
  --dependencies rclpy geometry_msgs turtlesim kura_saya
```
Buat node `kura_segitiga` di `kura_saya/kura_saya/` (boleh menyalin `kura_persegi.py` sebagai
titik awal). Sudut belok segitiga sama sisi = 120° (2π/3 rad). Daftarkan di `setup.py` pada
bagian `console_scripts`:
```python
'kura_segitiga = kura_saya.kura_segitiga:main',
```
lalu `colcon build --symlink-install`, `source install/setup.bash`, dan
`ros2 run kura_saya kura_segitiga`. Jalankan juga `colcon test` — gaya kodemu ikut diperiksa.

**4. Rem darurat (40 menit).**

*4a — Cara naif.* Salin `pemantau_kura` menjadi `pemantau_rem` lalu ubah agar tidak hanya
memberi peringatan, tetapi juga **mengirim perintah berhenti** (`Twist()` kosong) ke
`/turtle1/cmd_vel` saat jarak ke dinding < 0,5. Uji dengan spiral yang cukup besar untuk
mencapai dinding:
```bash
ros2 run rtl_dasar kura_spiral --ros-args \
  -p kecepatan_belok:=1.0 -p pertambahan:=0.3 -p durasi:=30.0
```
Amati: kura-kura **tetap menabrak dinding** (turtlesim mencetak `Oh no! I hit the wall!`).
Kenapa? Tulis jawabanmu di `jawaban.md`. (Petunjuk: `ros2 topic info /turtle1/cmd_vel` —
ada berapa publisher, dan masing-masing mengirim berapa kali per detik?)

*4b — Filter keselamatan.* Perbaiki desainnya: jadikan `pemantau_rem` **satu-satunya**
publisher ke `/turtle1/cmd_vel`. Node lain mengirim perintah ke `/cmd_vel_mentah`;
`pemantau_rem` berlangganan topic itu dan meneruskannya — kecuali saat terlalu dekat
dinding, ia mengirim perintah berhenti. Kamu tidak perlu mengubah kode `kura_spiral`:
cukup **remap** nama topic-nya saat dijalankan dengan `-r nama_lama:=nama_baru`:
```bash
ros2 run rtl_dasar kura_spiral --ros-args -r /turtle1/cmd_vel:=/cmd_vel_mentah \
  -p kecepatan_belok:=1.0 -p pertambahan:=0.3 -p durasi:=30.0
```
Pola ini persis yang dipakai robot sungguhan: perintah dari perencana gerak selalu
melewati lapisan keselamatan sebelum sampai ke motor.

Contoh solusi: [`solusi/pemantau_rem.py`](solusi/pemantau_rem.py).

## Tantangan: persegi loop tertutup ⭐

Tulis node yang menggambar persegi dengan membaca `/turtle1/pose` dan terus mengoreksi
arah menuju setiap sudut. Targetkan titik akhir berjarak < 0,05 dari titik awal.

Petunjuk:
- Arah ke target: `math.atan2(dy, dx)`; galat arah = arah target − `pose.theta`.
- Selalu normalisasi galat sudut ke rentang [−π, π].
- Putar dulu sampai menghadap target, baru maju. Perlambat saat sudah dekat.

Contoh solusi: [`solusi/kura_persegi_tertutup.py`](solusi/kura_persegi_tertutup.py).

## Yang dikumpulkan

Repo GitHub berisi paket dengan `kura_segitiga` dan `pemantau_rem` (versi 4b),
`jawaban.md`, serta video layar pendek (≤ 1 menit) kura-kura menggambar segitiga.

## Lulus jika

- [ ] `jawaban.md` menjawab tugas 1, 2, dan 4a
- [ ] `kura_segitiga` jalan dengan `ros2 run`
- [ ] Rem darurat (4b) menghentikan kura-kura sebelum menyentuh dinding
- [ ] (Bonus) Persegi loop tertutup dengan galat < 0,05
