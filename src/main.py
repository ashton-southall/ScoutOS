from picozero import pico_led
import network
import socket
import time
import machine
import secrets # Ensure a file named secrets.py is present in file structure, containing SSID details

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
        print("ARNI-SCOUT Connected")
        
def check():
    try:
        pico_led.on()
        led.on()
        wlan = network.WLAN(network.STA_IF)
        
        if wlan.isconnected() == False:
            connect()
            return
        
        addr = socket.getaddrinfo("google.com", 80)[0][-1]  # Resolve Google’s IP
        s = socket.socket()
        s.connect(addr)
        s.settimeout(1)
        s.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")
        response = s.recv(1024)
        print("Ping Success")
        pico_led.off()
        led.off()
        s.close()
        
    except Exception as e:
        print("Ping failed:", e)
        led.on()

led.off()
pico_led.blink(0.1)
print("Booting")
connect()

while True:
    check()
    time.sleep(5)

