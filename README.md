# Lab Robotika Tanpa Lab

**Belajar robotika otonom tanpa perlu lab mahal.** Semua materi berbasis simulasi
(ROS 2 + Gazebo/Webots) dan berjalan di laptop biasa — tanpa GPU khusus, tanpa robot fisik.

Repositori ini berisi materi **gratis** (silabus dan Modul 0–2) dari program pendidikan
robotika & AI berbahasa Indonesia, untuk tiga kelompok:

| Untuk siapa | Program | Format |
|---|---|---|
| Mahasiswa & pembelajar mandiri | Kursus **"ROS2 & Robotika Otonom dari Nol"** | Online, mandiri + cohort live |
| Tim robot kampus (KRI, KRAI, KRTI) | **Bootcamp 4 akhir pekan** per tim: ROS 2, computer vision, otonomi PX4 | Online live, dibiayai kampus |
| SMK & guru | **Paket "Lab Robotika Tanpa Lab"**: kurikulum + bimtek guru | Online-first, pendampingan |

Pengajar: **Muhammad Zacky Asy'ari** — peneliti PhD IT Convergence (Kumoh National
Institute of Technology, Korea), dosen Universitas Darma Persada, sebelumnya dosen
Automotive & Robotics Engineering di Binus.

## Struktur repositori

```
course/        Materi kursus: silabus, modul, latihan, kode
  ├─ silabus-ros2-dari-nol.tex   Silabus lengkap (sumber PDF)
  ├─ modul/                      Materi per modul
  ├─ latihan/                    Latihan simulasi
  └─ kode/                       Kode contoh (paket ROS 2)
latex/         Template LaTeX bersama (rtl.cls) — dipakai semua dokumen
pdf/           Hasil build PDF (dibuat otomatis, jangan diedit manual)
scripts/       Skrip build
```

## Membangun PDF

Semua dokumen memakai template `latex/rtl.cls`.

```bash
./scripts/build-pdf.sh                       # semua dokumen
./scripts/build-pdf.sh course/xxx.tex        # satu dokumen
```

Butuh TeX Live (`latexmk`, `texlive-latex-extra`). PDF terbaru selalu tersedia
di folder `pdf/`. Workflow GitHub Actions (`.github/workflows/build-pdf.yml`)
juga bisa dijalankan manual dari tab Actions.

Dokumen baru cukup diawali:

```latex
\documentclass{rtl}          % atau [onepage] untuk one-pager
\title{Judul} \subtitle{Subjudul} \doctype{Jenis Dokumen} \date{November 2026}
\begin{document}
\makeheader
...
\end{document}
```

## Materi lengkap

Modul 3–11, proyek akhir "Robot Kurir Kampus", dan materi bootcamp tersedia untuk
peserta terdaftar. Hubungi kontak di bawah untuk info pendaftaran.

## Lisensi

Kode: MIT (`LICENSE`). Materi pelajaran dan PDF: CC BY-NC 4.0 (`LICENSE-CONTENT.md`).

## Kontak

zacky.asyari1986@gmail.com
