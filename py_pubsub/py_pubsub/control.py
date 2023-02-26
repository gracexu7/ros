import rclpy
from rclpy.node import Node
from rclpy.executors import Executor, MultiThreadedExecutor

from std_msgs.msg import String


class MinimalPublisher(Node):

    def __init__(self, topic):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, topic, 10)
        timer_period = 1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'control %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

class MinimalSubscriber(Node):

    def __init__(self, topic):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            topic,
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    from_motors = MinimalSubscriber('motors_control')
    to_motors = MinimalPublisher('control_motors')
    from_sensors = MinimalSubscriber('sensors_control')
    to_comms = MinimalPublisher('control_comms')
    from_comms = MinimalSubscriber('comms_control')

    executor = MultiThreadedExecutor(num_threads=5)
    executor.add_node(from_motors)
    executor.add_node(to_motors)
    executor.add_node(from_sensors)
    executor.add_node(to_comms)
    executor.add_node(from_comms)
    
    executor.spin()
    
    rclpy.shutdown()


if __name__ == '__main__':
    main()
