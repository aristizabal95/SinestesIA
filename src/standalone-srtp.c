#include "integers.h"
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <signal.h>
#include <stddef.h>

#include <string.h>
#include <time.h>

#ifndef HAVE_UNISTD_H
#include <unistd.h>
#elif defined(_MSC_VER)
#include <io.h>
#define close _close
#endif
#ifdef HAVE_SYS_SOCKET_H
# include <sys/socket.h>
#endif
#ifdef HAVE_NETINET_IN_H
# include <netinet/in.h>
#elif defined HAVE_WINSOCK2_H
# include <winsock2.h>
# include <ws2tcpip.h>
# define RTPW_USE_WINSOCK2	1
#endif
#ifdef HAVE_ARPA_INET_H
# include <arpa/inet.h>
#endif

#include "srtp.h"           
#include "rtp.h"
#include "crypto_kernel.h"
#include "getopt_s.h"
#include "datatypes.h"

#define IP_ADDRESS '0.0.0.0'
#define PORT 6969

srtp_t session;
srtp_policy_t policy;
uint32_t ssrc = 0xdeadbeef;

typedef enum { sender, receiver, unkown } program_type;

//Set key to predetermined value
uint8_t key[30] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
                   0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
                   0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
                   0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D};

int main(){
	int sock, ret;
	struct in_addr rcvr_addr;
	struct sockaddr_in name;
	struct ip_mreq mreq;
	program_type prog_type = sender;
	sec_serv_t sec_servs = sec_serv_none;
	ret = srtp_init();
	if (ret) {
		printf("Could not initialize srtp\n");
		exit(1);
	}

	rcvr_addr.s_addr = inet_addr(IP_ADDRESS);
	if (rcvr_addr.s_addr == 0xffffffff) {
		printf("Cannot parse IPv4\n");
		exit(1);
	}

	sock = socket(PF_INET, SOCK_DGRAM, IPPROTO_UDP);
	if (sock < 0){
		printf("Could not open socket\n");
		exit(1);
	}

	name.sin_addr = IP_ADDRESS;
	name.sin_family = PF_INET;
	name.sin_port = htons(PORT);

	memset(&policy, 0x0, sizeof(srtp_policy_t));


    policy.key                 = (uint8_t *)key;
    policy.ssrc.type           = ssrc_specific;
    policy.ssrc.value          = ssrc;
    policy.rtp.cipher_type     = NULL_CIPHER;
    policy.rtp.cipher_key_len  = 0; 
    policy.rtp.auth_type       = NULL_AUTH;
    policy.rtp.auth_key_len    = 0;
    policy.rtp.auth_tag_len    = 0;
    policy.rtp.sec_serv        = sec_serv_none;   
    policy.rtcp.cipher_type    = NULL_CIPHER;
    policy.rtcp.cipher_key_len = 0; 
    policy.rtcp.auth_type      = NULL_AUTH;
    policy.rtcp.auth_key_len   = 0;
    policy.rtcp.auth_tag_len   = 0;
    policy.rtcp.sec_serv       = sec_serv_none;   
    policy.window_size         = 0;
    policy.allow_repeat_tx     = 0;
    policy.ekt                 = NULL;
    policy.next                = NULL;

	srtp_create(&session, &policy);

	while(1) {
		char* msg = "Hello there\n";
		unsigned len = strlen(msg);
		srtp_protect(session, msg, &len);
		send_srtp_packet(msg, len);
	}
}
