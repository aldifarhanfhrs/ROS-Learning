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

def go_to_goal(goal_publisher, x_goal, y_goal):
    global x, y, theta
    goal_message = Twist()
    #distance = 0.0
    rate = rospy.Rate(4)
    while True:
        kp_linear = 0.5
        distance_moved = abs(math.sqrt((x_goal - x)**2 + (y_goal - y)**2))
        linear_speed = distance_moved * kp_linear

        kp_angular = 4.0
        angular_moved = math.atan2(y_goal-y, x_goal-x)
        angular_speed = (angular_moved - theta) * kp_angular

        goal_message.linear.x = linear_speed
        goal_message.angular.z = angular_speed

        goal_publisher.publish(goal_message)
        print('x: {:.3f} \t y: {:.3f} \t theta: {:.3f} \t distance: {:.2f}'.format(x, y, theta, distance_moved))
        #print()
        rate.sleep()
        
        if distance_moved < 0.01:
            rospy.loginfo('Target Reached')
            #goal_message.linear.x = 0
            #goal_message.angular.z = 0
            #goal_publisher.publish(goal_message)
            break

if __name__ == '__main__':
    try:
        rospy.init_node('turtlesim_gotoGoal_pose', anonymous=True)

        goal_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        goal_subscriber = rospy.Subscriber('/turtle1/pose', Pose, pose_callback)

        time.sleep(1)

        go_to_goal(goal_publisher, 10.0, 1.0 )

    except rospy.ROSInterruptException:
        rospy.loginfo('Node Terminated')


