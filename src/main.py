from picozero import pico_led
import network
import socket
import time
import machine
import secrets # Ensure a file named secrets.py is present in file structure, containing SSID details

pingint = 1

# Initialize an external LED on GPIO 16
led = machine.Pin(16, machine.Pin.OUT)  # Set GPIO 16 as an output

def connect(): # Connect to WLAN - SSID in secrets.py
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    pico_led.blink(0.1)
    wlan.connect(secrets.ssid)
    
    if wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
        
    if wlan.isconnected() == True:
        print(secrets.ssid, "Connected")
        clearStatus()
        
def check():
    try:
        wlan = network.WLAN(network.STA_IF)
        
        if wlan.isconnected() == False:
            connect()
            return
        
        try:
            # Try to open a socket to Google DNS
            pico_led.on()
            sock = socket.socket()
            sock.settimeout(1)
            sock.connect(("8.8.8.8", 53))
            sock.close()
            clearStatus()
            return True
        except:
            led.on()
            return
    except:
        print("Fatal Error: Aborting Check")
        led.blink(0.5)
        return
        
def clearStatus():
    pico_led.off()
    led.off()
    return

led.off()
pico_led.blink(0.1)
print("Booting")
connect()
clearStatus()

while True:
    check()
    time.sleep(pingint)

