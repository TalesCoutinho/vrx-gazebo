import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener, Buffer
from transforms3d.euler import quat2euler

class TestTF(Node):
    def __init__(self):
        super().__init__('test_tf')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.timer = self.create_timer(1.0, self.check_tf)

    def check_tf(self):
        for target_frame in ['map', 'odom']:
            try:
                trans = self.tf_buffer.lookup_transform(target_frame, 'wamv/wamv/base_link', rclpy.time.Time())
                x = trans.transform.translation.x
                y = trans.transform.translation.y
                q = trans.transform.rotation
                euler = quat2euler([q.w, q.x, q.y, q.z])
                yaw = euler[2]
                self.get_logger().info(f'Frame: {target_frame} -> X: {x:.2f}, Y: {y:.2f}, Yaw: {yaw:.2f}')
            except Exception as e:
                pass

def main():
    rclpy.init()
    node = TestTF()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
