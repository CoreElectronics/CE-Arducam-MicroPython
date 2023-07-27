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
    
    # For getSensorConfig
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
    deviceAddress = 0x78
    
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

        self._writeReg(self.CAM_REG_SENSOR_RESET, self.CAM_SENSOR_RESET_ENABLE) # Reset camera
        self._waitIdle()
        self.getSensorConfig() # Get camera sensor information
        self._waitIdle()
        self._writeReg(self.CAM_REG_DEBUG_DEVICE_ADDRESS, self.deviceAddress)
        self._waitIdle()
        
        self.pixel_format = self.CAM_IMAGE_PIX_FMT_JPG
        self.mode = self.RESOLUTION_1920X1080
        self.setCameraFilter(self.SPECIAL_NORMAL)
        
        self.receivedLength = 0
        self.totalLength = 0
        self.burstFirstFlag = False
        print('camera init')
    '''
    Issue warning if the filepath doesnt end in .jpg (Blank) and append
    Issue error if the filetype is NOT .jpg
    '''
    def captureJPG(self):
        
        # TODO: CLASSES CALL THE FUNCTION TO UPDATE NEW PIXEL FORMAT AND MODE
        new_pixel_format = 0x00
        new_resolution = 0x00
        
        print('capturing jep')
        # TODO: PROPERTIES TO CONFIGURE THE PIXEL FORMAT
        if True:#new_pixel_format != self.pixel_format:
            self._writeReg(self.CAM_REG_FORMAT, self.pixel_format) # Set to capture a jpg
            self._waitIdle()
        
        # TODO: PROPERTIES TO CONFIGURE THE RESOLUTION
        if True:#new_resolution != self.mode:
            self._writeReg(self.CAM_REG_CAPTURE_RESOLUTION, self.mode) # Set to capture a jpg
            print('setting res', self.CAM_REG_CAPTURE_RESOLUTION, self.mode)
            self._waitIdle()
        
        # Start capturing the photo
        self._setCapture()
        print('capture jpg complete')
    
    # TODO: After reading the camera data clear the FIFO and reset the camera (so that the first time read can be used)
    def saveJPG(self,filename):
        headflag = 0
        print('starting saving')
        print('rec len:', self.receivedLength)
        
        imageData = 0x00
        imageDataNext = 0x00
        
        imageData_int = 0x00
        imageDataNext_int = 0x00
        
        while(self.receivedLength):
            
            imageData = imageDataNext
            imageData_int = imageDataNext_int
            
            imageDataNext = self._readByte()
            imageDataNext_int = int.from_bytes(imageDataNext, 1) # TODO: CHANGE TO READ n BYTES
            if headflag == 1:
                jpg_to_write.write(imageDataNext)
            
            if (imageData_int == 0xff) and (imageDataNext_int == 0xd8):
                # TODO: Save file to filename
                print('start of file')
                headflag = 1
                jpg_to_write = open(filename,'ab')
                jpg_to_write.write(imageData)
                jpg_to_write.write(imageDataNext)
                
            if (imageData_int == 0xff) and (imageDataNext_int == 0xd9):
                print('TODO: Save and close file?')
                headflag = 0
                jpg_to_write.write(imageDataNext)
                jpg_to_write.close()
    
    def getSensorConfig(self):
        self.cameraID = self._readReg(self.CAM_REG_SENSOR_ID);
        self._waitIdle()
#         print(self.cameraID)
        print('TODO DIFFERENTIATE MODELS')
    
    ##################### LOW LEVEL FUNCTIONS #####################
        
    def _busWrite(self, addr, val):
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
    
    def _writeReg(self, addr, val):
        self._busWrite(addr | 0x80, val)

    def _readReg(self, addr):
        data = self._busRead(addr & 0x7F)
        return data # TODO: Check that this should return raw bytes or int (int.from_bytes(data, 1))

    ##################### Wrapper FUNCTIONS #####################

    def _readByte(self):
        self.cs.off()
        self.spi_bus.write(bytes([self.SINGLE_FIFO_READ]))
        data = self.spi_bus.read(1)
        data = self.spi_bus.read(1)
        self.cs.on()
        self.receivedLength -= 1
        return data
    
    def _waitIdle(self):
        data = self._readReg(self.CAM_REG_SENSOR_STATE)
        while ((int.from_bytes(data, 1) & 0x03) == self.CAM_REG_SENSOR_STATE_IDLE):
            data = self._readReg(self.CAM_REG_SENSOR_STATE)
            sleep_ms(2)

    def _setCapture(self):
        self._clearFIFOFlag()
        self._startCapture()
        print('set cap a')
        while (self._getBit(self.ARDUCHIP_TRIG, self.CAP_DONE_MASK) == 0):
            sleep_ms(1)
        print('set cap b')
        self.receivedLength = self._readFIFOLength()
        self.totalLength = self.receivedLength
        self.burstFirstFlag = False
        ###################################################################### FINISH THIS UP
    
    def _readFIFOLength(self): # TODO: CONFIRM AND SWAP TO A 3 BYTE READ
        len1 = int.from_bytes(self._readReg(self.FIFO_SIZE1),1)
        len2 = int.from_bytes(self._readReg(self.FIFO_SIZE2),1)
        len3 = int.from_bytes(self._readReg(self.FIFO_SIZE3),1)
        print(len1,len2,len3)
        return ((len3 << 16) | (len2 << 8) | len1) & 0xffffff
        

    def _getBit(self, addr, bit):
        data = self._readReg(addr);
        return int.from_bytes(data, 1) & bit;

    def _clearFIFOFlag(self):
        self._writeReg(self.ARDUCHIP_FIFO, self.FIFO_CLEAR_ID_MASK)
        
    def _startCapture(self):
        self._writeReg(self.ARDUCHIP_FIFO, self.FIFO_START_MASK)
        
    def setCameraFilter(self, effect):
        self._writeReg(self.CAM_REG_COLOR_EFFECT_CONTROL, effect)
        self._waitIdle()



################################################################## CODE ACTUAL ##################################################################
spi = SPI(0,sck=Pin(18), miso=Pin(16), mosi=Pin(19))
cs = Pin(17, Pin.OUT)

cam = camera(spi, cs)
sleep_ms(1000) # Delay required for Auto white balance algorithm (AWB), should be run between startup
# TODO: Seemlessly handle this behind the scenes with a blocking delay (ticks_diff)

cam.captureJPG()
cam.saveJPG('/image1.jpg')

cam.captureJPG()
cam.saveJPG('/image2.jpg')

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


