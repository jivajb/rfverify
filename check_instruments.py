import pyvisa

rm = pyvisa.ResourceManager()

print("Available Instuments:")
resources = rm.list_resources()

if not resources:
    print("No Instruments Found")
else:
    for resource in resources:
        print(resource)
    