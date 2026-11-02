#!/usr/bin/env bash
# =====================================================================
#  cek_lab.sh — Cek kesehatan "lab" di laptopmu (Modul 0)
#  Lab Robotika Tanpa Lab
#
#  Pemakaian:
#     bash cek_lab.sh
#  Semua baris harus [ OK ]. Kirim tangkapan layar hasilnya sebagai
#  bukti Latihan 00.
# =====================================================================

HIJAU='\033[0;32m'; MERAH='\033[0;31m'; KUNING='\033[0;33m'; NORMAL='\033[0m'
LULUS=0; GAGAL=0; PERINGATAN=0

ok()    { echo -e "${HIJAU}[ OK ]${NORMAL} $1"; LULUS=$((LULUS+1)); }
gagal() { echo -e "${MERAH}[GAGAL]${NORMAL} $1"; echo "        → $2"; GAGAL=$((GAGAL+1)); }
awas()  { echo -e "${KUNING}[AWAS]${NORMAL} $1"; echo "        → $2"; PERINGATAN=$((PERINGATAN+1)); }

echo "=== Cek Lab Robotika Tanpa Lab ==="
echo

# 1. Sistem operasi
if [ -r /etc/os-release ]; then
  . /etc/os-release
  if [ "${VERSION_ID:-}" = "24.04" ]; then
    ok "Ubuntu 24.04 ($PRETTY_NAME)"
  else
    gagal "Sistem operasi: ${PRETTY_NAME:-tidak dikenal}" "ROS 2 Jazzy membutuhkan Ubuntu 24.04 (lihat Modul 0)."
  fi
fi
if grep -qi microsoft /proc/version 2>/dev/null; then
  echo "        (terdeteksi berjalan di WSL2)"
fi

# 2. Memori
RAM_GB=$(awk '/MemTotal/ {printf "%.1f", $2/1024/1024}' /proc/meminfo)
RAM_INT=${RAM_GB%.*}
if [ "$RAM_INT" -ge 7 ]; then
  ok "RAM ${RAM_GB} GB"
else
  awas "RAM ${RAM_GB} GB" "Di bawah 8 GB: Gazebo bisa lambat. Pakai tips hemat memori di Modul 0 (atau Webots)."
fi

# 3. ROS 2
if [ "${ROS_DISTRO:-}" = "jazzy" ]; then
  ok "ROS_DISTRO=jazzy"
else
  gagal "ROS_DISTRO belum 'jazzy' (sekarang: '${ROS_DISTRO:-kosong}')" \
        "Jalankan: echo 'source /opt/ros/jazzy/setup.bash' >> ~/.bashrc lalu buka terminal baru."
fi

if command -v ros2 >/dev/null 2>&1; then
  ok "Perintah ros2 tersedia"
else
  gagal "Perintah ros2 tidak ditemukan" "Instal ros-jazzy-desktop dan source setup.bash (Modul 0, langkah 3)."
fi

# 4. Paket penting
for pkg in demo_nodes_py turtlesim rviz2 ros_gz_sim; do
  if command -v ros2 >/dev/null 2>&1 && ros2 pkg prefix "$pkg" >/dev/null 2>&1; then
    ok "Paket $pkg"
  else
    case $pkg in
      ros_gz_sim) saran="sudo apt install ros-jazzy-ros-gz" ;;
      *)          saran="sudo apt install ros-jazzy-desktop" ;;
    esac
    gagal "Paket $pkg belum terpasang" "$saran"
  fi
done

# 5. Gazebo
if command -v gz >/dev/null 2>&1; then
  GZV=$(gz sim --versions 2>/dev/null | head -1)
  ok "Gazebo tersedia (gz sim ${GZV:-?})"
else
  gagal "Perintah gz (Gazebo) tidak ditemukan" "sudo apt install ros-jazzy-ros-gz"
fi

# 6. Alat pengembangan
command -v colcon >/dev/null 2>&1 && ok "colcon" || gagal "colcon tidak ditemukan" "sudo apt install ros-dev-tools"
command -v git    >/dev/null 2>&1 && ok "git"    || gagal "git tidak ditemukan" "sudo apt install git"
python3 -c "import cv2" 2>/dev/null && ok "Python OpenCV" || awas "OpenCV untuk Python belum ada" "Dibutuhkan mulai Modul 8: sudo apt install python3-opencv"

# 7. Uji komunikasi ROS 2 (talker -> listener)
if command -v ros2 >/dev/null 2>&1; then
  ros2 run demo_nodes_py talker >/dev/null 2>&1 &
  PID_TALKER=$!
  if timeout 10 ros2 topic echo /chatter --once >/dev/null 2>&1; then
    ok "Komunikasi ROS 2 (talker → /chatter) berjalan"
  else
    gagal "Tidak ada pesan di /chatter dalam 10 detik" "Coba: export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST, atau cek firewall (Modul 0, Pemecahan Masalah)."
  fi
  kill $PID_TALKER 2>/dev/null; wait $PID_TALKER 2>/dev/null
fi

echo
echo "=== Hasil: $LULUS lulus, $PERINGATAN peringatan, $GAGAL gagal ==="
if [ $GAGAL -eq 0 ]; then
  echo -e "${HIJAU}Lab kamu siap! Lanjut ke Modul 1.${NORMAL}"
else
  echo -e "${MERAH}Perbaiki item [GAGAL] di atas, lalu jalankan skrip ini lagi.${NORMAL}"
fi
exit $GAGAL
