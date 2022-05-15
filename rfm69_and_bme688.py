import RPi.GPIO as GPIO
from time import sleep
import board
import busio
import digitalio
import adafruit_rfm69
import board
import adafruit_bme680


# Bytes to be sent in the packet to the master radio
def bytes_data(temp_values, pressure_values, gas_values, humidity_values, node_id):
    data = bytes(f'{"{:.0f}".format(float(temp_values))},{"{:.0f}".format(float(pressure_values))},{"{:.0f}".format(float(gas_values))},{"{:.1f}".format(float(humidity_values))},{(node_id)}', "utf-8")
    return data

# Sending the packet with a series of blue LED calls signaling that the packet is sent outside of the code
def send_packet(rfm69br_data):
    rfm69.send(rfm69br_data)
    GPIO.setup(12,GPIO.OUT)
    print("Packet sent")
    GPIO.output(12,GPIO.HIGH)
    sleep(0.2)
    GPIO.output(12,GPIO.LOW)
    
# Ensuring that master radio recieved the packet from the node. Brings bidirectional data transfer to project
def receiver_check(packet, node_id):
    if packet is not None:
        packet_text = str(packet, 'utf-8')
        
        # This is an additonal step checking that the packet is the one sent from this node with a red LED
        if packet_text == "Packet received from node " + node_id:
            GPIO.setup(13,GPIO.OUT)
            print("Master radio received packet")
            GPIO.output(13,GPIO.HIGH)
            sleep(0.2)
            GPIO.output(13,GPIO.LOW)
            print('Received: {0}'.format(packet_text))
            
    else:
        print('No packet received!')
    
def run():
    # Will continuously send and receive packets
    while True:
        
        # Defining environmental metrics from BME688 sensor (These are defined in the loop so metrics will update)
        temp_values ='{}'.format(sensor.temperature)
        gas_values = '{}'.format(sensor.gas)
        humidity_values = '{}'.format(sensor.humidity)
        pressure_values = '{}'.format(sensor.pressure)
        humidity_values = '{}'.format(sensor.humidity)
        node_id = 'xEm-10'
    
        rfm69br_data = bytes_data(temp_values, pressure_values, gas_values, humidity_values, node_id)
        
        print(rfm69br_data)
        
        send_packet(rfm69br_data)
        
        # Reciever packet
        packet = rfm69.receive(timeout = 3.0)
    
        receiver_check(packet, node_id)
            
        # There is a sleep of 10 seconds at the end of the program for the sensors to give more accurate readings    
        sleep(10)
    
if __name__ == "__main__":
    
    # Defining GPIO pins
    spi = busio.SPI(board.SCK, MOSI = board.MOSI, MISO = board.MISO)
    cs = digitalio.DigitalInOut(board.CE1)
    reset = digitalio.DigitalInOut(board.D25)

    # Configure the packet radio (Frequency 433MHz)
    rfm69 = adafruit_rfm69.RFM69(spi, cs, reset, 433.0)
    
    # Configuring the BME688 sensor
    i2c = board.I2C()
    sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)
    
    run()