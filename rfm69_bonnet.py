import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
import adafruit_rfm69

# Button A
buttonA = DigitalInOut(board.D5)
buttonA.direction = Direction.INPUT
buttonA.pull = Pull.UP

# Button B
buttonB = DigitalInOut(board.D6)
buttonB.direction = Direction.INPUT
buttonB.pull = Pull.UP

# Button C
buttonC = DigitalInOut(board.D12)
buttonC.direction = Direction.INPUT
buttonC.pull = Pull.UP

# Creating the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# OLED display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)

# Clearing the display.
display.fill(0)
display.show()
width = display.width
height = display.height

# Configure the packet radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, 433.0)
prev_packet = None

# Checking the temperature status of the bonnet, so that hardware is functioning correctly
print('Temperature: {} degrees C'.format(rfm69.temperature))

while True:
    packet = None
    # draw a box to clear the image
    display.fill(0)
    display.text('Emanate Radio', 35, 0, 1)

    # check for packet rx (receive)
    packet = rfm69.receive()
    if packet is None:
        display.show()
        display.text('Waiting for packet..', 1, 20, 1)
    else:
        # Display the packet text and rssi
        display.fill(0)
        prev_packet = packet
        packet_text = str(prev_packet, "utf-8")
        display.text('MESSAGE RECEIVED: ', 0, 0, 1)
        display.text(packet_text, 25, 0, 1)
        time.sleep(0.5)

    if not buttonA.value:
        # Send Button A
        display.fill(0)
        button_a_data = bytes("Button A!\r\n","utf-8")
        rfm69.send(button_a_data)
        display.text('Sent Button A!', 25, 15, 1)
        
    elif not buttonB.value:
        # Send Button B
        display.fill(0)
        button_b_data = bytes("Button B!\r\n","utf-8")
        rfm69.send(button_b_data)
        display.text('Sent Button B!', 25, 15, 1)
        
    elif not buttonC.value:
        # Send Button C
        display.fill(0)
        button_c_data = bytes("Button C!\r\n","utf-8")
        rfm69.send(button_c_data)
        display.text('Sent Button C!', 25, 15, 1)

    display.show()
    time.sleep(0.1)