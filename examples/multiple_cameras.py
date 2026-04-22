from machine import Pin, SPI, reset
from camera import *
fm = FileManager()

# Configuration for ESP 32S (NodeMCU) using VSPI w/ CS pins 16, 17, and 4
spi = SPI(2, baudrate=800000, polarity=0, phase=0, bits=8, firstbit=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
cs_pins = [ Pin(16, Pin.OUT), Pin(17, Pin.OUT), Pin(4, Pin.OUT) ]
onboard_LED = Pin(2,  Pin.OUT)

# This example uses 3 cameras at the noted CS pins, however feel free to add/remove.
# All that is required is turning ON/OFF the other CS pins for multiple cameras to work at once.

# Initialize cameras at pins
cams = [
    Camera(spi, cs_pins[0], debug_text_enabled=True), 
    Camera(spi, cs_pins[1], debug_text_enabled=True),
    Camera(spi, cs_pins[2], debug_text_enabled=True)
]

# Take captures with all cameras, in succession
def captureAll(cams):
    for current_cam_index, cam_to_capture in enumerate(cams):
        for i, cam_to_disable in enumerate(cams):
            if i != current_cam_index: cam_to_disable.cs.on() # Make all CS pins on/high except the camera taking the image
        sleep_ms(50)
        cam_to_capture.capture_jpg()

def saveAll(cams):
    for current_cam_index, cam_to_save in enumerate(cams):
        for i, cam_to_disable in enumerate(cams):
            if i != current_cam_index: cam_to_disable.cs.on() # Make all CS pins on/high except the camera taking the image
        cam_to_save.save_jpg(fm.new_jpg_filename('image'))

    
onboard_LED.on()
captureAll(cams)
saveAll(cams)
onboard_LED.off()