#!/usr/bin/env python
import rospy
from robotont_msgs.msg import LedModuleSegment, ColorRGB
import numpy as np
from sensor_msgs.msg import LaserScan
import time
import math

range_1=2#maximum range(anything further away from will be blue)
range_2=1#closer to it will be greener, further away is more blueish
closest=0.3#closer to it will be reder, further away is more green
max_c=255

distances=[]

np.warnings.filterwarnings('ignore')

led_publisher = rospy.Publisher(
        '/robotont/led_segment', LedModuleSegment, queue_size=5)

def scan_callback(data):
    global distances
    distances = data.ranges

def timer_callback(event):
    global distances
    distances = [x for x in distances if str(x) != 'nan']#filter nans
    array_len = len(distances)
    if array_len==0:#if nothing came
        print('Zero')
        return
    
    led_msg = LedModuleSegment()
    LED_COUNT=60
    led_msg.colors = []
    dest=[]
    for i in range(LED_COUNT):
        color = ColorRGB()#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        dis=np.nanmean(distances[int(i*array_len/LED_COUNT):int((i+1)*array_len/LED_COUNT)])
        dest.append(dis)
        #One By One
        if dis>range_1:
            color.r = 0
            color.g = 0
            color.b = max_c
        elif dis>range_2:
            v=mapper_basic(dis,range_2,range_1,0,max_c)
            color.b=v
            color.g=max_c-v
            color.r=0
        else:
            v=mapper_basic(dis,closest,range_2,0,max_c)
            color.b=0
            color.g=v
            color.r=max_c-v
        led_msg.colors.append(color)
    led_msg.idx_start = 0
    #print(dest, led_msg.colors)
    led_publisher.publish(led_msg)
    
    
def doLED():
    # Starts a new node
    rospy.init_node('robotont_led_publisher_subscriber', anonymous=True)
    rospy.Subscriber('scan', LaserScan, scan_callback)
    t = rospy.Timer(rospy.Duration(.1), timer_callback)
    rospy.spin()

def mapper_basic(val, fromi, toi, fromo, too):
    #rospy.loginfo("Got value %f", val)
    #print(f'val {fromi}, {toi}, {fromo}, {too}, {(val-fromi)*(too-fromo)/(toi-fromi)+fromo}, {int((val-fromi)*(too-fromo)/(toi-fromi)+fromo)}')
    if val<fromi or str(val)=='nan':
        #print(f'Value received {val}, led output {fromo} [val<min_inp]')
        return fromo
    elif val>toi:
        #print(f'Value received {val}, led output {too} [val>max_inp]')
        return too
    else:
        #print(f'Value received {val}, led output {int((val-fromi)*(too-fromo)/(toi-fromi)+fromo)}')
        return int((val-fromi)*(too-fromo)/(toi-fromi)+fromo)


if __name__ == '__main__':
    try:
        doLED()
    except rospy.ROSInterruptException:
        print("Exiting nicely...")
        pass
