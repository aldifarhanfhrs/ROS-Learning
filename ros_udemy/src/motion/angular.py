#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time

def pose_callback(data):
    global x, y, theta
    x = data.x
    y = data.y
    theta = data.theta

def angular(angular_publisher, angular_speed_degree, relative_degree, clockwise):
    angular_message = Twist()
    angular_speed = math.radians(abs(angular_speed_degree))

    if clockwise:
        angular_message.angular.z = abs(angular_speed)
    else:
        angular_message.angular.z = -abs(angular_speed)

    loop_rate = rospy.Rate(10)
    t0 = rospy.Time.now().to_sec()

    while True:
        angular_publisher.publish(angular_message)
        
        t1 = rospy.Time.now().to_sec()
        current_angle_degree = (t1 - t0) * angular_speed_degree
        loop_rate.sleep()

        print('Pose Theta: {}'.format(theta))
        print('Current Angular Degree: {}'.format(current_angle_degree))
        print()

        if current_angle_degree >= relative_degree:
            rospy.loginfo('Angle Reached')
            angular_message.angular.z = 0
            angular_publisher.publish(angular_message)
            break

if __name__ == '__main__':
    try:
        rospy.init_node('turtlesim_angular_pose', anonymous= True)

        publisher_topic = '/turtle1/cmd_vel'
        angular_publisher = rospy.Publisher(publisher_topic, Twist, queue_size= 10)

        subscriber_topic = '/turtle1/pose'
        angular_subscriber = rospy.Subscriber(subscriber_topic, Pose, pose_callback)
        #time.sleep()

        angular(angular_publisher, 10.0, 90.0, True)
    except rospy.ROSInterruptException:
        rospy.loginfo('Node Terminated!')





