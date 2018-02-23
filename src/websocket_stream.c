// WEBSOCKET_STREAM
// Functions created with the purpose of streaming live video/audio
// data through a websocket. This websocket will be streaming on port
// asynchronously from the rest of the program. In this code, we
// will suppose a message has already been generated, and is ready for
// streaming.
#ifndef WEBSOCKET_STREAM
#define WEBSOCKET_STREAM


#include <stdio.h>
#include <websock/websock.h>
#include <pthread.h>
#include <string.h>

#include "globals.h"

#endif

void send_streaming(libwebsock_client_state *state, char *messageBuff) {
	pthread_mutex_lock(&streaming_mutex);
	libwebsock_send_text(state, messageBuff); // TODO: send binary instead of text
	pthread_mutex_unlock(&streaming_mutex);
}

int streaming_connect_cb(libwebsock_client_state *state) {
	fprintf(stderr, "New connection with socket descriptor: %d\n", state->sockfd);
	while(!die){
		send_streaming(state, (char *)messageBuffer);
	}
	return 0;
}

void createWebSocket(char* ip, char* port){
	libwebsock_context *ctx = NULL;
	ctx = libwebsock_init();
	if(ctx == NULL){
		fprintf(stderr, "Error during libwebsock_init.\n");
		exit(1);
	}
	ctx->onopen = streaming_connect_cb;
	libwebsock_bind(ctx, ip, port);
	printf("Socket created! Waiting for connection\n");
	libwebsock_wait(ctx);
}

void *websocket_threadfunc(void *arg) {
	createWebSocket("0.0.0.0", "8080");
	return;
}

// int main(){
// 	createWebSocket("0.0.0.0", "8080");
// 	return 0;
// }
