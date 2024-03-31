#!/usr/bin/env python3

import sys
import rospy
from ros_essentials_cpp.srv import AddTwoInts
from ros_essentials_cpp.srv import AddTwoIntsRequest
from ros_essentials_cpp.srv import AddTwoIntsResponse

def add_two_ints_client(x, y):
    rospy.wait_for_service('add_two_ints')
    try:
        add_two_ints = rospy.ServiceProxy('add_two_ints', AddTwoInts)
        response = add_two_ints(x, y)
        return response.sum
    except rospy.ServiceException as e:
        print('Service Failed: ', e)

def usage():
    Usage = 'Usage: {} [x y]'.format(sys.argv[0])
    return Usage

if __name__ == "__main__":  
    if len(sys.argv) == 3:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
    else:
        print(usage())
        sys.exit()

    print('Requesting: {} + {}:'.format(x, y))
    server = add_two_ints_client(x, y)
    print("{} + {} = {}".format(x, y, server))