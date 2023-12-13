# Arducam port to Pico


from machine import Pin, SPI, reset



# Developing on 1.19
'''
#################### PINOUT ###############
Camera pin - Pico Pin
VCC - 3V3
GND - GND
SCK - GP18 - white
MISO - RX - GP16 - brown
MOSI - TX - GP19 - yellow
CS - GP17 - orange
'''


from utime import sleep_ms
import utime

import uos
import ujson




'''
Start this alongside the camera module to save photos in a folder with a filename i.e. image-<counter>.jpg
* appends '_' after a word, the next number and the file format
'''
def filemanager(self,filename):
    count = 0
    files = {}
    # Ensure file is present
    if self.FILE_MANAGER_LOG_NAME not in uos.listdir():
        with open(self.FILE_MANAGER_LOG_NAME, 'w') as f:
            f.write(ujson.dumps({}))
        
    # Check if the filename already exists in the storage
    with open(self.FILE_MANAGER_LOG_NAME, 'r') as f:
        files = ujson.loads(f.read())
        if filename in files:
            count = files[filename] + 1
        files[filename] = count
        
    # Save the updated list back to the storage
    with open(self.FILE_MANAGER_LOG_NAME, 'w') as f:
        f.write(ujson.dumps(files))

    new_filename = f"{filename}_{count}.jpg" if count > 0 else f"{filename}.jpg"
    return new_filename



############### HIGH LEVEL FUNCTIONS #################

class camera:
    # Required imports
    
    # Register definitions


    # For camera Reset
    CAM_REG_SENSOR_RESET = 0x07
    CAM_SENSOR_RESET_ENABLE = 0x40
    
    # For get_sensor_config
    CAM_REG_SENSOR_ID = 0x40
    
    SENSOR_5MP_1 = 0x81
    SENSOR_3MP_1 = 0x82
    SENSOR_5MP_2 = 0x83
    SENSOR_3MP_2 = 0x84
    
    ## Camera effect control
    
    # Set Colour Effect
    CAM_REG_COLOR_EFFECT_CONTROL = 0x27
    
    SPECIAL_NORMAL = 0x00
    SPECIAL_BW = 0x04
    SPECIAL_GREENISH = 0x20
    # TODO Complete

    # Set Brightness
    CAM_REG_BRIGHTNESS_CONTROL = 0X22
    
    # TODO
    
    

    # Set Contrast
    CAM_REG_CONTRAST_CONTROL = 0X23
    
    CONTRAST_MINUS_3 = 6
    CONTRAST_MINUS_2 = 4
    CONTRAST_MINUS_1 = 2
    CONTRAST_DEFAULT = 0
    CONTRAST_PLUS_1 = 1
    CONTRAST_PLUS_2 = 3
    CONTRAST_PLUS_3 = 5
    
    
    # Set Saturation
    CAM_REG_SATURATION_CONTROL = 0X24
    
    

    # Set Exposure Value
    # TODO: INSPECT LIBRARY, DIFFERENT TO OTHER SETTING REGISTERS
    
    
    # Set Whitebalance
    CAM_REG_WB_MODE_CONTROL = 0X26
    
    WB_MODE_AUTO = 0
    WB_MODE_SUNNY = 1
    WB_MODE_OFFICE = 2
    WB_MODE_CLOUDY = 3
    WB_MODE_HOME = 4

    # Set Sharpness
    CAM_REG_SHARPNESS_CONTROL = 0X28
    
    # Set Autofocus
    CAM_REG_AUTO_FOCUS_CONTROL = 0X29
    
    # Set Image quality
    CAM_REG_IMAGE_QUALITY = 0x2A
    
    
    # Device addressing
    CAM_REG_DEBUG_DEVICE_ADDRESS = 0x0A
    deviceAddress = 0x78
    
    # For Waiting
    CAM_REG_SENSOR_STATE = 0x44
    CAM_REG_SENSOR_STATE_IDLE = 0x01
    
    # Setup for capturing photos
    CAM_REG_FORMAT = 0x20
    
    CAM_IMAGE_PIX_FMT_JPG = 0x01
    CAM_IMAGE_PIX_FMT_RGB565 = 0x02
    CAM_IMAGE_PIX_FMT_YUV = 0x03
    
    # Resolution settings
    CAM_REG_CAPTURE_RESOLUTION = 0x21
    
    RESOLUTION_160X120 = 0X00
    RESOLUTION_320X240 = 0X01
    RESOLUTION_640X480 = 0X02
    RESOLUTION_800X600 = 0X03
    RESOLUTION_1280X720 = 0X04
    RESOLUTION_1280X960 = 0X05
    RESOLUTION_1600X1200 = 0X06
    RESOLUTION_1920X1080 = 0X07
    RESOLUTION_2048X1536 = 0X08
    RESOLUTION_2592X1944 = 0X09
    RESOLUTION_96X96 = 0X0a
    RESOLUTION_128X128 = 0X0b
    RESOLUTION_320X320 = 0X0c

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
    
    WHITE_BALANCE_WAIT_TIME_MS = 500
    
    FILE_MANAGER_LOG_NAME = 'filemanager.log'
    
    

