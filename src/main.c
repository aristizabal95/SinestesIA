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

#include "globals.h"
#include "websocket_stream.h"

// Declare threads
pthread_t kinect_streaming_thread;
pthread_t server_thread;
pthread_t move_servo_thread;

// Mutex for handling servo position update
pthread_mutex_t servo_pos_mutex = PTHREAD_MUTEX_INITIALIZER;
// Mutex for handling message preparation vs message send
pthread_mutex_t streaming_mutex = PTHREAD_MUTEX_INITIALIZER;

volatile int die = 0;

uint8_t *depth_mid, *depth_front;
uint8_t *rgb_back, *rgb_mid, *rgb_front;
uint8_t *messageBuffer;

int g_argc;
char **g_argv;

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

int main(int argc, char *argv[]){
	int rc;

	//Create kinect thread
	// rc = pthread_create(&kinect_streaming_thread, NULL, freenect_main, TODO);
	// if (rc){
	// 	printf("ERROR creating kinect streaming thread. Code is %d\n", rc);
	// 	exit(-1);
	// }

	// //Create server_thread
	// rc = pthread_create(&server_thread, NULL, server_main, TODO);
	// if(rc){
	// 	printf("ERROR creating server thread. Code is %d\n", rc);
	// 	exit(-1);
	// }

	// //Create command handler thread
	// rc = pthread_create(&move_servo_thread, NULL, moveServo, TODO);
	// if(rc){
	// 	printf("Error creating command handler thread. Code is %d\n", rc);
	// 	exit(-1);
	// }
	// pthread_exit(NULL);
	createWebSocket("0.0.0.0", "8080");
	return 0;
}

