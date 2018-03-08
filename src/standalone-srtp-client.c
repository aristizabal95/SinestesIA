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

//Set key to predetermined value
uint8_t key[30] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
                   0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
                   0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
                   0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D};

int main(){
	srtp_init();

	memset(&policy, 0x0, sizeof(srtp_policy_t));

	crypto_policy_set_rtp_default(&policy.rtp);
	crypto_policy_set_rtcp_default(&policy.rtcp);
	policy.ssrc.type = ssrc_specific;
	policy.ssrc.value = ssrc;
	policy.key = key;
	policy.next = NULL;

	srtp_create(&session, &policy);

	while(1) {
		char rtp_buffer[2048];
		unsigned len;

		len = get_rtp_packet(rtp_buffer);
		char* msg = "Hello there\n";
		int len = strlen(msg);
	}
}
