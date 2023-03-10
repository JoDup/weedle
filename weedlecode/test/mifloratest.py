from miflora.miflora_poller import MiFloraPoller
from btlewrap.bluepy import BluepyBackend

mac = '5C:85:7E:B0:40:38'
poller = MiFloraPoller(mac, BluepyBackend)

print("FW: {}".format(poller.firmware_version()))
print("Name: {}".format(poller.name()))
print("Temperature: {}".format(poller.parameter_value('temperature')))
print("Moisture: {}".format(poller.parameter_value('moisture')))
print("Light: {}".format(poller.parameter_value('light')))
print("Conductivity: {}".format(poller.parameter_value('conductivity')))
