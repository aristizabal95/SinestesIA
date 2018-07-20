# ImprovAI
Music Generation through interactive dancing with Deep Learning.

# Requirements:
  # Hardware Requirements:
  ImprovAI Is been designed to run on two separate systems, although it can be modified to run on just one. First a server streaming all Kinect Data as well as receiving Hardware Commands. In the current state, this server is running in a Raspberry Pi 3 B. On the other side, there's a client intended to do the heavy work with the data received from the server. This can run on the same system.
  Over all, the hardware requirements are:
  - Server system (Rpi3B)
  - Kinect (v1)
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
  - Tensorflow
  - Pure Data
  - H5Py (for training only)
  - [pypng](https://github.com/drj11/pypng)

# Installation

First clone this repo:
`git clone https://github.com/aristizabal95/M.O.N.I.K.A.git`

For the server side, you must compile the source code
`cd ImprovAI`
`gcc -Wall -o -I/LIBFREENECT/HEADER/LIBRARY/DIR bin/main src/*.c -lpthread -lfreenect -lm`

For the client side, there's no need to compile any C code, and just use the python programs inside the `client-side` folder
`python3 client-side/main.py`
