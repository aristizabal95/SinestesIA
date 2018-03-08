// SRTP_STREAM
// Functions created with the purpose of streaming or sending live video/depth/audio data through SRTP.
// This stream will be sent async, and requires a message to be fully built beforehand.
#ifndef SRTP_STREAM
#define SRTP_STREAM


#include <stdio.h>          /* for printf, fprintf */
#include <stdlib.h>         /* for atoi()          */
#include <errno.h>
#include <signal.h>         /* for signal()        */

#include <string.h>         /* for strncpy()       */
#include <time.h>	    /* for usleep()        */
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include "srtp.h"
#include "rtp.h"
#include "crypto_kernel.h"
#include "globals.h"
#include "srtp_stream.h"
#include <pthread.h>

#endif

#define MAX_KEY_LEN 96
#define PORT 9999

rtp_sender_t configSRTP(int *sock) {
	// Handle all configuration necessary for secure real-time transfer of data
	struct in_addr rcvr_addr;

	struct sockaddr_in name;

	sec_serv_t sec_servs = sec_serv_none;
	char *input_key = "e87aec95b8ed151f263bad181ccd6c8deae14c18bb03e0deb8580c68a967"; // Hardcoded for now
	char *address = "0.0.0.0";
	char key[MAX_KEY_LEN];
	unsigned short port = 0;

	rtp_sender_t snd;
	srtp_policy_t policy;
	err_status_t status;
	int len;
	int expected_len;
	uint32_t ssrc= 0xdeadbeef;

	status = srtp_init();
	if (status) {
		printf("Error: srtp initialization failed with error code %d\n", status);
		exit(1);
	}

	sec_servs = sec_serv_conf_and_auth;

	port = PORT;

	if (0 == inet_aton(address, &rcvr_addr)) {
		fprintf(stderr, "Cannot parse IPv4 address %s\n", address);
		exit(1);
	}
	if (rcvr_addr.s_addr == INADDR_NONE) {
		fprintf(stderr, "address error\n");
		exit(1);
	}

	*sock = socket(PF_INET, SOCK_DGRAM, IPPROTO_UDP);
	if (sock < 0) {
		int err;
		err = errno;
		fprintf(stderr, "Couldn't open socket: %d\n", err);
		exit(1);
	}

	name.sin_addr = rcvr_addr;
	name.sin_family = PF_INET;
	name.sin_port = htons(port);

	crypto_policy_set_rtp_default(&policy.rtp);
	crypto_policy_set_rtcp_default(&policy.rtcp);

	policy.ssrc.type = ssrc_specific;
	policy.ssrc.value = ssrc;
	policy.key = (uint8_t *)key;
	policy.ekt = NULL; //Apparently  ekt is not working correctly atm
	policy.next = NULL;
	policy.window_size = 128; // for replay protection
	policy.allow_repeat_tx = 0; //May be necessary for audio/video/depth transmission
	policy.rtp.sec_serv = sec_servs;
	policy.rtcp.sec_serv = sec_serv_none; // Would be ideal to have srtcp enabled for integrity

	expected_len = policy.rtp.cipher_key_len*2;
	len = hex_string_to_octet_string(key, input_key, expected_len);

	//check that the length of the key is the expected length
	if (len != expected_len) {
		fprintf(stderr, "error: length of key does not match expected length. Should be %d, but is %d\n", expected_len, len);
		exit(1);
	}

	printf("set master key/salt to %s/", octet_string_hex_string(key, 16));
	printf("%s\n", octet_string_hex_string(key+16, 14));

	/* MUST CHECK IF THIS WORKS... NO EXPLANATION FOR 'BEW' */
	// memset(&local, 0, sizeof(struct sockaddr_in));
	// local.sin_addr.s_addr = htonl(INADDR_ANY);
	// local.sin_port = htons(port);
	// ret = bind(sock, (struct sockaddr *) &local, sizeof(struct sockaddr_in));
	// if (ret < 0) {
	// 	fprintf(stderr, "bind failed\n");
	// 	perror("");
	// 	exit(1);
	// }
	/* END OF BEW */

	snd = rtp_sender_alloc();
	if (snd == NULL) {
		fprintf(stderr, "error: malloc() failed\n");
		exit(1);
	}
	rtp_sender_init(snd, *sock, name, ssrc);
	status = rtp_sender_init_srtp(snd, &policy);
	if (status) {
		fprintf(stderr, "error: stp_create() failed with code %d\n", status);
		exit(1);
	}

	// If everything went right, return sender
	return snd;
}


void runStream(rtp_sender_t snd){
	while(!die){
		pthread_mutex_lock(&streaming_mutex);
		char *message = (char *)messageBuffer;
		if(messageReady) {
			rtp_sendto(snd, message, MESSAGE_LEN);
			messageReady = 0;
			printf("Message sent!");
		}
		pthread_mutex_unlock(&streaming_mutex);
	}
}

int killSRTP(rtp_sender_t snd, int sock) {
	int status, ret;
	rtp_sender_deinit_srtp(snd);
	rtp_sender_dealloc(snd);
	ret = close(sock);
	if (ret < 0) {
		fprintf(stderr, "failed to close socket\n");
		perror("");
	}

	status = srtp_shutdown();
	if (status) {
		printf("error: srtp could not shut down, error: %d\n", status);
		return 1;
	}
	return 0;
}

void *srtp_threadfunc(void *arg) {
	rtp_sender_t sender;
	int sock, ret;
	sender = configSRTP(&sock);
	runStream(sender);
	ret = killSRTP(sender, sock);
	if (ret != 0) {
		printf("could not gracefully shutdown SRTP\n");
	} 
	return NULL;
}
