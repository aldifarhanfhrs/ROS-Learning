#!/usr/bin/env python
# license removed for brevity
import rospy
from ros_essentials_cpp.msg import IoTSensor
import random

pub = rospy.Publisher('iotTopic', IoTSensor, queue_size= 10)
rospy.init_node('iotPublisherNode', anonymous= True)

rate = rospy.Rate(1)

i = 0
while not rospy.is_shutdown():
    iotSensor = IoTSensor()
    iotSensor.id = 1
    iotSensor.name = 'Biomol'
    iotSensor.temperature = 24.00 + (random.random()*2)
    iotSensor.humidity = 33.00 + (random.random()*2)

    rospy.loginfo('Sensor Publishing: ')
    rospy.loginfo(iotSensor)
    pub.publish(iotSensor)
    rate.sleep()

    i = i+1
