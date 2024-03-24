#!/usr/bin/env python

from ros_udemy.srv import times_three_int
from ros_udemy.srv import times_three_intRequest
from ros_udemy.srv import times_three_intResponse
import time
import rospy

def handle_times_three_int(req):
    times = req.x * req.y * req.z 
    print("Hasil dari {}*{}*{} adalah {}".format(req.x, req.y, req.z, times))
    response = times_three_intResponse(times)
    return response

def times_three_int_server():
    print("Waiting for Cleint Requests!")
    rospy.init_node('times_three_int_server_node')
    rospy.Service('times_three_int_service', times_three_int, handle_times_three_int)
    rospy.spin()

if __name__ == '__main__':
    times_three_int_server()

