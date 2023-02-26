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

    from_control = MinimalSubscriber('control_comms')
    to_control = MinimalPublisher('comms_control')
    from_sensors = MinimalSubscriber('sensors_comms')
    to_sensors = MinimalPublisher('comms_sensors')

    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(from_control)
    executor.add_node(to_control)
    executor.add_node(from_sensors)
    executor.add_node(to_sensors)
    
    executor.spin()
    
    rclpy.shutdown()


if __name__ == '__main__':
    main()
