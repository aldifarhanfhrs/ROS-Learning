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

def move(velocity_publisher, speed, distance, isForward):
    global x, y
    velocity_message = Twist()

    x0 = x
    y0 = y
    distance_moved = 0.0
    rate = rospy.Rate(5)

    if isForward:
        velocity_message.linear.x = abs(speed)
    else:
        velocity_message.linear.x = -abs(speed)
    
    while True:
        velocity_publisher.publish(velocity_message)
        rate.sleep()

        distance_moved = math.sqrt((x - x0)**2 + (y - y0)**2)
        print('Current Angle: {}'.format(distance_moved))
        print('Pose X, Y, Theta: {},  {},  {}'.format(x, y, theta))
        print()

        if distance_moved >= distance:
            rospy.loginfo('Posisi Akhir Robot Tercapai')
            velocity_message.linear.x = 0
            velocity_publisher.publish(velocity_message)
            break

def angular(rotate_publisher, angular_speed_degree, ralative_angle_degree, is_clockwise):
    angular_message = Twist()
    angular_speed = math.radians(abs(angular_speed_degree))

    rate = rospy.Rate(5)
    t0 = rospy.Time.now().to_sec()
    current_angle_degree = 0

    if is_clockwise:
        angular_message.angular.z = abs(angular_speed)
    else:
        angular_message.angular.z = -abs(angular_speed)

    while True:
        rotate_publisher.publish(angular_message)

        t1 = rospy.Time.now().to_sec()
        current_angle_degree = (t1 - t0) * angular_speed_degree
        rate.sleep()

        print('Current Angle: {}'.format(current_angle_degree))
        print('Pose Theta: {}'.format(theta))
        print()
        
        if current_angle_degree >= ralative_angle_degree:
            angular_message.angular.z = 0
            rotate_publisher.publish(angular_message)
            rospy.loginfo('Rotasi Tercapai')
            break

def goto_goal(goal_publisher, x_goal, y_goal):
    global x, y, theta
    goal_message = Twist()

    while True:
        kp_linear = 0.5
        distance = math.sqrt((x_goal - x)**2 + (y_goal - y)**2)
        linear_speed = distance * kp_linear

        kp_angular = 3.5
        desired_angel_goal = math.atan2(y_goal - y, x_goal - x)
        angular_speed = (desired_angel_goal-theta) * kp_angular

        goal_message.linear.x = linear_speed
        goal_message.angular.z = angular_speed

        goal_publisher.publish(goal_message)
        print('x: {} \t y: {} \t theta: {}')
        print()
        rospy.Rate(5).sleep()

        if distance < 0.001:
            rospy.loginfo('Target Reached')
            break
    
def setDesiredOrientation(desired_publisher, speed_in_degree, desired_angle_degree):
    relative_angle_radians = math.radians(desired_angle_degree) - theta
    clockwise = 0

    if relative_angle_radians < 0:
        clockwise = 1
    else:
        clockwise = 0
    
    print('relative angle radians: {}'.format(math.degrees(relative_angle_radians)))
    print('desired angle degree:'.format(desired_angle_degree))

    angular(desired_publisher, speed_in_degree.math, math.degrees(abs(relative_angle_radians)))

def spiral(spiral_publisher, wk, rk):
    spiral_message = Twist()
    rate = rospy.Rate(1)

    while x < 10.5 and y < 10.5:
        rk = rk + 1
        spiral_message.linear.x = rk
        spiral_message.linear.y = 0
        spiral_message.linear.z = 0
        spiral_message.angular.x = 0
        spiral_message.angular.y = 0
        spiral_message.angular.z = wk

        spiral_publisher.publish(spiral_message)
        rate.sleep()
    spiral_message.linear.x = 0
    spiral_message.angular.z = 0
    spiral_publisher.publish(spiral_message)

def grid_cleaning(cleaning_publisher):
    Pose().x = 1
    Pose().y = 1
    Pose().theta = 0

    goto_goal(cleaning_publisher, 1.0, 1.0)
    setDesiredOrientation(cleaning_publisher, 30, math.radians(Pose().theta))

    for i in range(5):
        move(cleaning_publisher, 2.0, 1.0, True)
        angular(cleaning_publisher, 2.0, 9.0, False)
        move(cleaning_publisher, 2.0, 9.0, True)
        angular(cleaning_publisher, 2.0, 9.0, True)
        move(cleaning_publisher, 2.0, 1.0, True)
        angular(cleaning_publisher, 2.0, 9.0, True)
        move(cleaning_publisher, 2.0, 9.0, True)
        angular(cleaning_publisher, 2.0, 9.0, False)
    pass

if __name__ == '__main__':
    try:
        rospy.init_node('turtlesim_motion_pose', anonymous= True)

        publisher_topic = '/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(publisher_topic, Twist, queue_size=10)
        rotate_publisher = rospy.Publisher(publisher_topic, Twist, queue_size=10)
        subscriber_topic = '/turtle1/pose'
        rospy.Subscriber(subscriber_topic, Pose, pose_callback)

        time.sleep(3)

        move(velocity_publisher, 1.0, 4.5, False)
        angular(rotate_publisher, 20.0, 180, False)

    except rospy.ROSInterruptException:
        rospy.loginfo('Node Terminated')
