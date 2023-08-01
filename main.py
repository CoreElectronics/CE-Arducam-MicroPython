# Arducam port to Pico

from machine import Pin, SPI, reset
# Developing on 1.19
'''
#################### PINOUT ###############
Camera pin - Pico Pin
VCC - 3V3
GND - GND
SCK - GP18
MISO - RX - GP16
MOSI - TX - GP19
CS - GP1
'''

from utime import sleep_ms

############### HIGH LEVEL FUNCTIONS #################

class camera:
    # TODO: Required imports


    # TODOD: COMPLETE Register definitions
    
    # For camera Reset
    CAM_REG_SENSOR_RESET = 0x07
    CAM_SENSOR_RESET_ENABLE = 0x40
    
    # For get_sensor_config
    CAM_REG_SENSOR_ID = 0x40
    
    SENSOR_5MP_1 = 0x81
    SENSOR_3MP_1 = 0x82
    SENSOR_5MP_2 = 0x83
    SENSOR_3MP_2 = 0x84
    
    # Set mode
    CAM_REG_COLOR_EFFECT_CONTROL = 0x27
    SPECIAL_NORMAL = 0x00
    SPECIAL_BW = 0x04
    SPECIAL_GREENISH = 0x20
    
    
    # Device addressing
    CAM_REG_DEBUG_DEVICE_ADDRESS = 0x0A
    DEVICE_ADDRESS = 0x78
    
    # For Waiting
    CAM_REG_SENSOR_STATE = 0x44
    CAM_REG_SENSOR_STATE_IDLE = 0x01
    
    # Setup for capturing photos
    CAM_REG_FORMAT = 0x20
    CAM_REG_CAPTURE_RESOLUTION = 0x21
    
    CAM_IMAGE_PIX_FMT_JPG = 0x01
    RESOLUTION_160X120 = 0x00
    RESOLUTION_320X240 = 0x01
    RESOLUTION_640X480 = 0x02
    RESOLUTION_1920X1080 = 0x80
    CAM_IMAGE_MODE_FHD = 0x07

    # 
    ARDUCHIP_FIFO = 0x04
    FIFO_CLEAR_ID_MASK = 0x01
    FIFO_START_MASK = 0x02
    
    ARDUCHIP_TRIG = 0x44
    CAP_DONE_MASK = 0x04
    
    FIFO_SIZE1 = 0x45
    FIFO_SIZE2 = 0x46
    FIFO_SIZE3 = 0x47
    
    SINGLE_FIFO_READ = 0x3D
    
    ##################### Callable FUNCTIONS #####################
        
    def __init__(self, spi_bus, cs):
        self.cs = cs
        self.spi_bus = spi_bus

        self._write_reg(camera.CAM_REG_SENSOR_RESET, camera.CAM_SENSOR_RESET_ENABLE) # Reset camera
        self._wait_idle()
        self.get_sensor_config() # Get camera sensor information
        self._wait_idle()
        self._write_reg(camera.CAM_REG_DEBUG_DEVICE_ADDRESS, camera.deviceAddress)
        self._wait_idle()
        
        self.pixel_format = self.CAM_IMAGE_PIX_FMT_JPG
        self.mode = self.RESOLUTION_1920X1080
        self.setCameraFilter(self.SPECIAL_NORMAL)
        
        self.received_length = 0
        self.total_length = 0
        self.burst_first_flag = False
        print('camera init')
    '''
    Issue warning if the filepath doesnt end in .jpg (Blank) and append
    Issue error if the filetype is NOT .jpg
    '''
    def capture_JPG(self):
        
        # TODO: CLASSES CALL THE FUNCTION TO UPDATE NEW PIXEL FORMAT AND MODE
        new_pixel_format = 0x00
        new_resolution = 0x00
        
        print('capturing jep')
        # TODO: PROPERTIES TO CONFIGURE THE PIXEL FORMAT
        if new_pixel_format != self.pixel_format:
            self._write_reg(camera.CAM_REG_FORMAT, self.pixel_format) # Set to capture a jpg
            self._wait_idle()
        
        # TODO: PROPERTIES TO CONFIGURE THE RESOLUTION
        if new_resolution != self.mode:
            self.__write_reg(camera.CAM_REG_CAPTURE_RESOLUTION, self.mode) # Set to capture a jpg
            self._wait_idle()

        
        # Start capturing the photo
        self._set_capture()
        print('capture jpg complete')
    
    # TODO: After reading the camera data clear the FIFO and reset the camera (so that the first time read can be used)
    def save_JPG(self,filename):
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
    
    def get_sensor_config(self):
        self.cameraID = self._read_reg(camera.CAM_REG_SENSOR_ID);
        self._wait_idle()
