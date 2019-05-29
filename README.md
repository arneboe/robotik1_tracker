# robotik1_tracker
Tracking stuff for robotik1 turtle

# Installation


```
cd catkin_ws/src
git clone git@github.com:arneboe/robotik1_tracker.git
cd ..
catkin_make
```

In `launch/usb_cam_stream_publisher.launch` set the correct absolut path to the camera calibration file (which is located in `calibration`).


# Usage
```
roscore 
roslaunch robotik1_tracker usb_cam_stream_publisher.launch  
roslaunch robotik1_tracker aruco_marker_finder.launch  markerId:=701 markerSize:=0.1 
rosrun robotik1_tracker camera_tracker.py
```
