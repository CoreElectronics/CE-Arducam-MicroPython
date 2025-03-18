# A single, simple photo

# Import required modules
from machine import Pin, SPI, reset
from Camera import *

spi = SPI(0,sck=Pin(18), miso=Pin(16), mosi=Pin(19), baudrate=8000000) # Pins for the Raspberry Pi Pico
cs = Pin(17, Pin.OUT)

# A manager to handling new photos being taken
filemanager = FileManager()

# Create a "Camera" object with the SPI interface defined above
cam = Camera(spi, cs) # Default resolution of 640x480

# Capture a photo - this only takes a moment
cam.capture_jpg()

# To let any data settle
sleep_ms(5)

# Save the photo into the onboard memory
cam.save_JPG_burst(fm.new_jpg_filename('image'))