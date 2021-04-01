# TelloDrone
Guilford College Capstone Project - Connor Button and Eric Eaves

Spring 2021

Professor Chafic Bou-Saba

## Goals
Remote connection to Tello drone via Raspberry Pi and VNC connection. The drone is equipped with a 720p front facing camera, 2 vertical-axis IR sensors, and rotor guards for each of the 4 propellers.

The drone can be queried for frames from the video stream. The frames are individually processed for facial and gesture detection. Based on the python logic, commands are returned to the drone.

Commands can be sent to the drone in the form:

\[Right(+)/Left(-), Forward(+)/Backward(-), Up(+)/Down(-), Clockwise(+)/C-Clockwise(-)], 
where each element of the array is an integer, denoting the speed of the movement.

The code will then run a thread sleep command for a predetermined amount of time to allow the drone to move before accepting further commands.

**ImageControl** displays the live image from the drone and allows user input to actively influence the speed, direction, and height of the drone. This extends the **KeyPressModule** and a *pygame* window for user input.

**ObjectTracking** sets the framework for facial object detection, using one of the [haar cascade](https://www.murtazahassan.com/wp-content/uploads/2020/03/haarcascades.zip) files available online.

## Dependencies
Python 3.7

### Module Dependencies
* pip : 19.2.3

* numpy : 1.20.1

* opencv-python : 4.5.1.48

* pygame : 2.0.1

* setuptools : 41.2.0

* djitellopy : 1.5

### Hardware
* DJI Tello EDU Drone

* Raspberry Pi 4 Model B

### Software
* Development IDE : PyCharm (PC), Thonny (PI)

* RealVNC

* Rasbian OS

### Other Requirements
* Internet Connection

* Ethernet for Pi

* Open Space

