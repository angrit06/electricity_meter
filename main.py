from machine import Pin
import time
import network
import machine
from umqtt.robust import MQTTClient
import ubinascii
import adafruit_mlx90393


# def magnetic():
#     I2C_BUS = busio.I2C(board.SCL, board.SDA)
#     SENSOR = adafruit_mlx90393.MLX90393(I2C_BUS, gain=adafruit_mlx90393.GAIN_1X)
#     while True:
#         MX, MY, MZ = SENSOR.magnetic
#         print("[{}]".format(time.monotonic()))
#         print("X: {} uT".format(MX))
#         print("Y: {} uT".format(MY))
#         print("Z: {} uT".format(MZ))
#         # Display the status field if an error occured, etc.
#         if SENSOR.last_status > adafruit_mlx90393.STATUS_OK:
#             SENSOR.display_status()
#         time.sleep(1.0)

def blink(periods, frequenz):
    led = Pin(2, Pin.OUT)
    print("... blink ... ")
    for i in range(periods):
        led(0)
        time.sleep(frequenz)
        led(1)
        time.sleep(frequenz)


def connect_network():
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    print("sta active: ", sta_if.active())
    print("ap active: ", ap_if.active())
    print("network config: ", ap_if.ifconfig())

    # activate connection
    sta_if.active(True)
    ap_if.active(False)
    print("try to connect ...")
    sta_if.connect('WLAN-886311', '59696816459236044341')
    print("connected: ", sta_if.isconnected())
    while not sta_if.isconnected():
        print("... try to connect again ... ")
        blink(periods=10, frequenz=0.25)
        sta_if.connect('WLAN-886311', '59696816459236044341')
        print("connected: ", sta_if.isconnected())
    if sta_if.isconnected():
        print("... connected!")
        print("network config: ", sta_if.ifconfig())
        blink(periods=10, frequenz=0.15)


def mqtt_client():
    id = ubinascii.hexlify(machine.unique_id())
    print(id.decode('utf8'))
    mqtt_client = MQTTClient(id.decode('utf8'), "raspberrypi")
    mqtt_client.connect()
    return mqtt_client

if __name__ == '__main__':
    blink(periods=5, frequenz=1)
    connect_network()
    mqtt_client = mqtt_client()
    mqtt_client.publish(topic="/cellar/electricity_meter/X", msg="test")
    # magnetic()
    # mqtt_client.publish(topic="/cellar/electricity_meter/test", msg="test!")
    blink(periods=10, frequenz=0.4)
