#!/usr/bin/env python

from ros_udemy.srv import times_three_int
from ros_udemy.srv import times_three_intRequest
from ros_udemy.srv import times_three_intResponse
import time
import rospy
import sys

def times_three_int_client(x, y, z):
    rospy.wait_for_service('times_three_int_service')
    try:
        times_three_int_proxy = rospy.ServiceProxy('times_three_int_service', times_three_int)
        request = times_three_int_proxy(x, y, z)
        return request
    except rospy.ServiceException as error:
        print('Service Gagal', error)

def client_process():
    print("Requesting {} * {} * {}".format(x, y, z))
    times = times_three_int_client(x, y, z)
    print("Hasilnya adalah {}".format(times))

def log():
    error = print("Terdapat error pada {}".format(sys.argv[0]))
    return error

if __name__ == '__main__':
    if len(sys.argv) == 4:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
        z = int(sys.argv[3])
    else:
        print(log())
        sys.exit()
        
    client_process()