# User callable functions
## Main functions
## Setting functions
# Internal functions
## High level internal functions
## Low level

##################### Callable FUNCTIONS #####################

########### CORE PHOTO FUNCTIONS ###########
    def __init__(self, spi_bus, cs):
        self.cs = cs
        self.spi_bus = spi_bus

        self._write_reg(self.CAM_REG_SENSOR_RESET, self.CAM_SENSOR_RESET_ENABLE) # Reset camera
        self._wait_idle()
        self._get_sensor_config() # Get camera sensor information
        self._wait_idle()
        self._write_reg(self.CAM_REG_DEBUG_DEVICE_ADDRESS, self.deviceAddress)
        self._wait_idle()
        
        self.old_pixel_format = self.CAM_IMAGE_PIX_FMT_JPG
        self.pixel_format = self.CAM_IMAGE_PIX_FMT_JPG
        self.old_resolution = = self.RESOLUTION_640X480
        self.resolution = self.RESOLUTION_640X480 # Arducam Arduino Library refers to this as 'mode'
        self.set_filter(self.SPECIAL_NORMAL)
        
        self.received_length = 0
        self.total_length = 0
        self.burst_first_flag = False
        
        # Tracks the AWB warmup time
        self.start_time = utime.ticks_ms()
        
        print('camera init')
    '''
    Issue warning if the filepath doesnt end in .jpg (Blank) and append
    Issue error if the filetype is NOT .jpg
    '''
    def capture_jpg(self):
        
        if utime.ticks_diff(utime.ticks_ms(), self.start_time) >= self.WHITE_BALANCE_WAIT_TIME_MS:
        
        
            # TODO: CLASSES CALL THE FUNCTION TO UPDATE NEW PIXEL FORMAT AND MODE
            new_pixel_format = 0x00
            new_resolution = self.RESOLUTION_320X240
            
            print('Starting capture JPG')
            # JPG, bmp ect
            # TODO: PROPERTIES TO CONFIGURE THE PIXEL FORMAT
            if self.old_pixel_format != self.pixel_format:
                self.old_pixel_format = self.pixel_format
                self._write_reg(self.CAM_REG_FORMAT, self.pixel_format) # Set to capture a jpg
                self._wait_idle()
            
                # TODO: PROPERTIES TO CONFIGURE THE RESOLUTION
            if self.old_resolution != self.resolution:
                self.old_resolution = self.resolution
                self._write_reg(self.CAM_REG_CAPTURE_RESOLUTION, new_resolution)
                print('setting res', new_resolution)
                self._wait_idle()
            
            # Start capturing the photo
            self._set_capture()
            print('capture jpg complete')
        else:
            print('Please add a ', self.WHITE_BALANCE_WAIT_TIME_MS, ' delay to allow for white balance to run')
    
    # TODO: After reading the camera data clear the FIFO and reset the camera (so that the first time read can be used)
    def saveJPG(self,filename):
        headflag = 0
        print('starting saving')
        print('rec len:', self.received_length)
        
        image_data = 0x00
        image_data_next = 0x00
        
        image_data_int = 0x00
        image_data_next_int = 0x00
        
        while(self.received_length):
            
            image_data = image_data_next
            image_data_int = image_data_next_int

            image_data_next = self._read_byte() 
            image_data_next_int = int.from_bytes(image_data_next, 1) # TODO: CHANGE TO READ n BYTES
            if headflag == 1:
                jpg_to_write.write(image_data_next)
            
            if (image_data_int == 0xff) and (image_data_next_int == 0xd8):
                # TODO: Save file to filename
                print('start of file')
                headflag = 1
                jpg_to_write = open(filename,'ab')
                jpg_to_write.write(image_data)
                jpg_to_write.write(image_data_next)
                
            if (image_data_int == 0xff) and (image_data_next_int == 0xd9):
                print('TODO: Save and close file?')
                headflag = 0
                jpg_to_write.write(image_data_next)
                jpg_to_write.close()

    '''
        Set using self.RESOLUTION_<resolution>
    '''
    def set_resolution(self, new_resolution):
        self.resolution = new_resolution

    def set_pixel_format(self, new_pixel_format):
        self.pixel_format = new_pixel_format




