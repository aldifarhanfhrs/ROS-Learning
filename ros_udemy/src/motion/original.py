#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time

# Variabel global untuk posisi robot
x = 0.0
y = 0.0
yaw = 0.0

def pose_callback(pose_message):
    global x, y, yaw
    
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta

def move(velocity_publisher, speed, distance, is_forward):
    global x, y, yaw
    velocity_message = Twist()

    x0 = x
    y0 = y
    distance_moved = 0.0
    loop_rate = rospy.Rate(10)

    while True:
        if is_forward:
            velocity_message.linear.x = abs(speed)
        else:
            velocity_message.linear.x = -abs(speed)
        
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()

        # Hitung jarak yang telah ditempuh
        distance_moved = math.sqrt((x - x0)**2 + (y - y0)**2)

        if distance_moved >= distance:
            rospy.loginfo('Target Reached')
            break
    
    # Berhenti
    velocity_message.linear.x = 0
    velocity_publisher.publish(velocity_message)

if __name__ == '__main__':
    try:
        rospy.init_node('turtlesim_motion_pose_node', anonymous=True)
        cmd_vel_topic = '/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
        
        position_topic = '/turtle1/pose'
        pose_subscriber = rospy.Subscriber(position_topic, Pose, pose_callback)
        
        # Tunggu hingga mendapatkan posisi awal
        rospy.loginfo("Wait for the first message")
        while x == 0.0 and y == 0.0:
            rospy.sleep(0.1)
        
        move(velocity_publisher, 1.0, 4.0, True)
        
    except rospy.ROSInterruptException:
        rospy.loginfo('Node terminated')
