import rclpy
from rclpy.node import Node
import time
from std_msgs.msg import String,  Int64MultiArray

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
             String,
            'topic',
            self.listener_callback,
             0)
        self.subscription  # prevent unused variable warning
    
    def listener_callback(self, msg):
        print(msg.data)


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()