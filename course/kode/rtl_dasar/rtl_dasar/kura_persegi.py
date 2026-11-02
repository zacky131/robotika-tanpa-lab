"""Modul 2 — Menggambar persegi dengan turtlesim (kendali loop terbuka).

Kura-kura maju selama waktu tertentu, lalu berbelok 90 derajat, diulang 4 kali.
Ini disebut *loop terbuka*: robot tidak mengecek posisinya sendiri, hanya
mengandalkan waktu. Perhatikan: persegi hasilnya tidak sempurna. Kenapa?
(Jawabannya dibahas di modul dan di tantangan Latihan 02.)

Jalankan:
    ros2 run turtlesim turtlesim_node
    ros2 run rtl_dasar kura_persegi
Ubah ukuran persegi lewat parameter:
    ros2 run rtl_dasar kura_persegi --ros-args -p panjang_sisi:=3.0
"""
import math

import rclpy
from geometry_msgs.msg import Twist
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class KuraPersegi(Node):
    def __init__(self):
        super().__init__('kura_persegi')
        self.declare_parameter('panjang_sisi', 2.0)       # meter (satuan turtlesim)
        self.declare_parameter('kecepatan_maju', 1.0)     # m/s
        self.declare_parameter('kecepatan_belok', math.pi / 4)  # rad/s

        self.penerbit = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.fase = 'maju'          # 'maju' atau 'belok'
        self.sisi_selesai = 0
        self.mulai_fase = self.waktu_sekarang()
        self.create_timer(0.05, self.langkah)  # 20 Hz
        self.get_logger().info('Mulai menggambar persegi...')

    def waktu_sekarang(self):
        return self.get_clock().now().nanoseconds * 1e-9

    def langkah(self):
        sisi = self.get_parameter('panjang_sisi').value
        v = self.get_parameter('kecepatan_maju').value
        w = self.get_parameter('kecepatan_belok').value

        perintah = Twist()

        if self.sisi_selesai >= 4:
            self.penerbit.publish(perintah)  # semua nol -> berhenti
            self.get_logger().info('Persegi selesai!', once=True)
            return

        lama = self.waktu_sekarang() - self.mulai_fase

        if self.fase == 'maju':
            perintah.linear.x = v
            if lama >= sisi / v:
                self.ganti_fase('belok')
        else:
            perintah.angular.z = w
            if lama >= (math.pi / 2) / w:
                self.sisi_selesai += 1
                self.get_logger().info(f'Sisi ke-{self.sisi_selesai} selesai')
                self.ganti_fase('maju')

        self.penerbit.publish(perintah)

    def ganti_fase(self, fase_baru):
        self.fase = fase_baru
        self.mulai_fase = self.waktu_sekarang()


def main(args=None):
    rclpy.init(args=args)
    node = KuraPersegi()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
