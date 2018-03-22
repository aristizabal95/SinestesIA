#ifndef COMMAND_HANDLER
#define COMMAND_HANDLER

#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <pthread.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <signal.h>
#include <pigpio.h>

#include "globals.h"
#include "command_handler.h"

#endif

#define PORT 6666
#define MIN_WIDTH 1000
#define MAX_WIDTH 2000
#define MIN_POS (-90)
#define MAX_POS 90
#define SERVO_PIN 4
#define SERVO_SPEED 60 // Value in degrees/second

int desired_pos = 0;
int current_pos = 0;
pthread_t servo_thread;

void stop(int signum) {
	die = 1;
}

void error(char *msg) {
	perror(msg);
	die = 1;
}

struct command_t issueCommand(struct command_t cmd, struct command_t current_cmd) {
	if(cmd.idle != current_cmd.idle)
		// TODO Turn camera on or off
	if(cmd.format != current_cmd.format)
		requested_format = FREENECT_VIDEO_IR_8BIT;
	if(cmd.tilt != current_cmd.tilt){
		freenect_set_tilt_degs(f_dev, (int)(cmd.tilt - 30));
		current_cmd.tilt = freenect_get_tilt_degs(freenect_get_tilt_state(f_dev));
	}
	if(cmd.yaw != current_cmd.yaw){
		pthread_mutex_lock(&servo_pos_mutex);
		desired_pos = cmd.yaw - 90;
		current_cmd.yaw = current_pos;
		pthread_mutex_unlock(&servo_pos_mutex);
	}
		if(cmd.led != current_cmd.led){
			switch((int)cmd.led){
				case 0:
					freenect_set_led(f_dev, LED_OFF);
					break;
				case 1:
					freenect_set_led(f_dev, LED_GREEN);
					break;
				case 2:
					freenect_set_led(f_dev, LED_YELLOW);
					break;
				case 3:
					freenect_set_led(f_dev, LED_RED);
					break;
				case 4:
					freenect_set_led(f_dev, LED_BLINK_GREEN);
					break;
				case 5:
					//freenect_set_led(f_dev, LED_BLINK_YELLOW);
					break;
				case 6:
					freenect_set_led(f_dev, LED_BLINK_RED_YELLOW);
					break;
				case 7:
					// TODO waiting mode, rapidly alternate between green, yellow and red
					break;
				default:
					freenect_set_led(f_dev, LED_BLINK_GREEN);
					break;
			}
			current_cmd.led = cmd.led;
		}

	return current_cmd;
}

void *servo_threadfunc(void *arg) {
	if (gpioInitialise() < 0) error("Could not start PiGPIO\n");
	gpioSetSignalFunc(SIGINT, stop);
	float time = 1.0/SERVO_SPEED*1000000; // Time in microseconds
	int current_width;

	while(!die) {
		pthread_mutex_lock(&servo_pos_mutex);
		if(current_pos != desired_pos) {
			if (current_pos > desired_pos){
				current_pos--;
			}
			else {
				current_pos++;
			}
			// Convert pos from angle to pulse
			current_width = (int)(((float)current_pos - MIN_POS)/(MAX_POS - MIN_POS)*(MAX_WIDTH - MIN_WIDTH) + MIN_WIDTH);
			gpioServo(SERVO_PIN, current_width);
			usleep(time);
		}
		pthread_mutex_unlock(&servo_pos_mutex);
	}
	return NULL;
}

void *tcp_threadfunc(void *arg) {
	int sockfd, newsockfd, portno, clilen, n;
	int rc;
	struct command_t incoming_cmd;
	struct sockaddr_in serv_addr, cli_addr;
	sockfd = socket(AF_INET, SOCK_STREAM, 0);

	//define initial state
	struct command_t cmd;
	struct command_t current_cmd;
	cmd.idle = 0;
	cmd.format = 1;
	cmd.tilt = 0;
	cmd.yaw = 0;
	cmd.led = 0;
	cmd.brightness = 31;
	current_cmd = cmd;

	if (sockfd < 0)
		error("Could not create command socket\n");

	bzero((char *) &serv_addr, sizeof(serv_addr));
	portno = PORT;
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_port = htons(portno);
	serv_addr.sin_addr.s_addr = INADDR_ANY;

	if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0)
		error("Could not bind command server\n");

	listen(sockfd,5);
	clilen = sizeof(cli_addr);
	newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
	if (newsockfd < 0)
		error("Could not accept connection\n");

	// Start servo process with desired global variables
	rc = pthread_create(&servo_thread, NULL, servo_threadfunc, NULL);
	if(rc) {
		error("Could not create servo thread\n");
	}

	while(!die){
		n = -1;
		n = read(newsockfd, &incoming_cmd, 255);
		if (n < 0){
			error ("Could not read command\n");
			break;
		} 
		else {
		cmd = incoming_cmd;
		current_cmd = issueCommand(cmd, current_cmd);
		write(newsockfd, &current_cmd, sizeof(current_cmd));
		}
	}
}
