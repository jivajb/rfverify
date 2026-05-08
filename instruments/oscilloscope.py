#instruments/oscilloscope.py

import numpy as np

class Oscilloscope:
    def __init__(self):
        pass
    
    def measure_amplitude(self, voltage):
        
        return (np.max(voltage) - np.min(voltage)) / 2
    
    def measure_rms(self, voltage):
        return np.sqrt(np.mean(voltage ** 2))
    
    def measure_noise(self, voltage):
        clean = np.mean(voltage)
        noise = voltage - clean
        return np.std(noise)
    
    def detect_transient(self, voltage, threshold=0.2):
        spikes = np.where(np.abs(voltage)>threshold)[0]
        return len(spikes) > 0