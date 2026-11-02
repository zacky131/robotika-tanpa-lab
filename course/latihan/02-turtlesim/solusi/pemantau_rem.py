"""Latihan 02 — SOLUSI TUGAS 4b: rem darurat sebagai *filter keselamatan*.

Node ini menjadi SATU-SATUNYA publisher ke /turtle1/cmd_vel. Perintah gerak dari
node lain masuk lewat /cmd_vel_mentah, lalu diteruskan hanya jika kura-kura masih
jauh dari dinding. Begitu terlalu dekat, rem terkunci dan kura-kura berhenti.

Cara menjalankan (tanpa perlu dimasukkan ke paket):
    ros2 run turtlesim turtlesim_node
    python3 pemantau_rem.py
    ros2 run rtl_dasar kura_spiral --ros-args -r /turtle1/cmd_vel:=/cmd_vel_mentah \
        -p kecepatan_belok:=1.0 -p pertambahan:=0.3 -p durasi:=30.0
"""
from geometry_msgs.msg import Twist
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from turtlesim.msg import Pose

BATAS_ARENA = 11.08


class PemantauRem(Node):
    def __init__(self):
        super().__init__('pemantau_rem')
        self.declare_parameter('jarak_rem', 0.5)
        self.penerbit = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.create_subscription(Pose, '/turtle1/pose', self.terima_pose, 10)
        self.create_subscription(Twist, '/cmd_vel_mentah', self.terima_perintah, 10)
        self.rem_aktif = False

    def terima_pose(self, pose):
        jarak_ke_dinding = min(pose.x, pose.y, BATAS_ARENA - pose.x, BATAS_ARENA - pose.y)
        if not self.rem_aktif and jarak_ke_dinding < self.get_parameter('jarak_rem').value:
            self.rem_aktif = True
            self.penerbit.publish(Twist())  # langsung berhenti, jangan tunggu perintah berikutnya
            self.get_logger().warn(f'REM DARURAT! Jarak ke dinding {jarak_ke_dinding:.2f}')

    def terima_perintah(self, perintah):
        if self.rem_aktif:
            perintah = Twist()  # semua nol -> berhenti
        self.penerbit.publish(perintah)


def main(args=None):
    rclpy.init(args=args)
    node = PemantauRem()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
