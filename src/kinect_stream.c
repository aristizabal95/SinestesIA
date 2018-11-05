// KINECT_STREAM
// Functions created with the purpose of receiving data from the kienct
// and preparing it for serving. This functions will run asynchronously
// from the rest of the program.
#ifndef KINECT_STREAM
#define KINECT_STREAM

#include <stdio.h>
#include "libfreenect.h"
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <pthread.h>
#include <time.h>

#include <math.h>

#include "globals.h"

#endif

// freenect_video_format requested_format = FREENECT_VIDEO_RGB;
// freenect_video_format current_format = FREENECT_VIDEO_RGB;

pthread_cond_t freenect_frame_cond = PTHREAD_COND_INITIALIZER;
pthread_t message_thread;
clock_t start,end;
double cpu_time_used;

// int got_rgb = 0;
int got_depth = 0;
// volatile int rgbReady = 0;
volatile int depthReady = 0;

uint8_t *depth_mid, *depth_front;
// uint8_t *rgb_back, *rgb_mid, *rgb_front;
uint8_t *messageBuffer;

void prepareMessage() {
	pthread_mutex_lock(&streaming_mutex);

	// When using YUV_RGB mode, RGB frames only arrive at 15Hz, so we shouldn't force them to draw in lock-step.
	// However, this is CPU/GPU intensive when we are receiving frames in lockstep.
	// if (current_format == FREENECT_VIDEO_YUV_RGB) {
	// 	while(!got_depth && !got_rgb) {
	// 		pthread_cond_wait(&freenect_frame_cond, &streaming_mutex);
	// 		printf("YUV waiting\n");
	// 	}
	// }
	// else {
	// 	while ((!got_depth || !got_rgb) && requested_format != current_format) {
	// 		pthread_cond_wait(&freenect_frame_cond, &streaming_mutex);
	// 	}
	// }
	//
	// if (requested_format != current_format) {
	// 	pthread_mutex_unlock(&streaming_mutex);
	// 	return;
	// }

	uint8_t *tmp;

	if (got_depth) {
		tmp = depth_front;
		depth_front = depth_mid;
		depth_mid = tmp;
		memcpy(messageBuffer, depth_front, (640*480)); // copy depth to message shifted so as to leave space for rgb
		depthReady = 1;
		got_depth = 0;
	}
	// if (got_rgb) {
	// 	tmp = rgb_front;
	// 	rgb_front = rgb_mid;
	// 	rgb_mid = tmp;
	// 	memcpy(messageBuffer, rgb_front, (640*480*3));
	// 	rgbReady = 1;
	// 	got_rgb = 0;
	// }
	pthread_mutex_unlock(&streaming_mutex);
}

void *message_threadfunc(void *arg) {
	while(!die){
		prepareMessage();
	}
	return NULL;
}

void depth_cb(freenect_device *dev, void *v_depth, uint32_t timestamp) {

	int i;
	uint16_t *depth = (uint16_t*)v_depth;

	//pthread_mutex_lock(&streaming_mutex);
	for (i=0; i<640*480; i++) {
		depth_mid[i] = (int)(depth[i]/2048.0*255);
	}

	got_depth++;
	//pthread_cond_signal(&freenect_frame_cond);
	//pthread_mutex_unlock(&streaming_mutex);
}

// void rgb_cb(freenect_device *dev, void *rgb, uint32_t timestamp) {
// 	pthread_mutex_lock(&streaming_mutex);
//
// 	// swap buffers
// 	assert (rgb_back == rgb);
// 	rgb_back = rgb_mid;
// 	freenect_set_video_buffer(dev, rgb_back);
// 	rgb_mid = (uint8_t*)rgb;
//
// 	got_rgb++;
// 	pthread_cond_signal(&freenect_frame_cond);
// 	pthread_mutex_unlock(&streaming_mutex);
// }

void *freenect_threadfunc(void *arg) {
	int rc;

	depth_mid = (uint8_t*)malloc(640*480);
	depth_front = (uint8_t*)malloc(640*480);
	// rgb_back = (uint8_t*)malloc(640*480*3);
	// rgb_mid = (uint8_t*)malloc(640*480*3);
	// rgb_front = (uint8_t*)malloc(640*480*3);
	messageBuffer = (uint8_t*)malloc(640*480); // Increased messageBuffer size for both depth and rgb

	freenect_set_depth_callback(f_dev, depth_cb);
	// freenect_set_video_callback(f_dev, rgb_cb);
	// freenect_set_video_mode(f_dev, freenect_find_video_mode(FREENECT_RESOLUTION_MEDIUM, current_format));
	freenect_set_depth_mode(f_dev, freenect_find_depth_mode(FREENECT_RESOLUTION_MEDIUM, FREENECT_DEPTH_11BIT));
	// freenect_set_video_buffer(f_dev, rgb_back);

	freenect_start_depth(f_dev);
	// freenect_start_video(f_dev);

	rc = pthread_create(&message_thread, NULL, message_threadfunc, NULL);
	if (rc) {
		printf("pthread_create failed!\n");
		freenect_shutdown(f_ctx);
		return NULL;
	}

	while(!die && freenect_process_events(f_ctx) >= 0) {
		// if (requested_format != current_format) {
		// 	freenect_stop_video(f_dev);
		// 	freenect_set_video_mode(f_dev, freenect_find_video_mode(FREENECT_RESOLUTION_MEDIUM, requested_format));
		// 	freenect_start_video(f_dev);
		// 	current_format = requested_format;
		// }
	}

	printf("\nShutting down streams...\n");

	freenect_stop_depth(f_dev);
	// freenect_stop_video(f_dev);

	freenect_close_device(f_dev);
	freenect_shutdown(f_ctx);
	free(depth_mid);
	free(depth_front);
	// free(rgb_back);
	// free(rgb_mid);
	// free(rgb_front);

	printf("--done!\n");
	return NULL;
}
