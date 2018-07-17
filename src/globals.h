#ifndef GLOBALS_H_
#define GLOBALS_H_

#include "libfreenect.h"
#define MESSAGE_LEN 640*480*3*2

struct command_t {
	unsigned int idle:1; // Idle defines wether the cam is on or off
	unsigned int format:1; // format specifies wether the camera is IR or RGB
	unsigned int tilt:6; // Tilt Pos: range from 0 to 60 (-30, 30)
	uint8_t      yaw; // Yaw Pos: range from 0 to 180 (-90, 90)
	unsigned int led:3; // LED state, range from 0 to 6
	unsigned int brightness:5; // Brightness range from 0 to 32
};

extern struct command_t cmd;

extern pthread_mutex_t streaming_mutex;
extern pthread_mutex_t servo_pos_mutex;
extern volatile int die;

extern uint8_t *messageBuffer;
extern freenect_video_format requested_format;
extern freenect_video_format current_format;

extern freenect_context *f_ctx;
extern freenect_device *f_dev;

extern volatile int rgbReady;
extern volatile int depthReady;
#endif
