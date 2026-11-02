# Latihan 01 — Analisis Log Sensor Robot

**Modul:** [1 — Linux & Python](../../modul/01-linux-python.md) · **Waktu:** 60–90 menit

## Cerita

Robot kurir di gudang merekam data sensornya selama 2 menit ke berkas
[`data/log_sensor.csv`](data/log_sensor.csv):

| Kolom | Arti |
|---|---|
| `waktu_s` | waktu sejak robot menyala (detik) |
| `jarak_lidar_m` | jarak ke rintangan terdekat di depan robot (meter) |
| `suhu_motor_c` | suhu motor (°C) |
| `tegangan_baterai_v` | tegangan baterai (volt) |

Operator ingin tahu: *seberapa sering robot hampir menabrak, dan apakah baterai serta motornya aman?*

## Tugas

1. Salin berkas awal ke repo latihanmu:
   ```bash
   mkdir -p ~/latihan-robotika/01-log-sensor
   cp -r ~/robotika-tanpa-lab/course/latihan/01-log-sensor/{mulai,data} ~/latihan-robotika/01-log-sensor/
   cd ~/latihan-robotika/01-log-sensor/mulai
   python3 analisis_log.py ../data/log_sensor.csv
   ```
2. Lengkapi **TODO 1–4** di `analisis_log.py`:
   - **TODO 1** — baca CSV, ubah ke angka, lewati baris rusak (ada satu yang sengaja dikosongkan).
   - **TODO 2** — hitung rata-rata, minimum, maksimum.
   - **TODO 3** — hitung *kejadian* hampir menabrak (bacaan berturut-turut < 0,30 m dihitung satu kejadian).
   - **TODO 4** — cetak peringatan suhu motor dan baterai.
3. Commit dan push ke GitHub-mu.

## Hasil yang benar

```
Jumlah bacaan valid : 239 (dilewati: 1)
...
Kejadian hampir menabrak (< 0.3 m): 2
  - detik 35.0 s.d. 38.5
  - detik 90.0 s.d. 92.5
Baterai aman (11.64 V)
```

## Lulus jika

- [ ] Program tidak *crash* walaupun ada baris kosong
- [ ] Ringkasan tiga sensor benar
- [ ] Jumlah kejadian hampir menabrak = 2 beserta waktunya
- [ ] Kode ada di repo GitHub-mu dengan minimal 2 commit

## Tantangan tambahan

- Ubah `SUHU_PANAS_C` menjadi 45. Mulai detik ke berapa motor dianggap panas?
- Tambahkan argumen kedua untuk ambang jarak: `python3 analisis_log.py data.csv 0.5`.
- Buat grafik jarak terhadap waktu dengan `matplotlib` (`sudo apt install python3-matplotlib`).

Sudah mencoba sungguh-sungguh dan masih buntu? Lihat [`solusi/`](solusi/).
