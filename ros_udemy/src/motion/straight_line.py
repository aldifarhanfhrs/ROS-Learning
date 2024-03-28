#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time

def pose_callback(data):
    global x, y, yaw
    
    x = data.x
    y = data.y
    yaw = data.theta

def move(velocity_publisher, speed, distance, is_forward):
    global x, y
    velocity_message = Twist()

    x0 = x
    y0 = y

    distance_moved = 0.0
    rate = rospy.Rate(5)

    if is_forward:
        velocity_message.linear.x = abs(speed)
    else:
        velocity_message.linear.x = -abs(speed)

    while True:
        velocity_publisher.publish(velocity_message)

        distance_moved = math.sqrt(abs((x - x0)**2 + (y - y0)**2))
        rate.sleep()
        print('Pose x, y: {}, {}'.format(x, y))
        print()

        if distance_moved >= distance:
            rospy.loginfo('Target Reached')
            velocity_message.linear.x = 0
            velocity_publisher.publish(velocity_message)
            break
if __name__ == '__main__':
    try:
        rospy.init_node('turtlesim_velocity_pose', anonymous= True)

        velocity_publisher = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)
        velocity_subscriber = rospy.Subscriber('turtle1/pose', Pose, pose_callback)
        time.sleep(1)

        move(velocity_publisher, 1.0, 4.5, True)

    except rospy.ROSInterruptException:
        rospy.loginfo('Node Interupted')