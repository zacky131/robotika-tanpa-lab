"""
Modul 2 — Memantau posisi kura-kura.

Node ini berlangganan topic `/turtle1/pose`, mencetak posisi setiap 1 detik,
dan memberi peringatan jika kura-kura terlalu dekat ke dinding arena.
Arena turtlesim berukuran sekitar 11 x 11 (koordinat 0 sampai ~11.1).

Jalankan bersama kura_persegi atau kura_spiral:
    ros2 run rtl_dasar pemantau_kura
"""
import math

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from turtlesim.msg import Pose

BATAS_ARENA = 11.08


class PemantauKura(Node):
    def __init__(self):
        super().__init__('pemantau_kura')
        self.declare_parameter('jarak_aman', 1.0)
        self.create_subscription(Pose, '/turtle1/pose', self.terima_pose, 10)

    def terima_pose(self, pose):
        jarak_aman = self.get_parameter('jarak_aman').value
        jarak_ke_dinding = min(pose.x, pose.y, BATAS_ARENA - pose.x, BATAS_ARENA - pose.y)

        self.get_logger().info(
            f'x={pose.x:5.2f}  y={pose.y:5.2f}  arah={math.degrees(pose.theta):6.1f}°',
            throttle_duration_sec=1.0)

        if jarak_ke_dinding < jarak_aman:
            self.get_logger().warn(
                f'Awas! Jarak ke dinding tinggal {jarak_ke_dinding:.2f}',
                throttle_duration_sec=1.0)


def main(args=None):
    rclpy.init(args=args)
    node = PemantauKura()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
