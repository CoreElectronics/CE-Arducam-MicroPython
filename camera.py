from utime import sleep_ms
import utime

import uos
import ujson

'''
Start this alongside the camera module to save photos in a folder with a filename i.e. image-<counter>.jpg
* appends '_' after a word, the next number and the file format
'''
class FileManager:
    def __init__(self, file_manager_name='filemanager.log'):
        self.FILE_MANAGER_LOG_NAME = file_manager_name
        self.last_request_filename = None
        self.suffix = None
        count = 0
        self.file_dict = {}

        try:
            # Check if the filename already exists in the storage
            with open(self.FILE_MANAGER_LOG_NAME, 'r') as f:
                self.file_dict = ujson.loads(f.read())
        except:
            # Ensure file is present
            if self.FILE_MANAGER_LOG_NAME not in uos.listdir():
                with open(self.FILE_MANAGER_LOG_NAME, 'w') as f:
                    f.write(ujson.dumps(self.file_dict))

    def new_jpg_filename(self, requested_filename=None):
        return (self.new_filename(requested_filename) + '.jpg')

    def new_filename(self, requested_filename):
        count = 0
        self.last_request_filename = requested_filename

        if requested_filename == None and self.last_request_filename == None:
            raise Exception('Please enter a filename for the first use of the function')

        if requested_filename in self.file_dict:
            count = self.file_dict[requested_filename] + 1
        self.file_dict[requested_filename] = count

        self.save_manager_file()
        new_filename = f"{requested_filename}_{count}" if count > 0 else f"{requested_filename}"

        return new_filename

    def save_manager_file(self):
        # Save the updated list back to the storage
        with open(self.FILE_MANAGER_LOG_NAME, 'w') as f:
            f.write(ujson.dumps(self.file_dict))



