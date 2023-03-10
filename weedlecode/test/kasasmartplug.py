from pyHS100 import SmartStrip


p = SmartStrip("172.27.0.69")

# change state of a single outlet
p.turn_off(index=1)
# query and print current state of all outlets




