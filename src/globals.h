#ifndef GLOBALS_H_
#define GLOBALS_H_

#include "libfreenect.h"
#define MESSAGE_LEN 640*480*3

extern pthread_mutex_t streaming_mutex;
extern pthread_mutex_t servo_pos_mutex;
extern volatile int die;

extern uint8_t *messageBuffer;
extern freenect_video_format requested_format;
extern freenect_video_format current_format;

extern freenect_context *f_ctx;
extern freenect_device *f_dev;

extern int messageReady;
#endif
