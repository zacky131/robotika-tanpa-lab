"""Latihan 01 — SOLUSI: analisis log sensor robot.

Pemakaian:
    python3 analisis_log.py ../data/log_sensor.csv
"""
import csv
import sys

JARAK_BAHAYA_M = 0.30       # di bawah ini dianggap hampir menabrak
TEGANGAN_RENDAH_V = 11.5    # di bawah ini baterai perlu diisi
SUHU_PANAS_C = 60.0         # di atas ini motor terlalu panas


def baca_log(nama_berkas):
    """Membaca CSV dan mengembalikan list of dict. Baris dengan nilai kosong dilewati."""
    data = []
    dilewati = 0
    with open(nama_berkas, newline='') as f:
        for baris in csv.DictReader(f):
            try:
                data.append({kunci: float(nilai) for kunci, nilai in baris.items()})
            except ValueError:
                dilewati += 1
    return data, dilewati


def ringkas(nilai):
    """Rata-rata, minimum, maksimum dari sebuah list angka."""
    return sum(nilai) / len(nilai), min(nilai), max(nilai)


def hitung_kejadian(data, kolom, syarat):
    """Mengelompokkan baris berurutan yang memenuhi syarat menjadi 'kejadian'.

    Contoh: 8 bacaan berturut-turut dengan jarak < 0.3 m = 1 kejadian.
    Mengembalikan list (waktu_mulai, waktu_selesai).
    """
    kejadian = []
    mulai = None
    sebelumnya = None
    for baris in data:
        if syarat(baris[kolom]):
            if mulai is None:
                mulai = baris['waktu_s']
            sebelumnya = baris['waktu_s']
        elif mulai is not None:
            kejadian.append((mulai, sebelumnya))
            mulai = None
    if mulai is not None:
        kejadian.append((mulai, sebelumnya))
    return kejadian


def main():
    if len(sys.argv) != 2:
        print('Pemakaian: python3 analisis_log.py <berkas.csv>')
        sys.exit(1)

    data, dilewati = baca_log(sys.argv[1])
    print(f'Jumlah bacaan valid : {len(data)} (dilewati: {dilewati})')
    print(f'Durasi rekaman      : {data[-1]["waktu_s"] - data[0]["waktu_s"]:.1f} detik\n')

    print(f'{"Sensor":<22}{"rata-rata":>10}{"min":>8}{"maks":>8}')
    for kolom in ['jarak_lidar_m', 'suhu_motor_c', 'tegangan_baterai_v']:
        rata, terendah, tertinggi = ringkas([b[kolom] for b in data])
        print(f'{kolom:<22}{rata:>10.2f}{terendah:>8.2f}{tertinggi:>8.2f}')

    print()
    hampir_tabrak = hitung_kejadian(data, 'jarak_lidar_m', lambda x: x < JARAK_BAHAYA_M)
    print(f'Kejadian hampir menabrak (< {JARAK_BAHAYA_M} m): {len(hampir_tabrak)}')
    for mulai, selesai in hampir_tabrak:
        print(f'  - detik {mulai:.1f} s.d. {selesai:.1f}')

    panas = [b for b in data if b['suhu_motor_c'] > SUHU_PANAS_C]
    if panas:
        print(f'PERINGATAN: motor > {SUHU_PANAS_C} °C mulai detik {panas[0]["waktu_s"]:.1f}')

    tegangan_akhir = data[-1]['tegangan_baterai_v']
    if tegangan_akhir < TEGANGAN_RENDAH_V:
        print(f'PERINGATAN: baterai rendah ({tegangan_akhir:.2f} V) — isi ulang!')
    else:
        print(f'Baterai aman ({tegangan_akhir:.2f} V)')


if __name__ == '__main__':
    main()
