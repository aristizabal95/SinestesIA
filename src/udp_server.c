#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <netdp.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define BUFLEN 512
#define PORT 8888

void die(char *s){
	perror(s);
	exit(1);
}

int main(void) {
	struct sockaddr_in si_me, si_other;

	int s, i, slen = sizeof(si_other), recv_len;
	char buf[BUFLEN];``
}
