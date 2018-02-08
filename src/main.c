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
#include <pthread.h>
#include <math.h>

// Declare threads
pthread_t kinect_streaming_thread;
pthread_t server_thread;
pthread_t command_handler_thread;

// Mutex for handling servo position update
pthread_mutex_t servo_pos_mutex = PTHREAD_MUTEX_INITIALIZER

volatile int die = 0;

int g_argc;
char **g_argv;

int main(int argc, char *argv[]){
	int rc;

	//Create kinect thread
	rc = pthread_create(&kinect_streaming_thread, NULL, TODO, TODO);
	if (rc){
		printf("ERROR creating kinect streaming thread. Code is %d\n", rc);
		exit(-1);
	}

	//Create server_thread
	rc = pthread_create(&server_thread, NULL, TODO, TODO);
	if(rc){
		printf("ERROR creating server thread. Code is %d\n", rc);
		exit(-1);
	}

	//Create command handler thread
	rc = pthread_create(&command_handler_thread, NULL, TODO, TODO);
	if(rc){
		printf("Error creating command handler thread. Code is %d\n", rc);
		exit(-1);
	}
	pthread_exit(NULL);
}

