# Arducam port to Pico

from machine import Pin, SPI, reset
# Developing on 1.24
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


################################################################## CODE ACTUAL ##################################################################
#Pi pico
'''
spi = SPI(0,sck=Pin(18), miso=Pin(16), mosi=Pin(19), baudrate=8000000)
cs = Pin(17, Pin.OUT)

# button = Pin(15, Pin.IN,Pin.PULL_UP)
onboard_LED = Pin(25, Pin.OUT)
'''
#ESP 32 S3
spi = SPI(2,sck=Pin(12), miso=Pin(13), mosi=Pin(11), baudrate=8000000)
cs = Pin(17, Pin.OUT)

# button = Pin(15, Pin.IN,Pin.PULL_UP)
onboard_LED = Pin(48, Pin.OUT)

#Adds _# to end of filename, is same file name is used more than once images are stacked in the same file and only the first image renders while the size grows
fm = FileManager()

cam = Camera(spi, cs, debug_information=True)
cam.resolution = '320X240'
#cam.resolution = '640x480'
# cam.set_filter(cam.SPECIAL_REVERSE)
cam.set_brightness_level(cam.BRIGHTNESS_PLUS_4)
cam.set_contrast(cam.CONTRAST_MINUS_3)


onboard_LED.on()
cam.capture_jpg()
sleep_ms(50)
#cam.saveJPG('image.jpg') #fixed name
cam.saveJPG(fm.new_jpg_fn('image')) #updating name
onboard_LED.off()


#################################################################################################################################################
'''
Benchmarks
- Default SPI speed (1000000?), cam.resolution = '640X480', no burst read (camera pointed at roof) ==== TIME: ~7.8 seconds
- Increased speed (8000000), cam.resolution = '640X480', no burst read (camera pointed at roof) ==== TIME: ~7.3 seconds

'''
