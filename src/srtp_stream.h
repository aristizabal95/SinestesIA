#ifndef SRTP_STREAM_H
#define SRTP_STREAM_H

#include "rtp.h"

rtp_sender_t configSRTP(int *sock);

void runStream(rtp_sender_t snd);

int killSRTP(rtp_sender_t snd, int sock);

void *srtp_threadfunc(void *arg);

#endif 
