"""Modul 2 — Subscriber pertama.

Node ini mendengarkan topic `/sapaan` dan mencetak setiap pesan yang masuk.

Jalankan (setelah penerbit_halo berjalan):
    ros2 run rtl_dasar pelanggan_halo
"""
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String


class PelangganHalo(Node):
    def __init__(self):
        super().__init__('pelanggan_halo')
        # create_subscription(tipe pesan, nama topic, fungsi callback, kedalaman antrean)
        self.create_subscription(String, 'sapaan', self.terima, 10)
        self.jumlah_diterima = 0

    def terima(self, pesan):
        # Fungsi ini dipanggil otomatis setiap ada pesan baru di /sapaan
        self.jumlah_diterima += 1
        self.get_logger().info(f'Terima ({self.jumlah_diterima}): "{pesan.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = PelangganHalo()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
