# robotont_laserscan_leds
If something doesn;y
Required packages: depthimage_to_laserscan, robotont_msgs 
Demo: roslaunch robotont_laserscan_leds laserscan_and_leds_from_depth_image.launch 
Clear LEDs: rosrun robotont_laserscan_leds clear.py

For LIDAR:
Required: hls_lfcd_lds_driver
roslaunch hls_lfcd_lds_driver hlds_laser.launch
sudo chmod a+rw /dev/ttyUSB0

rosrun robotont_laserscan_leds lidar_leds_demo.py
