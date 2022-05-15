import RPi.GPIO as GPIO
from time import sleep
import board
import busio
import digitalio
import adafruit_rfm69
import bme688

# Defining GPIO pins
spi = busio.SPI(board.SCK, MOSI = board.MOSI, MISO = board.MISO)
cs = digitalio.DigitalInOut(board.CE1)
reset = digitalio.DigitalInOut(board.D25)

# Printing environmental metrics from BME688 sensor
tempValues ='{} degrees C'.format(bme688.temperature)
gasValues = '{} ohms'.format(bme688.gas)
altitudeValues = '{} meters'.format(bme688.altitude)
humidityValues = '{}%'.format(bme688.humidity)

rfm69 = adafruit_rfm69.RFM69(spi, cs, reset, 433.0)

# Will continuously send and receive packets
while True:
    #print('Temperature: {} degrees C'.format(bme688.temperature))
    #print('Gas: {} ohms'.format(bme688.gas))
    #print('Altitude: {} meters'.format(bme688.altitude))
    #print('Humidity: {}%'.format(bme688.humidity))

    rfm69br_data = bytes(f'\n\n {"{:.2f} metres".format(bme688.sensor.altitude)}', 'utf-8')
    
    rfm69.send(rfm69br_data)
    GPIO.setup(12,GPIO.OUT)
    
    print("Packet sent")
    GPIO.output(12,GPIO.HIGH)
    
    sleep(0.2)
    
    GPIO.output(12,GPIO.LOW)
    
    packet = rfm69.receive(timeout = 3.0)
    
    if packet is not None:
        packet_text = str(packet, 'ascii')
        print('Recieved: {0}'.format(packet_text))
        
    else:
        print('No packet recieved!')
        
    sleep(0.1)