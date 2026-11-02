"""
Modul 2 — Publisher pertama.

Node ini mengirim pesan teks ke topic `/sapaan` setiap 1 detik.

Jalankan:
    ros2 run rtl_dasar penerbit_halo
Lihat pesannya dari terminal lain:
    ros2 topic echo /sapaan
"""
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String


class PenerbitHalo(Node):
    def __init__(self):
        super().__init__('penerbit_halo')
        # create_publisher(tipe pesan, nama topic, kedalaman antrean QoS)
        self.penerbit = self.create_publisher(String, 'sapaan', 10)
        self.hitungan = 0
        # Timer memanggil self.kirim setiap 1.0 detik
        self.create_timer(1.0, self.kirim)

    def kirim(self):
        pesan = String()
        pesan.data = f'Halo dari Lab Robotika Tanpa Lab! #{self.hitungan}'
        self.penerbit.publish(pesan)
        self.get_logger().info(f'Kirim: "{pesan.data}"')
        self.hitungan += 1


def main(args=None):
    rclpy.init(args=args)
    node = PenerbitHalo()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
