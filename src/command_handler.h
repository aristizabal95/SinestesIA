#ifndef COMMAND_HANDLER_H
#define COMMAND_HANDLER_H

void stop(int signum);
void error(char *msg);
void *servo_threadfunc(void *arg);
void *tcp_threadfunc(void *arg);

#endif
