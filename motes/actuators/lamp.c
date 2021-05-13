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

#define MAX_PAYLOAD_LEN 5

/*---------------------------------------------------------------------------*/
PROCESS(udp_server_process, "UDP server process");
AUTOSTART_PROCESSES(&udp_server_process);
/*---------------------------------------------------------------------------*/

static struct uip_udp_conn *server_conn;
static char buf[MAX_PAYLOAD_LEN];
static uint16_t len;
int sequence = 0;
typedef struct FormatData
{
    char type_of_response[3];
    char sequence_number[9];
    char type_of_data[5];
    char payload[11];
} format_data;

/*---------------------------------------------------------------------------*/
//THIS SECTION WILL CONTAIN CONVERTERS BETWEEN BASE 2, 10 AND 16
//THIS SECTION IS IDENTICAL FOR EVERY MOTE
/*---------------------------------------------------------------------------*/

//This will take a hexadecimal and bit char, it will translate the hexadecimal into binary and put it into the binary char
static void hex2bin(char *hexdec, char *bits)
{

    int i = 0;

    while (hexdec[i])
    {
        printf("\n iteration %d string is: %s", i, bits);

        switch (hexdec[i])
        {
        case '0':
            strcat(bits, "0000");
            break;
        case '1':
            strcat(bits, "0001");
            break;
        case '2':
            strcat(bits, "0010");
            break;
        case '3':
            strcat(bits, "0011");
            break;
        case '4':
            strcat(bits, "0100");
            break;
        case '5':
            strcat(bits, "0101");
            break;
        case '6':
            strcat(bits, "0110");
            break;
        case '7':
            strcat(bits, "0111");
            break;
        case '8':
            strcat(bits, "1000");
            break;
        case '9':
            strcat(bits, "1001");
            break;
        case 'A':
        case 'a':
            strcat(bits, "1010");
            break;
        case 'B':
        case 'b':
            strcat(bits, "1011");
            break;
        case 'C':
        case 'c':
            strcat(bits, "1100");
            break;
        case 'D':
        case 'd':
            strcat(bits, "1101");
            break;
        case 'E':
        case 'e':
            strcat(bits, "1110");
            break;
        case 'F':
        case 'f':
            strcat(bits, "1111");
            break;
        default:
            printf("\nInvalid hexadecimal digit %c",
                   hexdec[i]);
        }
        i++;
    }
}

/*---------------------------------------------------------------------------*/

//This takes a binary char string and return it as a decimal integer
static int
bin2dec(char *binary_str)
{
    char *bin = binary_str;
    char *a = bin;
    int num = 0;
    do
    {
        int b = *a == '1' ? 1 : 0;
        num = (num << 1) | b;
        a++;
    } while (*a);
    printf("%X\n", num);
    return num;
}

/*---------------------------------------------------------------------------*/

//This function takes a decimal int, and returns an int with the decimal in binary values.
//We made sure we never give it a big integer, as that could cause problems.
int dec2bin(int decimalnum)
{
    int binarynum = 0;
    int rem, temp = 1;

    while (decimalnum != 0)
    {
        rem = decimalnum % 2;
        decimalnum = decimalnum / 2;
        binarynum = binarynum + rem * temp;
        temp = temp * 10;
    }
    return binarynum;
}

/*---------------------------------------------------------------------------*/
//THIS SECTION WILL CONTAIN ALL THE NETWORKING LOGIC
//THIS SECTION IS IDENTICAL FOR EVERY MOTE
/*---------------------------------------------------------------------------*/

static void
send_message(int value, int response_type)
{
    uip_ipaddr_t serveraddr;
    uip_ip6addr(&serveraddr, 0xbbbb, 0, 0, 0, 0, 0, 0, 1);

    char bin_message[25];

    //Handles the type of message. Ack, no ack etc..
    format_data data_to_send;
    sprintf(data_to_send.type_of_response, "%d", response_type);

    //Handles the sequence number, should be identical to sequence number received
    int binary_sequence = dec2bin(sequence);
    sprintf(data_to_send.sequence_number, "%08d", binary_sequence);

    //Handles adding the device ID
    strcpy(data_to_send.type_of_data, "0010"); //TODO this is still hard coded

    //Handles the payload
    int binary_payload = dec2bin(value);
    sprintf(data_to_send.payload, "%010d", binary_payload);

    sprintf(bin_message, "%s%s%s%s", data_to_send.type_of_response, data_to_send.sequence_number, data_to_send.type_of_data, data_to_send.payload);

    int decimal_message = bin2dec(bin_message);
    char hex_message[7];
    sprintf(hex_message, "%06x", decimal_message);
    uip_udp_packet_sendto(server_conn, hex_message, strlen(hex_message), &serveraddr, UIP_HTONS(UDP_SERVER_PORT));
}
/*---------------------------------------------------------------------------*/

static void process_data(format_data *fd, char *binary_str)
{
    printf("%s \n", binary_str);

    memcpy(fd->type_of_response, &binary_str[0], 2);

    memcpy(fd->sequence_number, &binary_str[2], 8);

    //This was done with a workaround because it kept adding random symbols if done with one memcpy
    char tmp1[3];
    char tmp2[3];
    memcpy(tmp1, &binary_str[10], 2);
    memcpy(tmp2, &binary_str[12], 2);
    strcat(tmp1, tmp2);
    strcat(fd->type_of_data, tmp1);

    memcpy(fd->payload, &binary_str[14], 10);

    printf("%s \n", fd->type_of_response);
    printf("%s \n", fd->sequence_number);
    printf("%s \n", fd->type_of_data);
    printf("%s \n", fd->payload);
}
/*---------------------------------------------------------------------------*/

static void
tcpip_handler(void)
{
    memset(buf, 0, MAX_PAYLOAD_LEN);
    if (uip_newdata())
    {
        len = uip_datalen();
        memcpy(buf, uip_appdata, len);
        printf("this is the beautiful lamp %s ", buf);
        char bits[24] = {0};
        hex2bin(buf, bits);
        printf("the bits are: %s \n", bits);
        format_data fd;
        process_data(&fd, bits);

        int recieved_sequence_nb = bin2dec(fd.sequence_number);
        if (recieved_sequence_nb < sequence)
        {
            printf("SEQUENCE NUMBER TOO LOW, RETURNING");
            return;
        }
        sequence = bin2dec(fd.sequence_number);

        if (strcmp(fd.type_of_data, "0010")) //TODO change this to device ID as well
        {
            printf("THIS MESSAGE WAS NOT INTENDED FOR THIS DEVICE, RETURNING");
            return;
        }

        int x = atoi(fd.payload);
        if (x)
        {
            PRINTF("LIGHTS ON");
            leds_on(LEDS_RED);
            if (strcmp(fd.type_of_response, "00") == 0)
            {
                send_message(1, 10);
            }
        }
        else
        {
            PRINTF("LIGHTS OFF");
            leds_off(LEDS_RED);
            if (strcmp(fd.type_of_response, "00") == 0)
            {
                send_message(0, 10);
            }
        }
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
        if (ev == tcpip_event)
        {
            tcpip_handler();
        }
    }

    PROCESS_END();
}
/*---------------------------------------------------------------------------*/