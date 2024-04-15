# Arducam port to Pico

from machine import Pin, SPI, reset
# Developing on 1.19

'''
#################### PINOUT ####################
Camera pin - Pico Pin
VCC - 3V3
GND - GND
SCK - GP18 - white
MISO - RX - GP16 - brown
MOSI - TX - GP19 - yellow
CS - GP17 - orange
'''


################################################################## CODE ACTUAL ##################################################################
spi = SPI(0,sck=Pin(18), miso=Pin(16), mosi=Pin(19), baudrate=8000000)
cs = Pin(17, Pin.OUT)

# button = Pin(15, Pin.IN,Pin.PULL_UP)
onboard_LED = Pin(25, Pin.OUT)

cam = Camera(spi, cs)

cam.resolution = '640x480'
# cam.set_filter(cam.SPECIAL_REVERSE)
cam.set_brightness_level(cam.BRIGHTNESS_PLUS_4)
cam.set_contrast(cam.CONTRAST_MINUS_3)


onboard_LED.on()
cam.capture_jpg()
sleep_ms(50)
cam.saveJPG('image.jpg')
onboard_LED.off()


#################################################################################################################################################
'''
Benchmarks
- Default SPI speed (1000000?), cam.resolution = '640X480', no burst read (camera pointed at roof) ==== TIME: ~7.8 seconds
- Increased speed (8000000), cam.resolution = '640X480', no burst read (camera pointed at roof) ==== TIME: ~7.3 seconds

'''