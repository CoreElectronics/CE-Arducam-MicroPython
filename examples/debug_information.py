'''
Demonstrating the `debug_text_enabled=True` argument in the Camera initialisation
'''

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

spi = SPI(0,sck=Pin(18), miso=Pin(16), mosi=Pin(19), baudrate=7000000)
cs = Pin(17, Pin.OUT)

onboard_LED = Pin(15, Pin.OUT)

cam = Camera(spi, cs, debug_text_enabled=True)


cam.resolution = '320X240'
cam.resolution

start_time_capture = utime.ticks_ms()

onboard_LED.on()
cam.capture_jpg()
sleep_ms(200)
cam.save_jpg('image.jpg')
onboard_LED.off()

total_time_ms = utime.ticks_diff(utime.ticks_ms(), start_time_capture)
print('Time taken: {}s'.format(total_time_ms/1000))

'''
Benchmarks
- Default SPI speed (1000000?), cam.resolution = '640X480', no burst read (camera pointed at roof) ==== TIME: ~7.8 seconds
- Increased speed (8000000), cam.resolution = '640X480', no burst read (camera pointed at roof) ==== TIME: ~7.3 seconds

'''