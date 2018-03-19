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

#include "globals.h"
#include "command_handler.h"

#endif

#define PORT 6666

void error(char *msg) {
	perror(msg);
	die = 1;
}

int issueCommand(struct command_t cmd, struct command_t current_cmd) {
	if(cmd.tilt != current_cmd.tilt)
		freenect_set_tilt_degs(f_dev, (int)(cmd.tilt - 30));
	return 0;
}

void *tcp_threadfunc(void *arg) {
	int sockfd, newsockfd, portno, clilen, n;
	struct command_t incoming_cmd;
	struct sockaddr_in serv_addr, cli_addr;
	sockfd = socket(AF_INET, SOCK_STREAM, 0);

	//define initial state
	struct command_t cmd;
	struct command_t current_cmd;
	cmd.idle = 0;
	cmd.format = 1;
	cmd.tilt = 0;
	cmd.yaw = 90;
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

	while(!die){
		n = -1;
		n = read(newsockfd, &incoming_cmd, 255);
		if (n < 0){
			error ("Could not read command\n");
			break;
		} 
		else {
		cmd = incoming_cmd;
		issueCommand(cmd, current_cmd);
		current_cmd = cmd;
		}
	}
}
