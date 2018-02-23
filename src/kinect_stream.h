#ifndef KINECT_STREAM_H
#define KINECT_STREAM_H

void prepareMessage();
void *message_threadfunc(void *arg);
void depth_cb(freenect_device *dev, void *v_depth, uint32_t timestamp);
void rgc_cb(freenect_device *dev, void *rgb, uint32_t timestamp);
void *freenect_threadfunc(void *arg);

#endif
