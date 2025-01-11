#!/usr/bin/env python2

import rospy
from std_msgs.msg import String

def event_callback(msg):
    # 处理接收到的消息
    rospy.loginfo("接收到消息: %s", msg.data)

def event_triggered_subscriber():
    # 初始化节点
    rospy.init_node('event_triggered_subscriber', anonymous=True)

    # 创建一个 Subscriber，订阅 /event_topic
    rospy.Subscriber('/event_topic', String, event_callback)

    # 循环等待消息
    rospy.spin()

if __name__ == '__main__':
    try:
        event_triggered_subscriber()
    except rospy.ROSInterruptException:
        pass
