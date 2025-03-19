import uasyncio as asyncio
from machine import Pin, SPI
import network
import socket
import os
from time import sleep
from Camera import *
import select

def web_page():
    html = """
        <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>
            <body>
                <h1>Hello World</h1>
                <p><img src="image.jpg" /></p>
            </body>
        </html>
    """
    return html




# Initialising the hardware
led = Pin(0, Pin.OUT)
button = Pin(15, Pin.IN, Pin.PULL_UP)

button_was_pressed = False

def button_irq(pin):
    global button_was_pressed
    button_was_pressed = True

button.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_irq)

spi = SPI(0, sck=Pin(18), miso=Pin(16), mosi=Pin(19))
cs = Pin(17, Pin.OUT)
cam = Camera(spi, cs)

sleep(1)  # AWB Warm up

# Function to setup Wi-Fi network
def setup_wifi(ssid, password):
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)
    
    print('AP Mode Is Active, You can Now Connect')
    print('IP Address To Connect to:: ' + ap.ifconfig()[0])


def ready_led_blink(delay):
    sleep(delay)
    led.on()
    sleep(delay)
    led.off()
    sleep(delay)
    led.on()
    sleep(delay)
    led.off()
    

async def take_photo_every_press():
    global button_was_pressed
    while True:
        if button_was_pressed:
            try:
                os.remove('image.jpg')
            except:
                print('No existing file to remove')
            print('starting photo')
            cam.set_resolution(0x01)
            cam.capture_jpg()
            led.on()
            cam.saveJPG('image.jpg')
            led.off()
            button_was_pressed = False  # reset the button press event
            ready_led_blink(0.2)
        await asyncio.sleep(0.5)

async def web_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    poller = select.poll()
    poller.register(s, select.POLLIN)
    ready_led_blink(0.1)
    while True:
        res = poller.poll(1000)  # time in milliseconds
        if res:
            conn, addr = s.accept()
            print('Got a connection from %s' % str(addr))
            request = conn.recv(1024)
            request = str(request)
            
            if 'GET / ' in request:
                response = web_page()
                conn.send(response)
                conn.close()
    
            elif 'GET /image.jpg ' in request:
                try:
                    with open('image.jpg', 'rb') as f:
                        while True:
                            data = f.read(1024)
                            if not data:
                                break
                            while len(data) > 0:
                                bytes_sent = conn.send(data)
                                data = data[bytes_sent:]
                finally:
                    conn.close()
    
            else:
                response = 'File not found'
                conn.send(response)
                conn.close()
        await asyncio.sleep(0)


# Starting asyncio event loop
setup_wifi('NAME1', 'PASSWORD')

loop = asyncio.get_event_loop()
loop.create_task(take_photo_every_press())
loop.create_task(web_server())
loop.run_forever()


