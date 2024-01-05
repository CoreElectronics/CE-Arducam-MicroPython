from machine import Pin, SPI
from Camera import *

spi = SPI(0,sck=Pin(18), miso=Pin(16), mosi=Pin(19), baudrate=8000000)
cs = Pin(17, Pin.OUT)

# button = Pin(15, Pin.IN,Pin.PULL_UP)
onboard_LED = Pin(25, Pin.OUT)

cam = Camera(spi, cs)

cam.resolution = '640x480'

onboard_LED.on()
cam.capture_jpg()
sleep_ms(50)
cam.saveJPG('image.jpg')
onboard_LED.off()
