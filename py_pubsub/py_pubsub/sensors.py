import rclpy
from rclpy.node import Node
from rclpy.executors import Executor, MultiThreadedExecutor

from std_msgs.msg import String


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'comms_sensors',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

class MinimalPublisher(Node):

    def __init__(self, topic):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, topic, 10)
        timer_period = 1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'sensors %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)

    tocontrol = MinimalPublisher('sensors_control')
    tocomms = MinimalPublisher('sensors_comms')
    minimal_subscriber = MinimalSubscriber()

    executor = MultiThreadedExecutor(num_threads=3)
    executor.add_node(tocontrol)
    executor.add_node(tocomms)
    executor.add_node(minimal_subscriber)

    executor.spin()
    
    rclpy.shutdown()


if __name__ == '__main__':
    main()
