"""Modul 2 — Menggambar spiral dengan turtlesim.

Kecepatan belok dibuat tetap, sedangkan kecepatan maju bertambah sedikit demi
sedikit. Hasilnya: lingkaran yang makin lama makin besar (spiral).

Jalankan:
    ros2 run turtlesim turtlesim_node
    ros2 run rtl_dasar kura_spiral
"""
import rclpy
from geometry_msgs.msg import Twist
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class KuraSpiral(Node):
    def __init__(self):
        super().__init__('kura_spiral')
        self.declare_parameter('kecepatan_belok', 2.0)   # rad/s, tetap
        self.declare_parameter('kecepatan_awal', 0.2)    # m/s
        self.declare_parameter('pertambahan', 0.15)      # m/s per detik
        self.declare_parameter('durasi', 12.0)           # detik

        self.penerbit = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.mulai = self.get_clock().now()
        self.create_timer(0.05, self.langkah)

    def langkah(self):
        t = (self.get_clock().now() - self.mulai).nanoseconds * 1e-9
        perintah = Twist()

        if t < self.get_parameter('durasi').value:
            perintah.linear.x = (self.get_parameter('kecepatan_awal').value
                                 + self.get_parameter('pertambahan').value * t)
            perintah.angular.z = self.get_parameter('kecepatan_belok').value
        else:
            self.get_logger().info('Spiral selesai!', once=True)

        self.penerbit.publish(perintah)


def main(args=None):
    rclpy.init(args=args)
    node = KuraSpiral()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
