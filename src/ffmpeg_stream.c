#ifndef FFMPEG_STREAM
#define FFMPEG_STREAM

#include <stdio.h>
#include <pthread.h>

#include "globals.h"
#include "ffmpeg_stream.h"

#endif

void *ffmpeg_threadfunc(void *arg) {
	FILE *pipeout; // This will be the pipe that will write to ffmpeg

	pipeout = popen("ffmpeg -threads 6 -r 25 -f rawvideo -vcodec rawvideo -pix_fmt rgb24 -s 640x480 -i - -srtp_out_suite AES_CM_128_HMAC_SHA1_80 -srtp_out_params 00108310518720928b30d38f41149351559761969b71d79f8218a39259a7 -preset ultrafast -vcodec libx264 -tune zerolatency -crf 40 -b 5000k -f rtp_mpegts srtp://192.168.0.100:1234", "w");
	while(!die) {
		pthread_mutex_lock(&streaming_mutex);
		if(messageReady) {
			fwrite(messageBuffer, 1, 640*480*3, pipeout);
			fflush(pipeout);
			messageReady = 0;
		}
		pthread_mutex_unlock(&streaming_mutex);
	}
	pclose(pipeout);
	return NULL;
}

