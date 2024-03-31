#!/usr/bin/env python3

import rospy
from ros_essentials_cpp.srv import AddTwoInts
from ros_essentials_cpp.srv import AddTwoIntsRequest
from ros_essentials_cpp.srv import AddTwoIntsResponse


def add_two_ints_server():
    rospy.init_node('add_two_inst_server_node')
    server = rospy.Service('add_two_ints', AddTwoInts, handle_add_two_ints)
    print('ready to add two ints')
    rospy.spin()

def handle_add_two_ints(req):
    print("Returning [{} + {} = {}]".format(req.a, req.b, (req.a + req.b)))
    return AddTwoIntsResponse(req.a + req.b)


if __name__ == "__main__":
    add_two_ints_server()