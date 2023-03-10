from pygattlib import GATTRequester, BLEAddressType

import struct

# Set the MAC address of the Govee H5101
DEVICE_MAC = "C6:38:32:31:51:96"

# Define the UUIDs for the temperature and humidity characteristics
TEMPERATURE_CHAR_UUID = "00002a6e-0000-1000-8000-00805f9b34fb"
HUMIDITY_CHAR_UUID = "00002a6f-0000-1000-8000-00805f9b34fb"

# Create a GATTRequester object to connect to the Govee H5101
req = GATTRequester(DEVICE_MAC, False)

# Connect to the device
req.connect(True, address_type=BLEAddressType.random)

# Read the temperature data
temperature_data = req.read_by_uuid(TEMPERATURE_CHAR_UUID)[0]
temperature = struct.unpack("<h", temperature_data)[0] / 100.0

# Read the humidity data
humidity_data = req.read_by_uuid(HUMIDITY_CHAR_UUID)[0]
humidity = struct.unpack("<h", humidity_data)[0] / 100.0

# Print the temperature and humidity data
print("Temperature: {}°C".format(temperature))
print("Humidity: {}%".format(humidity))

# Disconnect from the device
req.disconnect()
