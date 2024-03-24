#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def dusting_calling():
    rospy.init_node('dustin_node', anonymous=True)
    pub = rospy.Publisher('conversation', String, queue_size=10)
    rate = rospy.Rate(5)

    i = 0
    while not rospy.is_shutdown():
        message = "Hello Steve {}".format(i)
        rospy.loginfo(message)
        pub.publish(message)
        rate.sleep()
        i += 1

if __name__ == '__main__':
    try:
        dusting_calling()
    except rospy.ROSInterruptException:
        pass
