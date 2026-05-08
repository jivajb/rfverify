import pyvisa

class RealSignalGenerator:
    def __init__(self, resource_name):
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(resource_name)
    
    def identify(self):
        return self.inst.query("*IDN?")
    
    def configure_sine(self, freq_hz=1000000, amp_vpp=1.0):
        self.inst.write("FUNC SIN")
        self.inst.write(f"FREQ {freq_hz}")
        self.inst.write(f"VOLT {amp_vpp}")
        self.inst.write("OUTP ON")
    
    def output_off(self):
        self.inst.write("OUTP OFF")
        