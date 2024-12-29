from machine import Pin, SPI
from time import sleep_ms
import utime
import uos

class Camera:
    # Required imports and register definitions
    CAM_REG_SENSOR_RESET = 0x07
    CAM_SENSOR_RESET_ENABLE = 0x40
    CAM_REG_SENSOR_ID = 0x40
    
    SENSOR_5MP_1 = 0x81
    SENSOR_3MP_1 = 0x82
    SENSOR_5MP_2 = 0x83
    SENSOR_3MP_2 = 0x84
    
    # Camera registers
    CAM_REG_COLOR_EFFECT_CONTROL = 0x27
    CAM_REG_BRIGHTNESS_CONTROL = 0x22
    CAM_REG_CONTRAST_CONTROL = 0x23
    CAM_REG_SATURATION_CONTROL = 0x24
    CAM_REG_WB_MODE_CONTROL = 0x26
    CAM_REG_AUTO_FOCUS_CONTROL = 0x29
    CAM_REG_FORMAT = 0x20
    CAM_REG_CAPTURE_RESOLUTION = 0x21
    CAM_REG_DEBUG_DEVICE_ADDRESS = 0x0A
    deviceAddress = 0x78

    # Resolution settings
    RESOLUTION_320X240 = 0x01
    RESOLUTION_640X480 = 0x02
    RESOLUTION_1280X720 = 0x04
    RESOLUTION_1600X1200 = 0x06
    RESOLUTION_1920X1080 = 0x07
    RESOLUTION_2048X1536 = 0x08  # 3MP only
    RESOLUTION_2592X1944 = 0x09  # 5MP only
    
    # Valid resolutions
    valid_5mp_resolutions = {
        '320x240': RESOLUTION_320X240,
        '640x480': RESOLUTION_640X480,
        '1280x720': RESOLUTION_1280X720,
        '1600x1200': RESOLUTION_1600X1200,
        '1920x1080': RESOLUTION_1920X1080,
        '2592x1944': RESOLUTION_2592X1944
    }

    # White balance modes
    WB_MODE_AUTO = 0
    WB_MODE_SUNNY = 1
    WB_MODE_OFFICE = 2
    WB_MODE_CLOUDY = 3
    WB_MODE_HOME = 4
    
    # Brightness levels
    BRIGHTNESS_MINUS_4 = 8
    BRIGHTNESS_MINUS_3 = 6
    BRIGHTNESS_MINUS_2 = 4
    BRIGHTNESS_MINUS_1 = 2
    BRIGHTNESS_DEFAULT = 0
    BRIGHTNESS_PLUS_1 = 1
    BRIGHTNESS_PLUS_2 = 3
    BRIGHTNESS_PLUS_3 = 5
    BRIGHTNESS_PLUS_4 = 7
    
    # Contrast levels
    CONTRAST_MINUS_3 = 6
    CONTRAST_MINUS_2 = 4
    CONTRAST_MINUS_1 = 2
    CONTRAST_DEFAULT = 0
    CONTRAST_PLUS_1 = 1
    CONTRAST_PLUS_2 = 3
    CONTRAST_PLUS_3 = 5
    
    # Saturation levels
    SATURATION_MINUS_3 = 6
    SATURATION_MINUS_2 = 4
    SATURATION_MINUS_1 = 2
    SATURATION_DEFAULT = 0
    SATURATION_PLUS_1 = 1
    SATURATION_PLUS_2 = 3
    SATURATION_PLUS_3 = 5
    
    # Auto focus controls
    AF_ENABLE = 0x01
    AF_DISABLE = 0x00
    FOCUS_MANUAL = 0x02
    FOCUS_AUTO = 0x03
    SINGLE_FOCUS = 0x04
    
    # Image format
    CAM_IMAGE_PIX_FMT_JPG = 0x01
    
    # FIFO and State registers
    ARDUCHIP_FIFO = 0x04
    FIFO_CLEAR_ID_MASK = 0x01
    FIFO_START_MASK = 0x02
    ARDUCHIP_TRIG = 0x44
    CAP_DONE_MASK = 0x04
    FIFO_SIZE1 = 0x45
    FIFO_SIZE2 = 0x46
    FIFO_SIZE3 = 0x47
    SINGLE_FIFO_READ = 0x3D

    # For Waiting
    CAM_REG_SENSOR_STATE = 0x44
    CAM_REG_SENSOR_STATE_IDLE = 0x01
    
    def __init__(self, spi_bus, cs, skip_sleep=False):
        self.spi_bus = spi_bus
        self.cs = cs
        self.camera_idx = 'NOT DETECTED'
        
        # Initialize camera
        print("Initializing camera...")
        self._write_reg(self.CAM_REG_SENSOR_RESET, self.CAM_SENSOR_RESET_ENABLE)
        self._wait_idle()
        
        # Detect camera type
        self._get_sensor_config()
        self._wait_idle()
        
        # Set device address
        self._write_reg(self.CAM_REG_DEBUG_DEVICE_ADDRESS, self.deviceAddress)
        self._wait_idle()
        
        # Set initial format and resolution
        self.current_pixel_format = self.CAM_IMAGE_PIX_FMT_JPG
        self.current_resolution_setting = self.RESOLUTION_640X480
        
        # Initialize other variables
        self.received_length = 0
        self.total_length = 0
        
        if not skip_sleep and self.camera_idx == '5MP':
            sleep_ms(500)  # Wait for camera to stabilize
    
    def _get_sensor_config(self):
        """Detect camera type"""
        camera_id = self._read_reg(self.CAM_REG_SENSOR_ID)
        if (int.from_bytes(camera_id, 1) == self.SENSOR_5MP_1) or (int.from_bytes(camera_id, 1) == self.SENSOR_5MP_2):
            self.camera_idx = '5MP'
            print("5MP camera detected")
        elif (int.from_bytes(camera_id, 1) == self.SENSOR_3MP_1) or (int.from_bytes(camera_id, 1) == self.SENSOR_3MP_2):
            self.camera_idx = '3MP'
            print("3MP camera detected")

    @property
    def resolution(self):
        return self.current_resolution_setting
    
    @resolution.setter
    def resolution(self, new_resolution):
        """Set camera resolution"""
        try:
            input_string_lower = new_resolution.lower()
            if input_string_lower in self.valid_5mp_resolutions:
                print(f"Setting resolution to {new_resolution}")
                self.current_resolution_setting = self.valid_5mp_resolutions[input_string_lower]
                self._write_reg(self.CAM_REG_CAPTURE_RESOLUTION, self.current_resolution_setting)
                self._wait_idle()
            else:
                raise ValueError(f"Invalid resolution: {new_resolution}")
        except Exception as e:
            print(f"Resolution error: {e}")
            raise

    def set_white_balance(self, mode):
        """Set white balance mode"""
        try:
            wb_modes = {
                'auto': self.WB_MODE_AUTO,
                'sunny': self.WB_MODE_SUNNY,
                'office': self.WB_MODE_OFFICE,
                'cloudy': self.WB_MODE_CLOUDY,
                'home': self.WB_MODE_HOME
            }
            
            mode = mode.lower()
            if mode in wb_modes:
                print(f"Setting white balance to {mode}")
                self._write_reg(self.CAM_REG_WB_MODE_CONTROL, wb_modes[mode])
                self._wait_idle()
            else:
                raise ValueError(f"Invalid white balance mode: {mode}")
        except Exception as e:
            print(f"White balance error: {e}")
            raise

    def set_brightness_level(self, level):
        """Set brightness level"""
        try:
            level = int(level)
            print(f"Setting brightness to level {level}")
            self._write_reg(self.CAM_REG_BRIGHTNESS_CONTROL, level)
            self._wait_idle()
        except Exception as e:
            print(f"Brightness error: {e}")
            raise

    def set_contrast(self, level):
        """Set contrast level"""
        try:
            level = int(level)
            print(f"Setting contrast to level {level}")
            self._write_reg(self.CAM_REG_CONTRAST_CONTROL, level)
            self._wait_idle()
        except Exception as e:
            print(f"Contrast error: {e}")
            raise

    def set_saturation_control(self, level):
        """Set saturation level"""
        try:
            level = int(level)
            print(f"Setting saturation to level {level}")
            self._write_reg(self.CAM_REG_SATURATION_CONTROL, level)
            self._wait_idle()
        except Exception as e:
            print(f"Saturation error: {e}")
            raise

    def auto_focus(self, enable=True):
        """Enable or disable auto focus"""
        if self.camera_idx != '5MP':
            print("Auto focus is only supported on 5MP cameras")
            return False
            
        try:
            print(f"{'Enabling' if enable else 'Disabling'} auto focus...")
            if enable:
                # First ensure we're in auto focus mode
                self._write_reg(self.CAM_REG_AUTO_FOCUS_CONTROL, self.FOCUS_AUTO)
                sleep_ms(50)
                # Then enable auto focus
                self._write_reg(self.CAM_REG_AUTO_FOCUS_CONTROL, self.AF_ENABLE)
            else:
                # Disable auto focus
                self._write_reg(self.CAM_REG_AUTO_FOCUS_CONTROL, self.AF_DISABLE)
            sleep_ms(1000)  # Give time for focus to adjust
            print("Auto focus operation completed")
            return True
        except Exception as e:
            print(f"Auto focus error: {e}")
            return False

    def single_focus(self):
        """Perform single auto focus"""
        if self.camera_idx != '5MP':
            print("Auto focus is only supported on 5MP cameras")
            return False
            
        try:
            print("Performing single focus...")
            # First set to auto focus mode
            self._write_reg(self.CAM_REG_AUTO_FOCUS_CONTROL, self.FOCUS_AUTO)
            sleep_ms(50)
            # Then trigger single focus
            self._write_reg(self.CAM_REG_AUTO_FOCUS_CONTROL, self.SINGLE_FOCUS)
            sleep_ms(1000)  # Give time for focus operation
            print("Single focus completed")
            return True
        except Exception as e:
            print(f"Single focus error: {e}")
            return False
    
    def capture_jpg(self):
        """Capture image"""
        self._write_reg(self.CAM_REG_FORMAT, self.current_pixel_format)
        self._wait_idle()
        self._write_reg(self.CAM_REG_CAPTURE_RESOLUTION, self.current_resolution_setting)
        self._wait_idle()
        self._set_capture()
    
    def saveJPG(self, filename):
        """Save captured image"""
        print('Saving image...')
        headflag = 0
        image_data = 0x00
        image_data_next = 0x00
        
        image_data_int = 0x00
        image_data_next_int = 0x00
        
        while(self.received_length):
            image_data = image_data_next
            image_data_int = image_data_next_int
            
            image_data_next = self._read_byte()
            image_data_next_int = int.from_bytes(image_data_next, 1)
            
            if headflag == 1:
                jpg_to_write.write(image_data_next)
            
            if (image_data_int == 0xff) and (image_data_next_int == 0xd8):
                headflag = 1
                jpg_to_write = open(filename, 'wb')
                jpg_to_write.write(image_data)
                jpg_to_write.write(image_data_next)
                
            if (image_data_int == 0xff) and (image_data_next_int == 0xd9):
                headflag = 0
                jpg_to_write.write(image_data_next)
                jpg_to_write.close()
    
    def _set_capture(self):
        self._clear_fifo_flag()
        self._wait_idle()
        self._start_capture()
        
        while (int(self._get_bit(self.ARDUCHIP_TRIG, self.CAP_DONE_MASK)) == 0):
            sleep_ms(200)
            
        self.received_length = self._read_fifo_length()
        self.total_length = self.received_length
    
    def _clear_fifo_flag(self):
        self._write_reg(self.ARDUCHIP_FIFO, self.FIFO_CLEAR_ID_MASK)

    def _start_capture(self):
        self._write_reg(self.ARDUCHIP_FIFO, self.FIFO_START_MASK)
    
    def _read_fifo_length(self):
        len1 = int.from_bytes(self._read_reg(self.FIFO_SIZE1), 1)
        len2 = int.from_bytes(self._read_reg(self.FIFO_SIZE2), 1)
        len3 = int.from_bytes(self._read_reg(self.FIFO_SIZE3), 1)
        return ((len3 << 16) | (len2 << 8) | len1) & 0xffffff
    
    def _write_reg(self, addr, val):
        self.cs.off()
        self.spi_bus.write(bytes([addr | 0x80, val]))
        self.cs.on()
        sleep_ms(1)
    
    def _read_reg(self, addr):
        self.cs.off()
        self.spi_bus.write(bytes([addr & 0x7F]))
        data = self.spi_bus.read(1)
        data = self.spi_bus.read(1)
        self.cs.on()
        return data
    
    def _read_byte(self):
        self.cs.off()
        self.spi_bus.write(bytes([self.SINGLE_FIFO_READ]))
        data = self.spi_bus.read(1)
        data = self.spi_bus.read(1)
        self.cs.on()
        self.received_length -= 1
        return data
    
    def _wait_idle(self):
        sleep_ms(2)
    
    def _get_bit(self, addr, bit):
        data = self._read_reg(addr)
        return int.from_bytes(data, 1) & bit