#         print(self.cameraID)
        print('TODO DIFFERENTIATE MODELS')
    
    ##################### LOW LEVEL FUNCTIONS #####################
        
    def _bus_write(self, addr, val):
        self.cs.off()
        self.spi_bus.write(bytes([addr]))
        self.spi_bus.write(bytes([val])) # FixMe only works with single bytes
        self.cs.on()
        sleep_ms(1) # From the Arducam Library
        return 1
    
    def _busRead(self, addr):
        self.cs.off()
        self.spi_bus.write(bytes([addr]))
        data = self.spi_bus.read(1) # Only read second set of data
        data = self.spi_bus.read(1)
        self.cs.on()
        return data
    
    def __write_reg(self, addr, val):
        self._bus_write(addr | 0x80, val)

    def _read_reg(self, addr):
        data = self._busRead(addr & 0x7F)
        return data # TODO: Check that this should return raw bytes or int (int.from_bytes(data, 1))

    ##################### Wrapper FUNCTIONS #####################

    def _read_byte(self):
        self.cs.off()
        self.spi_bus.write(bytes([self.SINGLE_FIFO_READ]))
        data = self.spi_bus.read(1)
        data = self.spi_bus.read(1)
        self.cs.on()
        self.received_length -= 1
        return data
    

    def _wait_idle(self):
        data = self._read_reg(camera.CAM_REG_SENSOR_STATE)
        while ((int.from_bytes(data, 1) & 0x03) == camera.CAM_REG_SENSOR_STATE_IDLE):
            data = self._read_reg(camera.CAM_REG_SENSOR_STATE)
            sleep_ms(2)

    def _set_capture(self):
        self._clear_fifo_flag()
        self._start_capture()
        print('set cap a')
        while (self._get_bit(camera.ARDUCHIP_TRIG, camera.CAP_DONE_MASK) == 0):
            sleep_ms(1)
        print('set cap b')
        self.received_length = self._read_fifo_length()
        self.total_length = self.received_length
        self.burst_first_flag = False
        ###################################################################### FINISH THIS UP
    
    def _read_fifo_length(self): # TODO: CONFIRM AND SWAP TO A 3 BYTE READ
        len1 = int.from_bytes(self._read_reg(camera.FIFO_SIZE1),1)
        len2 = int.from_bytes(self._read_reg(camera.FIFO_SIZE2),1)
        len3 = int.from_bytes(self._read_reg(camera.FIFO_SIZE3),1)
        return ((len3 << 16) | (len2 << 8) | len1) & 0xffffff
        

    def _get_bit(self, addr, bit):
        data = self._read_reg(addr);
        return int.from_bytes(data, 1) & bit;

    def _clear_fifo_flag(self):
        self.__write_reg(camera.ARDUCHIP_FIFO, camera.FIFO_CLEAR_ID_MASK)
        
    def _start_capture(self):
        self.__write_reg(camera.ARDUCHIP_FIFO, camera.FIFO_START_MASK)
        
    def setCameraFilter(self, effect):
        self._writeReg(self.CAM_REG_COLOR_EFFECT_CONTROL, effect)
        self._waitIdle()



################################################################## CODE ACTUAL ##################################################################
spi = SPI(0,sck=Pin(18), miso=Pin(16), mosi=Pin(19))
cs = Pin(17, Pin.OUT)

cam = camera(spi, cs)
sleep_ms(1000) # Delay required for Auto white balance algorithm (AWB), should be run between startup
# TODO: Seemlessly handle this behind the scenes with a blocking delay (ticks_diff)


cam.capture_JPG()

cam.save_JPG('/image.jpg')

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
# cam.captureJPG("/path/to/image.jpg")
'''
Append filename with warning if '.jpg' is not included
'''


