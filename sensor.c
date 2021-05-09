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

/*---------------------------------------------------------------------------*/
#define USE_PROXIMITY 0
#define USE_NOISE 1
/*---------------------------------------------------------------------------*/

#define DEBUG DEBUG_PRINT
#include "net/ipv6/uip-debug.h"

#define MAX_PAYLOAD_LEN 3

static struct uip_udp_conn *client_conn;
static uip_ipaddr_t server_ipaddr;

/*---------------------------------------------------------------------------*/
PROCESS(udp_client_process, "UDP client process");
AUTOSTART_PROCESSES(&udp_client_process);
/*---------------------------------------------------------------------------*/
static void
tcpip_handler(void)
{
    char *str;

    if (uip_newdata())
    {
        str = uip_appdata;
        str[uip_datalen()] = '\0';
        printf("DATA recv '%s'\n", str);
    }
}
/*---------------------------------------------------------------------------*/
#if USE_NOISE
static int
get_noise(void)
{
    int data_to_send = random_rand() % 120;
    return data_to_send;
}

/*---------------------------------------------------------------------------*/
static void
send_noise(void *ptr)
{
    char buf[MAX_PAYLOAD_LEN];
    int data_to_send;

    data_to_send = get_noise();
    PRINTF("noise = %d'\n'", data_to_send);

    PRINTF("DATA send to %d 'Hello %d'\n",
           client_conn->ripaddr.u8[15], data_to_send);
    sprintf(buf, "d=%d", data_to_send);
    uip_udp_packet_sendto(client_conn, buf, strlen(buf),
                          &server_ipaddr, UIP_HTONS(UDP_SERVER_PORT));
    struct ctimer *ct_ptr = ptr;
    ctimer_reset(ct_ptr);
}
#endif
/*---------------------------------------------------------------------------*/
#if USE_PROXIMITY
static void
send_proximity(int value)
{
    char buf[MAX_PAYLOAD_LEN];
    int data_to_send = value;

    PRINTF("proximity = %d'\n'", data_to_send);

    PRINTF("DATA send to %d 'Hello %d'\n",
           client_conn->ripaddr.u8[15], data_to_send);
    sprintf(buf, "d=%d", data_to_send);
    uip_udp_packet_sendto(client_conn, buf, strlen(buf),
                          &server_ipaddr, UIP_HTONS(UDP_SERVER_PORT));
}
#endif
/*---------------------------------------------------------------------------*/
static void
print_local_addresses(void)
{
    int i;
    uint8_t state;

    PRINTF("Client IPv6 addresses: ");
    for (i = 0; i < UIP_DS6_ADDR_NB; i++)
    {
        state = uip_ds6_if.addr_list[i].state;
        if (uip_ds6_if.addr_list[i].isused &&
            (state == ADDR_TENTATIVE || state == ADDR_PREFERRED))
        {
            PRINT6ADDR(&uip_ds6_if.addr_list[i].ipaddr);
            PRINTF("\n");
            /* hack to make address "final" */
            if (state == ADDR_TENTATIVE)
            {
                uip_ds6_if.addr_list[i].state = ADDR_PREFERRED;
            }
        }
    }
}
/*---------------------------------------------------------------------------*/
static void
set_global_address(void)
{
    uip_ipaddr_t ipaddr;

    uip_ip6addr(&ipaddr, 0xbbbb, 0, 0, 0, 0, 0, 0, 0);
    uip_ds6_set_addr_iid(&ipaddr, &uip_lladdr);
    uip_ds6_addr_add(&ipaddr, 0, ADDR_AUTOCONF);

    /* set server address */
    uip_ip6addr(&server_ipaddr, 0xbbbb, 0, 0, 0, 0, 0, 0, 1);
}
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(udp_client_process, ev, data)
{
#if USE_NOISE
    static struct ctimer ct;
    void *ct_ptr = &ct;
    ctimer_set(&ct, CLOCK_SECOND * 5, send_noise, ct_ptr);
#endif

#if USE_PROXIMITY
    SENSORS_ACTIVATE(button_sensor);
#endif

    PROCESS_BEGIN();

    // PROCESS_PAUSE();

    set_global_address();

    PRINTF("UDP client process started\n");

    print_local_addresses();

    /* new connection with remote host */
    client_conn = udp_new(NULL, UIP_HTONS(UDP_SERVER_PORT), NULL);
    udp_bind(client_conn, UIP_HTONS(UDP_CLIENT_PORT));

    PRINTF("Created a connection with the server ");
    PRINT6ADDR(&client_conn->ripaddr);
    PRINTF(" local/remote port %u/%u\n",
           UIP_HTONS(client_conn->lport), UIP_HTONS(client_conn->rport));

    while (1)
    {

        PROCESS_WAIT_EVENT();
        if (ev == tcpip_event)
        {
            tcpip_handler();
        }
#if USE_PROXIMITY

        static uint32_t seconds = 5;
        static struct etimer et; // Define the timer

        if (ev == sensors_event)
        {
            if (data == &button_sensor)
            {
                leds_toggle(LEDS_RED);
                send_proximity(1);
                etimer_set(&et, CLOCK_SECOND * seconds);
            }
        }

        if (etimer_expired(&et))
        {
            printf("timer");
            leds_toggle(LEDS_RED);
            send_proximity(0);
        }
#endif
    }

    PROCESS_END();
}
/*---------------------------------------------------------------------------*/