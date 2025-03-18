# ArduCam Mega Cameras for microcontrollers


from machine import Pin, SPI, reset
from Camera import *

spi = SPI(0,sck=Pin(18), miso=Pin(16), mosi=Pin(19), baudrate=8000000) # Pins for the Raspberry Pi Pico
cs = Pin(17, Pin.OUT)



#Adds _# to end of filename, is same file name is used more than once images are stacked in the same file and only the first image renders while the size grows
fm = FileManager()

cam = Camera(spi, cs)

# cam.resolution = '1920x1080'
cam.resolution = '640x480'
# cam.set_filter(cam.SPECIAL_REVERSE)
# cam.set_brightness_level(cam.BRIGHTNESS_PLUS_4)
# cam.set_contrast(cam.CONTRAST_MINUS_3)

print("pic1")
onboard_LED.on()
cam.capture_jpg()
sleep_ms(50)
cam.save_JPG_burst(fm.new_jpg_filename('image'))
onboard_LED.off()
sleep_ms(500)

print("pic2")
onboard_LED.on()
cam.capture_jpg()
sleep_ms(50)
cam.save_JPG_burst(fm.new_jpg_filename('image'))
onboard_LED.off()


#################################################################################################################################################
'''
Benchmarks
- Default SPI speed (1000000?), cam.resolution = '640X480', no burst read (camera pointed at roof) ==== TIME: ~7.8 seconds
- Increased speed (8000000), cam.resolution = '640X480', no burst read (camera pointed at roof) ==== TIME: ~7.3 seconds

'''
