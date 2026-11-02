"""Latihan 02 — SOLUSI TANTANGAN: persegi dengan kendali loop tertutup.

Berbeda dengan kura_persegi (loop terbuka, hanya mengandalkan waktu), node ini
membaca posisi kura-kura dari /turtle1/pose dan terus mengoreksi arah dan jarak
menuju setiap sudut persegi. Hasilnya: persegi yang jauh lebih rapi.

Cara menjalankan (tanpa perlu dimasukkan ke paket):
    ros2 run turtlesim turtlesim_node
    python3 kura_persegi_tertutup.py
"""
import math

import rclpy
from geometry_msgs.msg import Twist
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from turtlesim.msg import Pose

TOLERANSI_JARAK = 0.05     # dianggap sampai jika sedekat ini ke sudut
TOLERANSI_SUDUT = 0.02     # rad; di atas ini, putar dulu sebelum maju
KP_MAJU = 1.5              # penguat kendali proporsional
KP_BELOK = 4.0


def normalisasi_sudut(sudut):
    """Membuat sudut berada di rentang [-pi, pi]."""
    return math.atan2(math.sin(sudut), math.cos(sudut))


class KuraPersegiTertutup(Node):
    def __init__(self):
        super().__init__('kura_persegi_tertutup')
        self.declare_parameter('panjang_sisi', 3.0)
        self.penerbit = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.create_subscription(Pose, '/turtle1/pose', self.terima_pose, 10)
        self.pose = None
        self.titik_sudut = []   # daftar titik sudut persegi (dibuat dari pose awal)
        self.indeks = 0
        self.create_timer(0.05, self.langkah)

    def terima_pose(self, pose):
        if self.pose is None:
            # Persegi dibuat relatif terhadap posisi awal kura-kura
            s = self.get_parameter('panjang_sisi').value
            x0, y0 = pose.x, pose.y
            self.titik_sudut = [(x0 + s, y0), (x0 + s, y0 + s), (x0, y0 + s), (x0, y0)]
            self.get_logger().info(f'Target sudut: {self.titik_sudut}')
        self.pose = pose

    def langkah(self):
        if self.pose is None:
            return  # belum ada data posisi

        perintah = Twist()
        if self.indeks >= len(self.titik_sudut):
            self.penerbit.publish(perintah)
            self.get_logger().info('Persegi (loop tertutup) selesai!', once=True)
            return

        tx, ty = self.titik_sudut[self.indeks]
        dx, dy = tx - self.pose.x, ty - self.pose.y
        jarak = math.hypot(dx, dy)
        galat_sudut = normalisasi_sudut(math.atan2(dy, dx) - self.pose.theta)

        if jarak < TOLERANSI_JARAK:
            self.get_logger().info(f'Sampai di sudut {self.indeks + 1}')
            self.indeks += 1
        elif abs(galat_sudut) > TOLERANSI_SUDUT:
            perintah.angular.z = KP_BELOK * galat_sudut          # putar di tempat
        else:
            perintah.linear.x = min(KP_MAJU * jarak, 2.0)         # maju, melambat saat dekat
            perintah.angular.z = KP_BELOK * galat_sudut          # koreksi kecil sambil jalan

        self.penerbit.publish(perintah)


def main(args=None):
    rclpy.init(args=args)
    node = KuraPersegiTertutup()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
