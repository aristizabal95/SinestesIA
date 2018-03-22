# M.O.N.I.K.A
Motorized, Omniscient, Network Independent Kinect Assistant

This is just a little project of mine, trying to create a smart-home (or may I say smart-room?) Assistant based on Kinect and RPI. 

# Requirements:
  # Hardware Requirements:
  M.O.N.I.K.A Is intented to run on two separate systems. First a server streaming all Kinect Data as well as receiving Hardware Commands. In the current state, this server is running in a Raspberry Pi 3 B. This server also requires a servo to control X axis of the Kinect. On the other side, there's a client intended to do the heavy work with the data received from the server. This can run on the same system.
  Over all, the hardware requirements are:
  - Server system (Rpi3B)
  - Kinect (v1)
  - Servo
  - Client system
  
  # Dependencies:
  This project currently depends on:
  Server Side
  - Ffmpeg
  - Pthread (`sudo apt-get install libpthread-stubs0-dev`)
  - [Libfreenect](https://github.com/OpenKinect/libfreenect)
  
  Client Side
  - Python3.4+
  - Ffmpeg
  - Numpy
  - OpenCV2
  - [pypng](https://github.com/drj11/pypng)

# Installation

First clone this repo:
`git clone https://github.com/aristizabal95/M.O.N.I.K.A.git`

For the server side, you must compile the source code
`cd M.O.N.I.K.A`
`gcc -Wall -o bin/main src/*.c -lpthread -lfreenect`

For the client side, there's no need to have any C code, and just use the python programs inside the `client-side` folder