class Camera:
    ## For camera Reset
    CAM_REG_SENSOR_RESET = 0x07
    CAM_SENSOR_RESET_ENABLE = 0x40
    ## For get_sensor_config
    CAM_REG_SENSOR_ID = 0x40
    SENSOR_5MP_1 = 0x81
    SENSOR_3MP_1 = 0x82
    SENSOR_5MP_2 = 0x83
    SENSOR_3MP_2 = 0x84
    # Camera effect control
    ## Set Colour Effect
    CAM_REG_COLOR_EFFECT_CONTROL = 0x27
    SPECIAL_NORMAL = 0x00
    SPECIAL_COOL = 1
    SPECIAL_WARM = 2
    SPECIAL_BW = 0x04
    SPECIAL_YELLOWING = 4
    SPECIAL_REVERSE = 5
    SPECIAL_GREENISH = 6
    SPECIAL_LIGHT_YELLOW = 9 # 3MP Only
    ## Set Brightness
    CAM_REG_BRIGHTNESS_CONTROL = 0X22
    BRIGHTNESS_MINUS_4 = 8
    BRIGHTNESS_MINUS_3 = 6
    BRIGHTNESS_MINUS_2 = 4
    BRIGHTNESS_MINUS_1 = 2
    BRIGHTNESS_DEFAULT = 0
    BRIGHTNESS_PLUS_1 = 1
    BRIGHTNESS_PLUS_2 = 3
    BRIGHTNESS_PLUS_3 = 5
    BRIGHTNESS_PLUS_4 = 7
    ## Set Contrast
    CAM_REG_CONTRAST_CONTROL = 0X23
    CONTRAST_MINUS_3 = 6
    CONTRAST_MINUS_2 = 4
    CONTRAST_MINUS_1 = 2
    CONTRAST_DEFAULT = 0
    CONTRAST_PLUS_1 = 1
    CONTRAST_PLUS_2 = 3
    CONTRAST_PLUS_3 = 5
    ## Set Saturation
    CAM_REG_SATURATION_CONTROL = 0X24
    SATURATION_MINUS_3 = 6
    SATURATION_MINUS_2 = 4
    SATURATION_MINUS_1 = 2
    SATURATION_DEFAULT = 0
    SATURATION_PLUS_1 = 1
    SATURATION_PLUS_2 = 3
    SATURATION_PLUS_3 = 5
    ## Set Exposure Value
    CAM_REG_EXPOSURE_CONTROL = 0X25
    EXPOSURE_MINUS_3 = 6
    EXPOSURE_MINUS_2 = 4
    EXPOSURE_MINUS_1 = 2
    EXPOSURE_DEFAULT = 0
    EXPOSURE_PLUS_1 = 1
    EXPOSURE_PLUS_2 = 3
    EXPOSURE_PLUS_3 = 5
    ## Set Whitebalance
    CAM_REG_WB_MODE_CONTROL = 0X26
    WB_MODE_AUTO = 0
    WB_MODE_SUNNY = 1
    WB_MODE_OFFICE = 2
    WB_MODE_CLOUDY = 3
    WB_MODE_HOME = 4
    ## Set Sharpness
    CAM_REG_SHARPNESS_CONTROL = 0X28 #3MP only
    SHARPNESS_NORMAL = 0
    SHARPNESS_1 = 1
    SHARPNESS_2 = 2
    SHARPNESS_3 = 3
    SHARPNESS_4 = 4
    SHARPNESS_5 = 5
    SHARPNESS_6 = 6
    SHARPNESS_7 = 7
    SHARPNESS_8 = 8
    ## Set Autofocus
    CAM_REG_AUTO_FOCUS_CONTROL = 0X29 #5MP only
    ## Set Image quality
    CAM_REG_IMAGE_QUALITY = 0x2A
    IMAGE_QUALITY_HIGH = 0
    IMAGE_QUALITY_MEDI = 1
    IMAGE_QUALITY_LOW = 2
    # Manual gain, and exposure are explored in the datasheet - https://www.arducam.com/downloads/datasheet/Arducam_MEGA_SPI_Camera_Application_Note.pdf
    # Device addressing
    CAM_REG_DEBUG_DEVICE_ADDRESS = 0x0A
    deviceAddress = 0x78
    # For state management
    CAM_REG_SENSOR_STATE = 0x44
    CAM_REG_SENSOR_STATE_IDLE = 0x01
    # Setup for capturing photos
    CAM_REG_FORMAT = 0x20
    CAM_IMAGE_PIX_FMT_JPG = 0x01
    CAM_IMAGE_PIX_FMT_RGB565 = 0x02
    CAM_IMAGE_PIX_FMT_YUV = 0x03
    # Resolution settings
    CAM_REG_CAPTURE_RESOLUTION = 0x21
    # Some resolutions are not available - refer to datasheet https://www.arducam.com/downloads/datasheet/Arducam_MEGA_SPI_Camera_Application_Note.pdf
    RESOLUTION_320X240 = 0X01
    RESOLUTION_640X480 = 0X02
    RESOLUTION_1280X720 = 0X04
    RESOLUTION_1600X1200 = 0X06
    RESOLUTION_1920X1080 = 0X07
    RESOLUTION_2048X1536 = 0X08 # 3MP only
    RESOLUTION_2592X1944 = 0X09 # 5MP only
    RESOLUTION_96X96 = 0X0a
    RESOLUTION_128X128 = 0X0b
    RESOLUTION_320X320 = 0X0c
    valid_3mp_resolutions = {
        '320x240': RESOLUTION_320X240, 
        '640x480': RESOLUTION_640X480, 
        '1280x720': RESOLUTION_1280X720, 
        '1600x1200': RESOLUTION_1600X1200,
        '1920x1080': RESOLUTION_1920X1080,
        '2048x1536': RESOLUTION_2048X1536,
        '96X96': RESOLUTION_96X96,
        '128X128': RESOLUTION_128X128,
        '320X320': RESOLUTION_320X320
    }
    valid_5mp_resolutions = {
        '320x240': RESOLUTION_320X240, 
        '640x480': RESOLUTION_640X480, 
        '1280x720': RESOLUTION_1280X720, 
        '1600x1200': RESOLUTION_1600X1200,
        '1920x1080': RESOLUTION_1920X1080,
        '2592x1944': RESOLUTION_2592X1944,
        '96X96': RESOLUTION_96X96,
        '128X128': RESOLUTION_128X128,
        '320X320': RESOLUTION_320X320
    }
    # FIFO and State setting registers
    ARDUCHIP_FIFO = 0x04
    FIFO_CLEAR_ID_MASK = 0x01
    FIFO_START_MASK = 0x02
    ARDUCHIP_TRIG = 0x44
    CAP_DONE_MASK = 0x04
    FIFO_SIZE1 = 0x45
    FIFO_SIZE2 = 0x46
    FIFO_SIZE3 = 0x47
    SINGLE_FIFO_READ = 0x3D
    BURST_FIFO_READ = 0X3C
    # Size of image_buffer (Burst reading)
    BUFFER_MAX_LENGTH = 255
    # For 5MP startup routine
    WHITE_BALANCE_WAIT_TIME_MS = 500

    def __init__(self, spi_bus, cs, skip_sleep=False, debug_text_enabled=False):
        self.cs = cs
        self.spi_bus = spi_bus
        self.debug_text_enabled = debug_text_enabled
        self.camera_idx = 'NOT DETECTED'
        
        self._write_reg(self.CAM_REG_SENSOR_RESET, self.CAM_SENSOR_RESET_ENABLE) # Reset camera
        self._wait_idle()
        self._get_sensor_config() # Get camera sensor information
        self._wait_idle()
        self._write_reg(self.CAM_REG_DEBUG_DEVICE_ADDRESS, self.deviceAddress)
        self._wait_idle()

        self.run_start_up_config = True

        # Set default format and resolution
        self.current_pixel_format = self.CAM_IMAGE_PIX_FMT_JPG
        self.old_pixel_format = self.current_pixel_format

        self.current_resolution_setting = self.RESOLUTION_640X480 # ArduCam driver defines this as mode
        self.old_resolution = self.current_resolution_setting

        self.set_filter(self.SPECIAL_NORMAL)

        self.received_length = 0
        self.total_length = 0

        # Burst setup
        self.first_burst_run = False
        self.image_buffer = bytearray(self.BUFFER_MAX_LENGTH)
        self.valid_image_buffer = 0

        # Tracks the AWB warmup time
        self.start_time = utime.ticks_ms()
        if debug_text_enabled:
            print('Camera version =', self.camera_idx)
        if self.camera_idx == '3MP':
            utime.sleep_ms(self.WHITE_BALANCE_WAIT_TIME_MS)# fifo length is sometimes a broken value (5 to 8 megabytes) and causes program to fail this helps 
            self._wait_idle()
            self.startup_routine_3MP()
        if self.camera_idx == '5MP' and skip_sleep == False:
            utime.sleep_ms(self.WHITE_BALANCE_WAIT_TIME_MS)

    def startup_routine_3MP(self):
        # Leave the shutter open for some time seconds (i.e. take a few photos without saving)
        if self.debug_text_enabled: print('Running 3MP startup routine')
        self.capture_jpg()
        self.save_jpg('dummy_image.jpg')
        uos.remove('dummy_image.jpg')
        if self.debug_text_enabled: print('Finished 3MP startup routine')

    def capture_jpg(self):
        if (utime.ticks_diff(utime.ticks_ms(), self.start_time) <= self.WHITE_BALANCE_WAIT_TIME_MS) and self.camera_idx == '5MP':
            print('Please add a ', self.WHITE_BALANCE_WAIT_TIME_MS, 'ms delay to allow for white balance to run')
        else:
            if self.debug_text_enabled: print('Entered capture_jpg')
            if (self.old_pixel_format != self.current_pixel_format) or self.run_start_up_config:
                self.old_pixel_format = self.current_pixel_format
                self._write_reg(self.CAM_REG_FORMAT, self.current_pixel_format) # Set to capture a jpg
                self._wait_idle()
            if self.debug_text_enabled: print('Old_resolution: ',self.old_resolution,'New_resolution: ',self.current_resolution_setting)
            if (self.old_resolution != self.current_resolution_setting) or self.run_start_up_config:
                self.old_resolution = self.current_resolution_setting
                self._write_reg(self.CAM_REG_CAPTURE_RESOLUTION, self.current_resolution_setting)
                if self.debug_text_enabled: print('Setting resolution: ', self.current_resolution_setting)
                self._wait_idle()
            self.run_start_up_config = False

            # Start capturing the photo
            self._set_capture()
            if self.debug_text_enabled: print('Finished capture_jpg')

    def _update_progress(self, progress, bar_length=20):
        filled_length = int(bar_length * progress)
        bar = '#' * filled_length + '-' * (bar_length - filled_length)
        print("Progress: |{}| {}%".format(bar, int(progress * 100)), end='\r')

    def save_jpg(self, filename="image.jpg", progress_bar=True): # From the amazing - @chrisrothwell1 - https://github.com/CoreElectronics/CE-Arducam-MicroPython/issues/9
        jpg_to_write = open(filename,'ab')
        recv_len = self.received_length
        starting_len = recv_len
        self.cs.off()
        self.spi_bus.write(bytes([self.BURST_FIFO_READ]))
        data = self.spi_bus.read(1)
        inx = 0
        while recv_len > 0:
            progress = (starting_len - recv_len)/starting_len
            if progress_bar: self._update_progress(progress)

            last_byte = self.image_buffer[self.BUFFER_MAX_LENGTH - 1]
            self.spi_bus.readinto(self.image_buffer)
            recv_len -= self.BUFFER_MAX_LENGTH
            inx = self.image_buffer.find(b'\xff\xd9')
            if inx >= 0:
                jpg_to_write.write(self.image_buffer[:inx+2])
                jpg_to_write.close()
                if progress_bar: self._update_progress(1)
                print()
                print("Image saved")
                break
            elif last_byte == 0xff and self.image_buffer[0] == 0xd9:
                jpg_to_write.write(b'\xd9')
                jpg_to_write.close()
                if progress_bar: self._update_progress(1)
                print()
                print("Image saved")
                break
            else:
                jpg_to_write.write(self.image_buffer)

    @property
    def resolution(self):
        return self.current_resolution_setting
    @resolution.setter
    def resolution(self, new_resolution):
        input_string_lower = new_resolution.lower()        
        if self.camera_idx == '3MP':
            if input_string_lower in self.valid_3mp_resolutions:
                self.current_resolution_setting = self.valid_3mp_resolutions[input_string_lower]
            else:
                raise ValueError("Invalid resolution provided for {}, please select from {}".format(self.camera_idx, list(self.valid_3mp_resolutions.keys())))

        elif self.camera_idx == '5MP':
            if input_string_lower in self.valid_5mp_resolutions:
                self.current_resolution_setting = self.valid_5mp_resolutions[input_string_lower]
            else:
                raise ValueError("Invalid resolution provided for {}, please select from {}".format(self.camera_idx, list(self.valid_5mp_resolutions.keys())))

    def set_pixel_format(self, new_pixel_format):
        self.current_pixel_format = new_pixel_format

    def set_brightness_level(self, brightness):
        self._write_reg(self.CAM_REG_BRIGHTNESS_CONTROL, brightness)
        self._wait_idle()

    def set_filter(self, effect):
        self._write_reg(self.CAM_REG_COLOR_EFFECT_CONTROL, effect)
        self._wait_idle()

    def set_saturation_control(self, saturation_value):
        self._write_reg(self.CAM_REG_SATURATION_CONTROL, saturation_value)
        self._wait_idle()

    def set_contrast(self, contrast):
        self._write_reg(self.CAM_REG_CONTRAST_CONTROL, contrast)
        self._wait_idle()

    def set_white_balance(self, environment):
        register_value = self.WB_MODE_AUTO

        if environment == 'sunny':
            register_value = self.WB_MODE_SUNNY
        elif environment == 'office':
            register_value = self.WB_MODE_OFFICE
        elif environment == 'cloudy':
            register_value = self.WB_MODE_CLOUDY
        elif environment == 'home':
            register_value = self.WB_MODE_HOME
        elif self.camera_idx == '3MP':
            print('For best results set a White Balance setting')

        self.white_balance_mode = register_value
        self._write_reg(self.CAM_REG_WB_MODE_CONTROL, register_value)
        self._wait_idle()

    def _clear_fifo_flag(self):
        self._write_reg(self.ARDUCHIP_FIFO, self.FIFO_CLEAR_ID_MASK)

    def _start_capture(self):
        self._write_reg(self.ARDUCHIP_FIFO, self.FIFO_START_MASK)

    def _set_capture(self):
        if self.debug_text_enabled: print('Entered _set_capture')
        self._clear_fifo_flag()
        self._wait_idle()
        self._start_capture()
        if self.debug_text_enabled: print('FIFO flag cleared, started _start_capture, waiting for CAP_DONE_MASK')
        while (int(self._get_bit(self.ARDUCHIP_TRIG, self.CAP_DONE_MASK)) == 0):
            if self.debug_text_enabled: print("ARDUCHIP_TRIG register, CAP_DONE_MASK:", self._get_bit(self.ARDUCHIP_TRIG, self.CAP_DONE_MASK))
            sleep_ms(200)
        if self.debug_text_enabled:print('Finished waiting for _start_capture')

        #_read_fifo_length() was giving imposible value tried adding wait, did not seem to fix it
        self._wait_idle()

        self.received_length = self._read_fifo_length()
        self.total_length = self.received_length
        self.burst_first_flag = False
        if self.debug_text_enabled: print('FIFO length has been read')

    def _read_fifo_length(self):
        if self.debug_text_enabled: print('Entered _read_fifo_length')
        len1 = int.from_bytes(self._read_reg(self.FIFO_SIZE1),1) #0x45
        len2 = int.from_bytes(self._read_reg(self.FIFO_SIZE2),1) #0x46
        len3 = int.from_bytes(self._read_reg(self.FIFO_SIZE3),1) #0x47
        if self.debug_text_enabled: 
            print("FIFO length bytes (int), (int), (int):")
            print(len1,len2,len3)
        if ((((len3 << 16) | (len2 << 8) | len1) & 0xffffff)>5000000): 
            print("Error fifo length is too long >5MB Size: ", (((len3 << 16) | (len2 << 8) | len1) & 0xffffff))
            print("Arducam possibly did not take a picture and is returning garbage data")
        return ((len3 << 16) | (len2 << 8) | len1) & 0xffffff

    def _get_sensor_config(self):
        camera_id = self._read_reg(self.CAM_REG_SENSOR_ID);
        self._wait_idle()
        if (int.from_bytes(camera_id, 1) == self.SENSOR_3MP_1) or (int.from_bytes(camera_id, 1) == self.SENSOR_3MP_2):
            self.camera_idx = '3MP'
        if (int.from_bytes(camera_id, 1) == self.SENSOR_5MP_1) or (int.from_bytes(camera_id, 1) == self.SENSOR_5MP_2):
            self.camera_idx = '5MP'

    def _bus_write(self, addr, val):
        self.cs.off()
        self.spi_bus.write(bytes([addr]))
        self.spi_bus.write(bytes([val])) # FixMe only works with single bytes
        self.cs.on()
        sleep_ms(1) # From the Arducam Library
        return 1

    def _bus_read(self, addr):
        self.cs.off()
        self.spi_bus.write(bytes([addr]))
        data = self.spi_bus.read(1) # Only read second set of data
        data = self.spi_bus.read(1)
        self.cs.on()
        return data

    def _write_reg(self, addr, val):
        self._bus_write(addr | 0x80, val)

    def _read_reg(self, addr):
        data = self._bus_read(addr & 0x7F)
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
        data = self._read_reg(self.CAM_REG_SENSOR_STATE)
        while ((int.from_bytes(data, 1) & 0x03) == self.CAM_REG_SENSOR_STATE_IDLE):
            data = self._read_reg(self.CAM_REG_SENSOR_STATE)
            sleep_ms(2)

    def _get_bit(self, addr, bit):
        data = self._read_reg(addr);
        return int.from_bytes(data, 1) & bit;