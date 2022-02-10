# Sinestes.IA
Music Generation through interactive dancing with Deep Learning.

## Requirements:
  ### Hardware Requirements:
  - Kinect (v1)
  
  ### Dependencies:
  The dependencies considerer here are only for running the pre-trained models both through `Interpreter.py` and `dream.py`:
  - Ffmpeg
  - Pthread (`sudo apt-get install libpthread-stubs0-dev`)
  - [Libfreenect](https://github.com/OpenKinect/libfreenect)
  - Python3.4+
  - Numpy
  - Tensorflow
  - OpenCV2
  - Pure Data Extended

## Installation
First get the trained data from [here](https://livejaverianaedu-my.sharepoint.com/:u:/g/personal/a_aristizabalm_javeriana_edu_co/EV0mkW_-nBdKuJlwmywlya4B844Jt_S-8yd5d8IIxPbrYQ?e=EAVMwy)

Then clone this repo, unzip the trained data and `cd` to the project:
```
unzip experiments.zip
git clone https://github.com/aristizabal95/SinestesIA.git
cd SinestesIA
```
### Build
This step is only necessary if `interpreter.py` is to be used

simply run `gcc -Wall -o bin/main src/*.c -lpthread -lfreenect` to compile the program

## Running the Interpreter
The Interpreter takes data from the Kinect in real-time, and generates sound instructions to be sent to Pure Data. To run this script you must
1. Open `pd/performer.pd` with Pure Data
2. Have the Kinect running with `./bin/main`
3. Start the Interpreter with `python3 mains/interpreter.py`

## Running the dream generator
The `mains/dream.py` script generates sequences of dance and music. To run it you must
1. Open `pd/performer.pd` with Pure Data
2. Start the Dream generator with `python3 mains/dream.py`
3. Optionally, set the duration of each dream with the argument `-l` (default: 150) and use `-r` to specify wether the program should add random influences to the dream generation or not (default: 1)
Example:
`python3 mains/dream -l 300 -r 0 # Make the length of each dream 300 and disable randomness in the dreams`
