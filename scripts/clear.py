#!/usr/bin/env python
import rospy
from robotont_msgs.msg import LedModuleSegment, ColorRGB
import time
import math


def doLED():
    # Starts a new node
    rospy.init_node('robotont_led_publisher', anonymous=True)
    led_publisher = rospy.Publisher(
        '/robotont/led_segment', LedModuleSegment, queue_size=5)
    

    t=0.1
    t1=0.1
    c_max=200
    c_step=10
    led_step=1
    led_msg = LedModuleSegment()


    LED_COUNT=60

    led_msg.idx_start = 0
    led_msg.colors = []
    color = ColorRGB()

    #One By One
    color.r = 0
    color.g = 0
    color.b = 0
    led_msg.colors = []
    for i in range(led_step):
        led_msg.colors.append(color)
    for i in range(0, LED_COUNT,led_step):
        led_msg.idx_start = i
        led_publisher.publish(led_msg)
        rospy.sleep(t1)

                
if __name__ == '__main__':
    try:
        doLED()
    except rospy.ROSInterruptException:
        print("Exiting nicely...")
        pass
