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
    global x, y, theta
    angular_message = Twist()

    t0 = rospy.Time.now().to_sec()
    angular_speed_radians = math.radians(abs(angular_speed_degree))
    rate = rospy.Rate(5)

    if clockwise:
        angular_message.angular.z = abs(angular_speed_radians)
    else:
        angular_message.angular.z = -abs(angular_speed_radians)

    while True:
        angular_publisher.publish(angular_message)

        t1 = rospy.Time.now().to_sec()
        current_angular_degree = (t1 - t0) * angular_speed_degree
        rate.sleep()
        print('Theta: {} \t Current Angle: {}'.format(theta, current_angular_degree))

        if not current_angular_degree < relative_degree:
            rospy.loginfo('Angle Reached')
            angular_message.angular.z = 0
            angular_publisher.publish(angular_message)
            break

def desired_orientation(orientation_publisher, speed_in_degree, desired_angle_degree):
    relative_angle_radians = math.radians(desired_angle_degree - theta)
    clockwise = 0
    if relative_angle_radians < 0:
        clockwise = 1
    else: 
        clockwise = 0
    
    print('Relative Angle Radians: {}'.format(math.degrees(relative_angle_radians)))
    print('Desired Angle Degree: {}'.format(desired_angle_degree))
    angular(orientation_publisher, speed_in_degree, math.degrees(abs(relative_angle_radians)), clockwise)


if __name__ == '__main__':
    try:
        rospy.init_node('turtlesim_angular_pose', anonymous= True)
        angular_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        orientation_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/turtle1/pose', Pose, pose_callback)

        time.sleep(2)
        angular(angular_publisher, 45.0, 180.0, True)
        #desired_orientation(orientation_publisher, 45.0, 180.0)

    except rospy.ROSInterruptException:
        rospy.loginfo('Node Terminated!')

