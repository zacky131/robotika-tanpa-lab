"""Latihan 01 — KODE AWAL: analisis log sensor robot.

Lengkapi bagian bertanda TODO. Jalankan:
    python3 analisis_log.py ../data/log_sensor.csv

Petunjuk: jangan intip folder solusi/ sebelum mencoba minimal 30 menit :)
"""
import csv
import sys

JARAK_BAHAYA_M = 0.30       # di bawah ini dianggap hampir menabrak
TEGANGAN_RENDAH_V = 11.5    # di bawah ini baterai perlu diisi
SUHU_PANAS_C = 60.0         # di atas ini motor terlalu panas


def baca_log(nama_berkas):
    """Membaca CSV dan mengembalikan (data, jumlah_baris_dilewati).

    data adalah list of dict, contoh satu elemen:
        {'waktu_s': 0.0, 'jarak_lidar_m': 1.55, 'suhu_motor_c': 31.0, 'tegangan_baterai_v': 12.6}
    """
    data = []
    dilewati = 0
    with open(nama_berkas, newline='') as f:
        for baris in csv.DictReader(f):
            # TODO 1: ubah semua nilai di `baris` menjadi float lalu tambahkan ke `data`.
            #         Ada satu baris yang nilainya kosong — float('') akan error (ValueError).
            #         Tangkap error itu dengan try/except dan tambah `dilewati`.
            pass
    return data, dilewati


def ringkas(nilai):
    """Mengembalikan (rata_rata, minimum, maksimum) dari list angka."""
    # TODO 2: hitung tiga nilai ini. Boleh pakai sum(), len(), min(), max().
    return 0.0, 0.0, 0.0


def hitung_kejadian(data, kolom, syarat):
    """Mengelompokkan bacaan BERURUTAN yang memenuhi syarat menjadi satu 'kejadian'.

    Contoh: 8 bacaan berturut-turut dengan jarak < 0.3 m dihitung 1 kejadian, bukan 8.
    Mengembalikan list berisi tuple (waktu_mulai, waktu_selesai).
    `syarat` adalah fungsi, misalnya: lambda x: x < 0.3
    """
    kejadian = []
    # TODO 3 (tantangan): telusuri `data` satu per satu dan catat kapan kejadian
    #         dimulai dan berakhir. Jangan lupa kejadian yang masih berlangsung
    #         di baris terakhir.
    return kejadian


def main():
    if len(sys.argv) != 2:
        print('Pemakaian: python3 analisis_log.py <berkas.csv>')
        sys.exit(1)

    data, dilewati = baca_log(sys.argv[1])
    if not data:
        print('Belum ada data terbaca — kerjakan TODO 1 dulu.')
        sys.exit(1)

    print(f'Jumlah bacaan valid : {len(data)} (dilewati: {dilewati})')

    print(f'{"Sensor":<22}{"rata-rata":>10}{"min":>8}{"maks":>8}')
    for kolom in ['jarak_lidar_m', 'suhu_motor_c', 'tegangan_baterai_v']:
        rata, terendah, tertinggi = ringkas([b[kolom] for b in data])
        print(f'{kolom:<22}{rata:>10.2f}{terendah:>8.2f}{tertinggi:>8.2f}')

    hampir_tabrak = hitung_kejadian(data, 'jarak_lidar_m', lambda x: x < JARAK_BAHAYA_M)
    print(f'\nKejadian hampir menabrak (< {JARAK_BAHAYA_M} m): {len(hampir_tabrak)}')
    for mulai, selesai in hampir_tabrak:
        print(f'  - detik {mulai:.1f} s.d. {selesai:.1f}')

    # TODO 4: cetak PERINGATAN jika suhu motor pernah melewati SUHU_PANAS_C,
    #         dan jika tegangan baterai di bacaan TERAKHIR di bawah TEGANGAN_RENDAH_V.


if __name__ == '__main__':
    main()
