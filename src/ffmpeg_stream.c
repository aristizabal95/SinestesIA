#ifndef FFMPEG_STREAM
#define FFMPEG_STREAM

#include <stdio.h>
#include <pthread.h>

#include "globals.h"
#include "ffmpeg_stream.h"

#endif

void *ffmpeg_threadfunc(void *arg) {
	FILE *pipeout; // This will be the pipe that will write to ffmpeg

	pipeout = popen("ffmpeg -r 25 -f rawvideo -vcodec rawvideo -pix_fmt rgb24 -s 1280x480 -i - -preset ultrafast -vcodec libx264 -tune zerolatency -crf 40 -b 5000k -f mpegts udp://localhost:1234", "w");
	while(!die) {
		pthread_mutex_lock(&streaming_mutex);
		if(rgbReady && depthReady) {
			fwrite(messageBuffer, 1, 640*480*4, pipeout);
			fflush(pipeout);
			rgbReady = 0;
			depthReady = 0;
		}
		pthread_mutex_unlock(&streaming_mutex);
	}
	pclose(pipeout);
	return NULL;
}

