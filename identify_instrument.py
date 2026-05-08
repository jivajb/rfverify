import pyvisa

RESOURCE_NAME = "PASTE_RESOURCE_HERE"

rm = pyvisa.ResourceManager()
inst = rm.open_resource(RESOURCE_NAME)

print(inst.query("*IDN?"))