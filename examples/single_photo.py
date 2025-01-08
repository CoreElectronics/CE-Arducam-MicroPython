
from machine import Pin, SPI
from camera import *

'''
#################### PINOUT ####################
Camera pin - Pico Pin
VCC - 3V3 - red
GND - GND - black
SPI - 0
SCK - GP18 - white
MISO - RX - GP16 - brown
MOSI - TX - GP19 - yellow
CS - GP17 - orange

Camera pin - ESP32 S3
VCC - 3V3 - red
GND - GND - black
SPI - 2
SCK - GP12 - white
MISO - RX - GP13 - brown
MOSI - TX - GP11 - yellow
CS - GP17 - orange
'''

spi = SPI(2,sck=Pin(12), miso=Pin(13), mosi=Pin(11), baudrate=8000000)
cs = Pin(17, Pin.OUT)

# button = Pin(15, Pin.IN,Pin.PULL_UP)
onboard_LED = Pin(48, Pin.OUT)

cam = Camera(spi, cs)

cam.resolution = '640x480'

onboard_LED.on()
cam.capture_jpg()
sleep_ms(50)
cam.saveJPG('image.jpg')
onboard_LED.off()
