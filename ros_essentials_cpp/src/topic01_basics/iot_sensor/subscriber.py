import rospy
from ros_essentials_cpp import IoTSensor

def iotSensorCallback(iotSensorMessage):
    rospy.loginfo('Data received: (%d, %s, %.2f, %.2f)', 
                iotSensorMessage.id, iotSensorMessage.name,
                iotSensorMessage.temperature, iotSensorMessage.humidity)
    
rospy.init_node('iotSubscriberNode',anonymous= True)
rospy.Subscriber('iotTopic', IoTSensor, iotSensorCallback)

rospy.spin()
