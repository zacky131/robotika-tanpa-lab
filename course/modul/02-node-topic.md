# Modul 2 — Konsep Inti ROS 2: Node & Topic

> **Estimasi:** 3 jam · **Hasil akhir:** paket ROS 2 pertamamu yang menggerakkan kura-kura

Di modul ini kamu mulai berpikir seperti perancang sistem robot: sebuah robot bukan
satu program raksasa, melainkan **banyak program kecil yang saling mengirim data**.

## Tujuan pembelajaran

Setelah modul ini kamu bisa:
1. Menjelaskan *node*, *topic*, *message*, *publisher*, dan *subscriber*.
2. Menyelidiki sistem ROS 2 yang sedang berjalan dengan perintah `ros2` dan `rqt_graph`.
3. Menulis publisher dan subscriber dengan Python (`rclpy`).
4. Membangun paket ROS 2 dengan `colcon` dan menjalankannya.
5. Menggerakkan kura-kura turtlesim dengan kode, lalu memantau posisinya.

---

## Bagian A — Cara ROS 2 berpikir

Bayangkan sebuah robot kurir:

```
 [driver_lidar] --/scan--> [penghindar_rintangan] --/cmd_vel--> [driver_motor]
                                    ^
 [driver_kamera] --/image--> [pendeteksi_aruco] --/target--/
```

| Istilah | Arti | Analogi |
|---|---|---|
| **Node** | Satu program dengan satu tugas | Satu orang di sebuah tim |
| **Topic** | "Saluran" bernama tempat data dikirim, mis. `/scan` | Grup chat dengan nama tertentu |
| **Message** | Bentuk data yang dikirim, mis. `geometry_msgs/msg/Twist` | Format pesan yang disepakati |
| **Publisher** | Node yang *mengirim* ke sebuah topic | Orang yang menulis di grup |
| **Subscriber** | Node yang *menerima* dari sebuah topic | Orang yang membaca grup |

Kenapa dipecah-pecah?
- **Mudah diganti:** driver LiDAR merek A bisa diganti merek B tanpa mengubah node lain.
- **Mudah diuji:** tiap node bisa diuji sendiri, bahkan dengan data rekaman.
- **Bisa dikerjakan tim:** anggota tim mengerjakan node yang berbeda secara paralel.
- **Simulasi = robot sungguhan:** node yang sama menerima `/scan` dari Gazebo atau dari LiDAR fisik.

Node menemukan satu sama lain secara otomatis lewat lapisan komunikasi bernama **DDS**.
Kamu tidak perlu mengatur alamat IP — cukup sepakati nama topic dan tipe pesannya.

---

## Bagian B — Menyelidiki sistem yang berjalan

Jalankan turtlesim dan teleop seperti di Modul 0, lalu buka terminal ketiga:

```bash
ros2 node list                         # node apa saja yang hidup?
ros2 topic list                        # topic apa saja yang ada?
ros2 topic info /turtle1/cmd_vel       # siapa yang mengirim & menerima?
ros2 interface show geometry_msgs/msg/Twist   # bentuk pesannya seperti apa?
ros2 topic echo /turtle1/pose          # intip data posisi secara langsung
ros2 topic hz /turtle1/pose            # berapa kali per detik dikirim?
```

Kirim perintah gerak langsung dari terminal (tanpa menulis kode):

```bash
ros2 topic pub --rate 1 /turtle1/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 2.0}, angular: {z: 1.8}}"
```

Kura-kura berputar membentuk lingkaran. Ini bukti bahwa teleop pun hanyalah
*publisher* ke `/turtle1/cmd_vel`.

Lihat gambaran sistemnya:

```bash
rqt_graph
```

### Pesan `Twist` — bahasa gerak robot

`Twist` berisi dua vektor: `linear` (m/s) dan `angular` (rad/s). Untuk robot beroda di bidang datar,
hanya dua angka yang penting:

- `linear.x` — kecepatan maju (+) atau mundur (−)
- `angular.z` — kecepatan belok ke kiri (+) atau kanan (−)

Pesan yang sama dipakai oleh robot beroda sungguhan dan oleh Nav2 di Modul 10.

### QoS secukupnya

Saat membuat publisher, angka `10` di akhir adalah **kedalaman antrean** (*QoS depth*):
berapa pesan disimpan jika penerima sedang sibuk. Untuk sekarang, 10 sudah cukup.
Pengaturan QoS lain (misalnya *reliable* vs *best effort*) dibahas saat bekerja dengan sensor.

---

## Bagian C — Workspace dan paket pertamamu

Kode ROS 2 disusun dalam **paket**, dan paket disimpan di **workspace**.

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

Kamu bisa membuat paket baru dengan:

```bash
ros2 pkg create --build-type ament_python --dependencies rclpy std_msgs nama_paket
```

Untuk kursus ini, paket contoh **`rtl_dasar`** sudah tersedia di repo. Hubungkan ke workspace-mu:

