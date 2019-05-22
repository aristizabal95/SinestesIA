# Sinestes.IA
Music Generation through interactive dancing with Deep Learning.

# Requirements:
  # Hardware Requirements:
  - Kinect (v1)
  
  # Dependencies:
  The dependencies considerer here are only for running the pre-trained models both through `Interpreter.py` and `dream.py`:
  - Ffmpeg
  - Pthread (`sudo apt-get install libpthread-stubs0-dev`)
  - [Libfreenect](https://github.com/OpenKinect/libfreenect)
  - Python3.4+
  - Numpy
  - Tensorflow
  - OpenCV2
  - Pure Data Extended

# Installation

First clone this repo, get and unzip the trained data, and `cd` to the project:
```
git clone https://github.com/aristizabal95/SinestesIA.git
wget LINK_TO_FILES
unzip experiments.zip
cd SinestesIA
```
# Build
This step is only necessary if `interpreter.py` is to be used
simply run `gcc -Wall -o bin/main src/*.c -lpthread -lfreenect` to compile the program

# Running the Interpreter
The Interpreter takes data from the Kinect in real-time, and generates sound instructions to be sent to Pure Data. To run this script you must
1. Open `pd/performer.pd` with Pure Data
2. Have the Kinect running with `./bin/main`
3. Start the Interpreter with `python3 mains/interpreter.py`

# Running the dream generation
The `mains/dream.py` script generates sequences of dance and music. To run it you must
1. Open `pd/performer.pd` with Pure Data
2. Start the Dream generation with `python3 mains/dream.py`
3. Optionally, set the duration of each dream with the argument `-l` (default: 150) and use `-r` to specify wether the program should add random influences to the dream generation or not (default: 0)
Example:
`python3 mains/dream -l 300 -r 1 # Make the length of each dream 300 and allow for randomness in the dreams`
