#!/user/bin/env python

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

def spiral(spiral_publisher, wk, rk):
    spiral_message = Twist()
    