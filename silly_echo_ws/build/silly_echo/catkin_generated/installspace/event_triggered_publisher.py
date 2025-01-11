#!/usr/bin/env python2
import rospy
from std_msgs.msg import String

def my_node():
    rospy.init_node('my_node', anonymous=True)
    pub = rospy.Publisher('my_topic', String, queue_size=10)
    rate = rospy.Rate(1)  # 1Hz
    while not rospy.is_shutdown():
        message = "Hello, ROS!"
        rospy.loginfo(message)
        ros_message = String()
        ros_message.data = message
        pub.publish(ros_message)
        rate.sleep()

if __name__ == '__main__':
    try:
        my_node()
    except rospy.ROSInterruptException:
        pass
