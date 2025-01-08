from machine import Pin, SPI
from camera import *
#Baud 8000000

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

spi = SPI(2,sck=Pin(12), miso=Pin(13), mosi=Pin(11), baudrate=100000)
cs = Pin(17, Pin.OUT)

# button = Pin(15, Pin.IN,Pin.PULL_UP)
onboard_LED = Pin(48, Pin.OUT)

cam = Camera(spi, cs, debug_information=True)
'''
RESOLUTION_160X120 = 0X00
RESOLUTION_320X240 = 0X01
RESOLUTION_640X480 = 0X02
RESOLUTION_1280X720 = 0X03
'''


cam.resolution = '320X240'
cam.resolution

start_time_capture = utime.ticks_ms()

onboard_LED.on()
cam.capture_jpg()
sleep_ms(200)
cam.saveJPG('image.jpg')
onboard_LED.off()

total_time_ms = utime.ticks_diff(utime.ticks_ms(), start_time_capture)
print('Time take: {}s'.format(total_time_ms/1000))