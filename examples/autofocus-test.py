from machine import Pin, SPI
from camera import Camera
import time
import uos

def print_debug(message, level=1):
    prefix = "  " * (level - 1)
    print(f"{prefix}🔍 {message}")

def print_section(message):
    print(f"\n{'='*20} {message} {'='*20}")

def check_file_exists(filename):
    try:
        return filename in uos.listdir()
    except:
        return False

def test_camera_capture():
    try:
        print_section("INITIALIZATION")
        
        # SPI Debug
        print_debug("Configuring SPI...")
        print_debug("Parameters:", 2)
        print_debug("- Baudrate: 8000000", 3)
        print_debug("- Polarity: 0", 3)
        print_debug("- Phase: 0", 3)
        print_debug("- Bits: 8", 3)
        print_debug("- First bit: MSB", 3)
        print_debug("- SCK Pin: 10", 3)
        print_debug("- MOSI Pin: 15", 3)
        print_debug("- MISO Pin: 12", 3)
        
        spi = SPI(1, 
                  baudrate=8000000,
                  polarity=0, 
                  phase=0, 
                  bits=8, 
                  firstbit=SPI.MSB,
                  sck=Pin(10),
                  mosi=Pin(15),
                  miso=Pin(12))
        print_debug("SPI initialized successfully")
        
        # CS Pin Debug
        print_debug("Configuring CS pin (Pin 13)...")
        cs = Pin(13, Pin.OUT)
        cs.value(1)
        print_debug("CS pin initialized and set HIGH")
        
        # Camera Instance
        print_debug("Creating camera instance...")
        camera = Camera(spi, cs)
        print_debug(f"Camera type detected: {camera.camera_idx}")
        
        # Stabilization Period
        print_debug("Starting camera stabilization period (2 seconds)...")
        time.sleep(2)
        print_debug("Stabilization complete")
        
        print_section("NORMAL CAPTURE TEST")
        
        # First Capture (No Autofocus)
        print_debug("Beginning capture without autofocus")
        print_debug("Current resolution: {}".format(camera.resolution))
        
        if check_file_exists('no_autofocus.jpg'):
            print_debug("Removing existing no_autofocus.jpg", 2)
            uos.remove('no_autofocus.jpg')
        
        print_debug("Initiating capture_jpg()", 2)
        camera.capture_jpg()
        print_debug("Capture complete", 2)
        
        print_debug("Saving image...", 2)
        camera.saveJPG('no_autofocus.jpg')
        
        if check_file_exists('no_autofocus.jpg'):
            size1 = uos.stat('no_autofocus.jpg')[6]
            print_debug(f"Image saved successfully (Size: {size1} bytes)", 2)
        else:
            raise Exception("Failed to save no_autofocus.jpg")
        
        print_section("AUTOFOCUS TEST")
        
        # Autofocus Test
        print_debug("Testing autofocus functionality")
        if camera.camera_idx != '5MP':
            print_debug("WARNING: Camera is not 5MP, autofocus may not work", 2)
        
        print_debug("Enabling autofocus...", 2)
        result = camera.auto_focus(True)
        print_debug(f"Autofocus enable result: {result}", 2)
        
        print_debug("Waiting for autofocus adjustment (2 seconds)...", 2)
        time.sleep(2)
        
        if check_file_exists('with_autofocus.jpg'):
            print_debug("Removing existing with_autofocus.jpg", 2)
            uos.remove('with_autofocus.jpg')
        
        print_debug("Initiating capture with autofocus...", 2)
        camera.capture_jpg()
        print_debug("Capture complete", 2)
        
        print_debug("Saving image...", 2)
        camera.saveJPG('with_autofocus.jpg')
        
        if check_file_exists('with_autofocus.jpg'):
            size2 = uos.stat('with_autofocus.jpg')[6]
            print_debug(f"Image saved successfully (Size: {size2} bytes)", 2)
        else:
            raise Exception("Failed to save with_autofocus.jpg")
        
        print_section("TEST RESULTS")
        print_debug("Test completed successfully")
        print_debug(f"No Autofocus image: {size1} bytes", 2)
        print_debug(f"With Autofocus image: {size2} bytes", 2)
        print_debug(f"Size difference: {abs(size2 - size1)} bytes", 2)
        
    except Exception as e:
        print_section("ERROR")
        print_debug(f"Test failed: {str(e)}")
        print_debug("Stack trace:", 2)
        import sys
        sys.print_exception(e)
    finally:
        print_section("CLEANUP")
        if 'spi' in locals():
            print_debug("Deinitializing SPI...")
            spi.deinit()
            print_debug("SPI deinitialized")

if __name__ == '__main__':
    test_camera_capture()
