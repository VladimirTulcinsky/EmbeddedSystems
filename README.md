# How to build

## Prior configuration
* sudo usermod -aG docker "your-user"
* in makefile of border-router comment the line PLATFORMS_EXCLUDE = nrf52dk z1
* modify or create /etc/docker/daemon.json by adding :
```
{
"ipv6": true,
"fixed-cidr-v6": "fd00::/64"
}
```
* restart by typing: sudo systemctl restart docker

## Cooja
Start Cooja with *contiker cooja*.
Steps have to be followed in this order for the project to work.

1. Create a mote with border-router.c
2. Create a proximity mote with sensor.c
    * In the file sensor.c set *USE_PROXIMITY to 1* and *USE_NOISE to 0*
3. Create a noise mote with sensor.c
    * In the file sensor.c set *USE_PROXIMITY to 0* and *USE_NOISE to 1*

Start the simulation on full speed to pace up the networking configuration, but once that's done set the speed to 10%!

## Tunslip
1. Get the container name by executing *docker ps*
2. Execute *docker container inspect <name-of-container>*
3. Get the ip address of the container
4. In _contiki-ng/tools/serial-io_ type and execute sudo *./tunslip6 -a <ip-address-of-contaier> -p <port-of-border-router> (probably something in the 6000x) bbbb::1/64*
5. Now data can flow between the container and the host

## Python server
1. Set the port to the appropriate port of the border router.
2. Run main.py

### Subscription to sensors
#### Proximity
You can subscribe to the proximity sensor. If you have subscribed to that particular node, and the sensor button is clicked (in the Cooja ecosystem),a led will light up in order to simulate detection and a message will display to notify movement. After 5 seconds, detection will disappear and the movement flag will be reset.

#### Noise
You can subscribe to the noise sensor. If you have subscribed to that particular node, a message will display the current detected dbA and tell you when it exceeds 95 dbA.

# Protocol
Sensors are only pushing information
That's why a mqtt like protocol is recommended.
If multiple users subscribe to one topic, it requires less resources from the sensor that works on battery because the broker-like device takes care of pushing the data to the multiple subscribers.
This, if we make the hypothesis that the broker-like device is connected to a power source.
In this case, only one user interacts with the interface. If multiple users were to use the program it would be easily extendable.


# Encountered problems
## Data format
For whatever reason we can't restrict the data to sole integers. We have to prepend it by text or else tunslip crashes.

# TODO:
Complete steps and modify at each step