```bash
ln -s ~/robotika-tanpa-lab/course/kode/rtl_dasar ~/ros2_ws/src/rtl_dasar
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

> 💡 `--symlink-install` membuat perubahan berkas Python langsung berlaku tanpa *build* ulang.
> Tetapi jika kamu **menambah node baru** di `setup.py`, jalankan `colcon build` lagi.
>
> 💡 Setiap membuka terminal baru, jalankan `source ~/ros2_ws/install/setup.bash`
> (atau tambahkan ke `~/.bashrc` setelah baris ROS 2).

Isi paket:

```
rtl_dasar/
├── package.xml          # identitas paket & dependensi
├── setup.py             # daftar node yang bisa dijalankan (entry_points)
├── setup.cfg
├── resource/rtl_dasar
└── rtl_dasar/
    ├── penerbit_halo.py     # publisher
    ├── pelanggan_halo.py    # subscriber
    ├── kura_persegi.py      # menggambar persegi
    ├── kura_spiral.py       # menggambar spiral
    └── pemantau_kura.py     # memantau posisi
```

---

## Bagian D — Publisher dan subscriber pertama

Buka `rtl_dasar/penerbit_halo.py`. Inti kodenya:

```python
class PenerbitHalo(Node):
    def __init__(self):
        super().__init__('penerbit_halo')                              # 1. beri nama node
        self.penerbit = self.create_publisher(String, 'sapaan', 10)     # 2. buat publisher
        self.create_timer(1.0, self.kirim)                             # 3. panggil kirim() tiap 1 detik

    def kirim(self):
        pesan = String()
        pesan.data = f'Halo dari Lab Robotika Tanpa Lab! #{self.hitungan}'
        self.penerbit.publish(pesan)                                   # 4. kirim!
```

Dan `pelanggan_halo.py`:

```python
self.create_subscription(String, 'sapaan', self.terima, 10)

def terima(self, pesan):        # dipanggil otomatis setiap ada pesan baru
    self.get_logger().info(f'Terima: "{pesan.data}"')
```

Jalankan di dua terminal:

```bash
ros2 run rtl_dasar penerbit_halo
ros2 run rtl_dasar pelanggan_halo
```

Coba eksperimen ini:
1. Jalankan **dua** subscriber sekaligus. Apakah keduanya menerima? (Ya — satu topic bisa punya banyak penerima.)
2. Matikan publisher lalu nyalakan lagi. Apa yang terjadi pada subscriber?
3. Ganti nama topic di salah satu berkas saja. Kenapa pesannya tidak sampai lagi?

### Bagian penting dari setiap node

- `rclpy.init()` — menyalakan ROS 2 di program ini.
- `rclpy.spin(node)` — menjaga node tetap hidup dan memproses timer serta callback.
- *Callback* — fungsi yang **dipanggil oleh ROS 2**, bukan olehmu. Callback harus selesai
  dengan cepat; jangan memakai `time.sleep()` panjang di dalamnya.

---

## Bagian E — Menggerakkan kura-kura dengan kode

```bash
ros2 run turtlesim turtlesim_node
ros2 run rtl_dasar kura_persegi
```

`kura_persegi` bergantian antara dua fase: **maju** selama `panjang_sisi / kecepatan` detik,
lalu **belok** 90° selama `(π/2) / kecepatan_belok` detik, sebanyak 4 kali.

Ubah ukurannya tanpa mengubah kode, memakai **parameter**:

```bash
ros2 run rtl_dasar kura_persegi --ros-args -p panjang_sisi:=3.0
```

Perhatikan hasilnya: **persegi tidak menutup dengan sempurna**. Inilah keterbatasan
kendali **loop terbuka** — robot hanya mengandalkan waktu dan tidak mengecek posisinya.
Galat kecil di setiap belokan menumpuk. Robot sungguhan mengalami hal yang sama, bahkan
lebih parah karena roda bisa selip.

Solusinya adalah kendali **loop tertutup**: membaca posisi (umpan balik), lalu terus mengoreksi.
Langkah pertamanya — membaca posisi — ada di `pemantau_kura`:

```bash
ros2 run rtl_dasar pemantau_kura
```

Node ini berlangganan `/turtle1/pose` dan memberi peringatan saat kura-kura terlalu dekat
dengan dinding. Menggabungkan pembacaan posisi dengan perintah gerak adalah tantangan di Latihan 02.

---

## Latihan

Kerjakan **[Latihan 02 — Kura-kura Otonom](../latihan/02-turtlesim/)**.

## Kuis singkat

1. Apa perbedaan node dan topic?
2. Topic `/turtle1/cmd_vel` memakai tipe pesan apa? Field mana yang mengatur kecepatan maju?
3. Perintah apa untuk melihat isi pesan di sebuah topic secara langsung?
4. Bisakah satu topic memiliki lebih dari satu subscriber? Lebih dari satu publisher?
5. Kenapa persegi dari `kura_persegi` tidak menutup sempurna?
6. Kapan kamu perlu menjalankan `colcon build` lagi meskipun sudah memakai `--symlink-install`?
7. Kenapa callback tidak boleh berisi `time.sleep(5)`?

<details><summary>Kunci jawaban</summary>

1. Node adalah program dengan satu tugas; topic adalah saluran bernama tempat node bertukar data.
2. `geometry_msgs/msg/Twist`; `linear.x`.
3. `ros2 topic echo <nama_topic>`.
4. Ya untuk keduanya.
5. Kendali loop terbuka: hanya mengandalkan waktu tanpa umpan balik posisi, sehingga galat menumpuk.
6. Saat menambah node baru di `setup.py` atau mengubah `package.xml`/berkas non-Python.
7. Selama callback berjalan, node tidak bisa memproses pesan atau timer lain — robot jadi "beku".
</details>
