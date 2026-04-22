'''
Basic use of the ArduCam Mega (3MP/5MP) SPI Camera
'''

from machine import Pin, SPI, reset
from camera import *

'''
Pinout for Raspberry Pi Pico

# Power
VCC - 3V3 - red
GND - GND - black

# SPI(0)

SCK - GP18 - White
MISO - RX - GP16 - Brown
MOSI - TX - GP19 - Yellow
CS - GP17 - Orange
'''

# Initialise hardware, high SPI baudrate to save images faster
spi = SPI(0,sck=Pin(18), miso=Pin(16), mosi=Pin(19), baudrate=8000000)
cs = Pin(17, Pin.OUT)

onboard_LED = Pin(25, Pin.OUT)

# Setup Camera
cam = Camera(spi, cs)

# sleep_ms(500) # Uncomment this line for the 5MP Variant

# Our recommended image capturing process
onboard_LED.on() # Turn the LED when taking a photo

cam.capture_jpg() # Send a command to the camera to capture the photo - saving is done...

sleep_ms(50)

cam.save_jpg('image.jpg') # ...seperately

onboard_LED.off()


