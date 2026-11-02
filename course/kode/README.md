# Kode Kursus

| Isi | Modul | Keterangan |
|---|---|---|
| [`cek_lab.sh`](cek_lab.sh) | 0 | Cek kesehatan instalasi ROS 2 + Gazebo |
| [`rtl_dasar/`](rtl_dasar/) | 2 | Paket ROS 2 Python: publisher/subscriber, turtlesim (persegi, spiral, pemantau) |

Target: **ROS 2 Jazzy + Gazebo Harmonic di Ubuntu 24.04**.

## Memakai paket di workspace-mu

```bash
mkdir -p ~/ros2_ws/src
ln -s ~/robotika-tanpa-lab/course/kode/rtl_dasar ~/ros2_ws/src/rtl_dasar
cd ~/ros2_ws && colcon build --symlink-install
source install/setup.bash
ros2 run rtl_dasar penerbit_halo
```
