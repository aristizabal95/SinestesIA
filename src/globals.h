#ifndef GLOBALS_H_
#define GLOBALS_H_

extern pthread_mutex_t streaming_mutex;
extern pthread_mutex_t servo_pos_mutex;
extern volatile int die;

uint8_t *messageBuffer;
#endif
