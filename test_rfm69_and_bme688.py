import unittest
import RPi.GPIO as GPIO
from rfm69_and_bme688 import bytes_data

class TestRfm69AndBme688(unittest.TestCase):
    
    def test_btyes_data(self):
        
        # Given
        temp_values = "24"
        pressure_values = "1018"
        gas_values = "516"
        humidity_values = "50"
        node_id = "xEm-47"
        expected_data = b'24,1018,516,50.0,xEm-47'
        
        # When
        result = bytes_data(temp_values, pressure_values, gas_values, humidity_values, node_id)
        
        # Then
        self.assertEqual(result, expected_data)

    # The rest of the functions rely on hardware to give realistic test results
        
    
if __name__ == '__main__':
    unittest.main()