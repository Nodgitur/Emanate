import board
import adafruit_bme680
import time

i2c = board.I2C()
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

#Pressure at sea level for Dublin. This is in hPa.
sensor.sea_level_pressure = 1008

# Defining metrics variables
temperature = sensor.temperature
gas = sensor.gas
altitude = sensor.altitude
humidity = sensor.humidity

while True:
 #   print('Altitude: {:.2f} metres'.format(sensor.altitude))
 print('{:.2f} ohms'.format(sensor.gas))
          
#while True:
    #print('Temperature: {} degrees C'.format(temperature))
    #print('Gas: {} ohms'.format(gas))
    #print('Altitude: {} meters'.format(altitude))
    
    #time.sleep(0.5)