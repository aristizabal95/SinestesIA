#ifndef WEBSOCKET_STREAM_H
#define WEBSOCKET_STREAM_H

void streaming_connect_cb(libwebsock_client_state *state);

void send_streaming(libwebsock_client_state *state, char **messageBuff);

void createWebSocket(char* ip, char* port);

void *websocket_threadfunc(void *arg);

#endif
