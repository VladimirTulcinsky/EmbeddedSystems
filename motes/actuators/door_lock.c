#include "contiki.h"
#include "lib/random.h"
#include "sys/ctimer.h"
#include "net/ipv6/uip.h"
#include "net/ipv6/uip-ds6.h"
#include "net/ipv6/uip-udp-packet.h"
#include "sys/ctimer.h"
#include "dev/leds.h"
#include "dev/button-sensor.h"

#include <stdio.h>
#include <string.h>

#include <time.h>
#include <stdlib.h>

#define UDP_CLIENT_PORT 8765
#define UDP_SERVER_PORT 5678

#define DEBUG DEBUG_PRINT
#include "net/ipv6/uip-debug.h"

#define MAX_PAYLOAD_LEN 3

/*---------------------------------------------------------------------------*/
PROCESS(udp_server_process, "UDP server process");
AUTOSTART_PROCESSES(&udp_server_process);
/*---------------------------------------------------------------------------*/

static struct uip_udp_conn *server_conn;
static char buf[MAX_PAYLOAD_LEN];
static uint16_t len;

static void
send_connection()
{
    char buf[MAX_PAYLOAD_LEN];
    int data_to_send = 000000000000110000000000;
    uip_ipaddr_t serveraddr;
    uip_ip6addr(&serveraddr, 0xbbbb, 0, 0, 0, 0, 0, 0, 1);

    sprintf(buf, "%d", data_to_send);
    uip_udp_packet_sendto(server_conn, buf, strlen(buf), &serveraddr, UIP_HTONS(UDP_SERVER_PORT));
}

static void
send_lampStatus(int value)
{
    char buf[MAX_PAYLOAD_LEN];
    int data_to_send = value;
    uip_ipaddr_t serveraddr;
    uip_ip6addr(&serveraddr, 0xbbbb, 0, 0, 0, 0, 0, 0, 1);

    sprintf(buf, "d=%d", data_to_send);
    uip_udp_packet_sendto(server_conn, buf, strlen(buf), &serveraddr, UIP_HTONS(UDP_SERVER_PORT));
}

static void
tcpip_handler(void)
{
    memset(buf, 0, MAX_PAYLOAD_LEN);
    if (uip_newdata())
    {
        len = uip_datalen();
        memcpy(buf, uip_appdata, len);

        int x = atoi(buf);
        if (x)
        {
            PRINTF("DOOR OPEN");
            leds_on(LEDS_GREEN);
            leds_off(LEDS_RED);
            send_lampStatus(1);
        }
        else
        {
            PRINTF("DOOR CLOSE");
            leds_off(LEDS_GREEN);
            leds_on(LEDS_RED);
            send_lampStatus(0);
        }

#if SERVER_REPLY
        uip_ipaddr_copy(&server_conn->ripaddr, &UIP_IP_BUF->srcipaddr);
        server_conn->rport = UIP_UDP_BUF->srcport;

        uip_udp_packet_send(server_conn, buf, len);
        /* Restore server connection to allow data from any node */
        uip_create_unspecified(&server_conn->ripaddr);
        server_conn->rport = 5678;
#endif
    }
    return;
}

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(udp_server_process, ev, data)
{

    PROCESS_BEGIN();
    PRINTF("Starting the server\n");

    server_conn = udp_new(NULL, UIP_HTONS(0), NULL);
    udp_bind(server_conn, UIP_HTONS(3000));

    PRINTF("Listen port: 3000, TTL=%u\n", server_conn->ttl);

    while (1)
    {
        PROCESS_YIELD();

        if (connected == 0)
        {
            send_connection(); // Send connection to the server to say this device exist

            memset(buf, 0, MAX_PAYLOAD_LEN);
            len = uip_datalen();
            memcpy(buf, uip_appdata, len);

            int value = atoi(buf);
            printf("%d\n", value);
        }
        else
        {
            if (ev == tcpip_event)
            {
                tcpip_handler();
            }
        }
    }

    PROCESS_END();
}
/*---------------------------------------------------------------------------*/