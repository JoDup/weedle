
import asyncio
from kasa import SmartPlug
from pprint import pformat as pf

plug = SmartPlug("172.27.0.69")
asyncio.run(plug.update())
print("Hardware: %s" % pf(plug.hw_info))
print("Full sysinfo: %s" % pf(plug.sys_info))

print("Current state: %s" % plug.is_on)

