#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def steve_callback(message):
    rospy.loginfo(" WOOOOOO %s", message.data)

def steve_subscriber():
    rospy.init_node('steve_node', anonymous=True)
    rospy.Subscriber('conversation', String, steve_callback)
    rospy.spin()

if __name__ == '__main__':
    steve_subscriber()
