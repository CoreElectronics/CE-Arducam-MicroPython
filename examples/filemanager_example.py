from machine import Pin, SPI
from time import sleep_ms
from camera import *

# Initialise Hardware
spi = SPI(0, sck=Pin(18), miso=Pin(16), mosi=Pin(19), baudrate=8000000)
cs = Pin(17, Pin.OUT)
onboard_LED = Pin(25, Pin.OUT)

# Setup Camera
cam = Camera(spi, cs)

# Start the FileManager
# It will read 'filemanager.log' to resume counting from where it left off before the last reboot.
fm = FileManager()

# Check how much free space is available
free_bytes = fm.filesystem_space()
free_mb_start = free_bytes / (1024 * 1024) # Convert to Megabytes
print("Free Space: {} MB".format(free_mb_start))

# sleep_ms(500) # Uncomment this line for the 5MP Variant

print("Starting photo sequence...")

# --- Sequence 1: The Loop (Tracking the 'burst' prefix) ---
print("Capturing 3 photos in a 'burst'...")
for i in range(3):
    onboard_LED.on() # Visual indicator that capture/save is happening
    
    # Send a command to the camera to capture the photo
    cam.capture_jpg()
    sleep_ms(50)
    
    # Generate the next filename (e.g., burst.jpg, burst_1.jpg, burst_2.jpg...)
    filename = fm.new_jpg_filename('burst')
    print(f" Saving to: {filename}")
    
    # Save the file to the local storage
    cam.save_jpg(filename)
    
    onboard_LED.off()
    sleep_ms(500) # Short delay between burst shots

sleep_ms(1500) # Pause between sequences

# --- Sequence 2: Multiple Prefixes (Tracking the 'landscape' prefix) ---
print("\nCapturing 2 'landscape' photos...")
for i in range(2):
    onboard_LED.on()
    
    cam.capture_jpg()
    sleep_ms(50)
    
    # Generate the next filename (e.g., landscape.jpg, landscape_1.jpg...)
    # The filemanager remembers this independently from 'burst'
    filename = fm.new_jpg_filename('landscape')
    print(f" Saving to: {filename}")
    
    cam.save_jpg(filename)
    
    onboard_LED.off()
    sleep_ms(500)

print("\nFinished! Check your storage for the new images.")
print("Run this file again to see even more photos in storage!")

# Check how much storage we used
free_bytes = fm.filesystem_space()
free_mb_end = free_bytes / (1024 * 1024) # Convert to Megabytes
mb_used = free_mb_start - free_mb_end
print("Space Used: {} MB".format(mb_used))