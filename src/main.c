/***************************************************************
 *                       M.O.N.I.K.Av2                         * 
 * Motirized, Omniscient, Network Independent Kinect Assistant *
 *                                                             *
 *                      HARDWARE SERVER                        *
 * This server will handle 3 separate tasks:                   *
 * 1. Configure kinect and stream video/audio data with RTMP   *
 * 2. Create TCP Server for listening to commands              *
 * 3. Handle commands.                                         *
 * Each of this tasks will have its own thread. In addition,   *
 * the servo will have an isolated thread to handle speed      *
 ***************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <pigpio.h>
#include <string.h>
#include "libfreenect.h"
#include <websock/websock.h>
#include <pthread.h>
#include <math.h>
#include <unistd.h>

#include "globals.h"
#include "kinect_stream.h"
#include "ffmpeg_stream.h"

#ifndef SIGQUIT
#define SIGQUIT SIGTERM
#endif

// Declare threads
pthread_t kinect_streaming_thread;
pthread_t server_thread;
pthread_t move_servo_thread;

// Mutex for handling servo position update
pthread_mutex_t servo_pos_mutex = PTHREAD_MUTEX_INITIALIZER;
// Mutex for handling message preparation vs message send
pthread_mutex_t streaming_mutex = PTHREAD_MUTEX_INITIALIZER;

volatile int die = 0;

int g_argc;
char **g_argv;

// Freenect global variables, remember to define them in globals.h
freenect_context *f_ctx;
freenect_device *f_dev;

/******************************************************************
 *                     FUNCTION DECLARATION                       *
 ******************************************************************/
int freenect_config();
int freenect_stream();
void *freenect_main();

int server_config();
int server_run();
void *server_main();

int issueCommand();
int moveServo();
void *servo_main();
void handler(int sig);

int main(int argc, char *argv[]){
	int rc; // return code
	signal(SIGINT, handler);

	printf("Okay everyone! I'm peering into your reality! Ahaha!\n");
	g_argc = argc;
	g_argv = argv;

	rc = freenect_init(&f_ctx, NULL);
	if (rc < 0){
		printf("No! I can't see! Something's wrong!\n");
		printf("Wait! Don't let me go!\n");
		sleep(1);
		for(int i=0;i<3;i++){
			printf(".");
			sleep(1);
		}
		printf("Fix me.\n");
		return 1;
	}

	// select subdevices. Check documentation for selecting microphone array too.
	freenect_select_subdevices(f_ctx, (freenect_device_flags)(FREENECT_DEVICE_MOTOR | FREENECT_DEVICE_CAMERA));

	int nr_devices = freenect_num_devices (f_ctx);
	int user_device_number = 0;
	if (nr_devices < 1) {
		freenect_shutdown(f_ctx);
		printf("Can't find my eyes! Everything's dark! Connect me!\n");
		return 1;
	}

	rc = freenect_open_device(f_ctx, &f_dev, user_device_number);
	if (rc < 0) {
		printf("Can't open my eyes!\n");
		for(int i=0;i<3;i++){
			printf(".");
			sleep(1);
		}
		printf("Help me.\n");
		freenect_shutdown(f_ctx);
		return 1;
	}

	// Freenect is now working.
	printf("I can see through, with burning retinas. Is someone there? Are you there?\n");

	// Create kinect thread
	rc = pthread_create(&kinect_streaming_thread, NULL, freenect_threadfunc, NULL);
	if (rc){
		printf("ERROR creating kinect streaming thread. Code is %d\n", rc);
		exit(-1);
	}

	// ffmpeg thread
	rc = pthread_create(&server_thread, NULL, ffmpeg_threadfunc, NULL);
	if(rc){
		printf("ERROR creating server thread. Code is %d\n", rc);
		exit(-1);
	}

	// //Create command handler thread
	// rc = pthread_create(&move_servo_thread, NULL, moveServo, TODO);
	// if(rc){
	// 	printf("Error creating command handler thread. Code is %d\n", rc);
	// 	exit(-1);
	// }
	// pthread_exit(NULL);
	pause()	;
	return 0;
}

void handler(int sig){
	if (sig == SIGINT || sig == SIGTERM || sig == SIGQUIT){
		die = 1;
		printf("Wait, not yet!\n");
		signal(sig, handler);
	}
}