########### ACCSESSORY FUNCTIONS ###########

    # TODO: Complete for other camera settings
    # Make these setters - https://github.com/CoreElectronics/CE-PiicoDev-Accelerometer-LIS3DH-MicroPython-Module/blob/abcb4337020434af010f2325b061e694b808316d/PiicoDev_LIS3DH.py#L118C1-L118C1
    def set_brightness_level(self):
        print('TODO: COMPLETE THIS FUNCTION')

    def set_filter(self, effect):
        self._write_reg(self.CAM_REG_COLOR_EFFECT_CONTROL, effect)
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
            print('TODO UPDATE: For best results set a White Balance setting')

        self.white_balance_mode = register_value
        self._write_reg(self.CAM_REG_WB_MODE_CONTROL, register_value)
        self._wait_idle()

##################### INTERNAL FUNCTIONS - HIGH LEVEL #####################

########### CORE PHOTO FUNCTIONS ###########
    def _clear_fifo_flag(self):
        self._write_reg(self.ARDUCHIP_FIFO, self.FIFO_CLEAR_ID_MASK)

    def _start_capture(self):
        self._write_reg(self.ARDUCHIP_FIFO, self.FIFO_START_MASK)

    def _set_capture(self):
        self._clear_fifo_flag()
        self._wait_idle()
        self._start_capture()
        while (self._get_bit(self.ARDUCHIP_TRIG, self.CAP_DONE_MASK) == 0):
            sleep_ms(1)
        self.received_length = self._read_fifo_length()
        self.total_length = self.received_length
        self.burst_first_flag = False
    
    def _read_fifo_length(self): # TODO: CONFIRM AND SWAP TO A 3 BYTE READ
        len1 = int.from_bytes(self._read_reg(self.FIFO_SIZE1),1)
        len2 = int.from_bytes(self._read_reg(self.FIFO_SIZE2),1)
        len3 = int.from_bytes(self._read_reg(self.FIFO_SIZE3),1)
        print(len1,len2,len3)
        return ((len3 << 16) | (len2 << 8) | len1) & 0xffffff

    def _get_sensor_config(self):
        camera_id = self._read_reg(self.CAM_REG_SENSOR_ID);
        self._wait_idle()
        if (int.from_bytes(camera_id, 1) == self.SENSOR_3MP_1) or (int.from_bytes(camera_id, 1) == self.SENSOR_3MP_2):
            self.camera_idx = '3MP'
        if (int.from_bytes(camera_id, 1) == self.SENSOR_5MP_1) or (int.from_bytes(camera_id, 1) == self.SENSOR_5MP_2):
            self.camera_idx = '5MP'


##################### INTERNAL FUNCTIONS - LOW LEVEL #####################
        
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
        return data # TODO: Check that this should return raw bytes or int (int.from_bytes(data, 1))

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




################################################################## CODE ACTUAL ##################################################################
spi = SPI(0,sck=Pin(18), miso=Pin(16), mosi=Pin(19))
cs = Pin(17, Pin.OUT)


onboard_LED = Pin(25, Pin.OUT)

cam = camera(spi, cs)

sleep_ms(1000)

print('starting loop')
onboard_LED.on()
#cam.set_white_balance('office')
cam.capture_jpg()
print('took photo')
sleep_ms(1000)
cam.saveJPG('image.jpg')
onboard_LED.off()




#################################################################################################################################################


# Initialise camera - 
# cam = LIBRARY.camera(spi, cs)

# Set parameters
# cam.brightness = OPTIONS
# cam.resolution = OPTIONS
# cam.effects = OPTIONS
# ECT...

# Get parameters
# cam.getModel


# Take photo
# cam.capture_jpg("/path/to/image.jpg")
'''
Append filename with warning if '.jpg' is not included
'''


