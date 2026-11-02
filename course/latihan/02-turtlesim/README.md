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
(1, 2, dan 4). Catat seberapa jauh titik akhir dari titik awal (pakai `pemantau_kura`).
Apakah galatnya makin besar untuk persegi yang lebih besar? Kenapa?

**3. Node buatanmu: segitiga (30 menit).** Buat node baru `kura_segitiga` di paketmu sendiri
(boleh menyalin `kura_persegi` sebagai titik awal). Sudut belok segitiga sama sisi = 120°.
Daftarkan di `setup.py`, lalu `colcon build`.

**4. Pemantau + rem darurat (30 menit).** Ubah `pemantau_kura` (salin dulu) agar tidak
hanya memberi peringatan, tetapi juga **mengirim perintah berhenti** ke `/turtle1/cmd_vel`
saat jarak ke dinding < 0,5. Uji dengan `kura_spiral` berdurasi panjang:
```bash
ros2 run rtl_dasar kura_spiral --ros-args -p durasi:=30.0
```
Pertanyaan: kura-kura berhenti sejenak lalu bergerak lagi. Kenapa? (Petunjuk: ada dua
publisher ke topic yang sama.) Tulis jawabanmu di `jawaban.md`.

## Tantangan: persegi loop tertutup ⭐

Tulis node yang menggambar persegi dengan membaca `/turtle1/pose` dan terus mengoreksi
arah menuju setiap sudut. Targetkan titik akhir berjarak < 0,05 dari titik awal.

Petunjuk:
- Arah ke target: `math.atan2(dy, dx)`; galat arah = arah target − `pose.theta`.
- Selalu normalisasi galat sudut ke rentang [−π, π].
- Putar dulu sampai menghadap target, baru maju. Perlambat saat sudah dekat.

Contoh solusi: [`solusi/kura_persegi_tertutup.py`](solusi/kura_persegi_tertutup.py).

## Yang dikumpulkan

Repo GitHub berisi paket dengan `kura_segitiga` dan pemantau rem darurat,
`jawaban.md`, serta video layar pendek (≤ 1 menit) kura-kura menggambar segitiga.

## Lulus jika

- [ ] `jawaban.md` menjawab tugas 1, 2, dan 4
- [ ] `kura_segitiga` jalan dengan `ros2 run`
- [ ] Rem darurat menghentikan kura-kura sebelum menyentuh dinding
- [ ] (Bonus) Persegi loop tertutup dengan galat < 0,05
