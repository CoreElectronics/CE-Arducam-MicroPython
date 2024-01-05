spi = SPI(0,sck=Pin(18), miso=Pin(16), mosi=Pin(19), baudrate=8000000)
cs = Pin(17, Pin.OUT)

# button = Pin(15, Pin.IN,Pin.PULL_UP)
onboard_LED = Pin(25, Pin.OUT)

cam = Camera(spi, cs, debug_information=True)
'''
RESOLUTION_160X120 = 0X00
    RESOLUTION_320X240 = 0X01
    RESOLUTION_640X480 = 0X02
    RESOLUTION_1280X720 = 0X03
    '''


cam.resolution = '640X480'

start_time_capture = utime.ticks_ms()

onboard_LED.on()
cam.capture_jpg()
sleep_ms(200)
cam.saveJPG('image.jpg')
onboard_LED.off()

total_time_ms = utime.ticks_diff(utime.ticks_ms(), start_time_capture)
print('Time take: {}s'.format(total_time_ms/1000))