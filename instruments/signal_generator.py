# signal_generator.py
import numpy as np

class SignalGenerator:
    def __init__(self):
        self.frequency_hz = 1000000 # MHz
        self.amplitude_v = 1.0 # volts
        self.sample_rate_hz = 100000000 # Mhz
        self.duration_s = 0.00001
        
        self.noise_level = 0.0
        
        self.enable_distortion = False
        self.distortion_level = 0.0
        
        self.enable_interference = False
        self.interference_freq_hz = 0
        self.interference_amp_v = 0.0
    
    def configure(self, freq, amp, noise):
        self.frequency_hz = freq
        self.amplitude_v = amp
        
        self.noise_level = noise
    
    def config_distortion(self, enabled, level=0.3):
        self.enable_distortion = enabled
        self.distortion_level = level if enabled else 0.0
        
    def config_interference(self, enabled, freq=1500000, amp=0.3):
        self.enable_interference = enabled
        self.interference_freq_hz = freq
        self.interference_amp_v = amp if enabled else 0.0

    
    def generate(self):
        time = np.arange(0, self.duration_s, 1 / self.sample_rate_hz)
        clean_signal = self.amplitude_v * np.sin(2 * np.pi * self.frequency_hz * time)
        
        voltage = clean_signal.copy()
        
        if self.enable_distortion:
            voltage += self.distortion_level * (clean_signal**2)
            
        if self.enable_interference:
            voltage += self.interference_amp_v + np.sin(2 * np.pi * self.interference_freq_hz  * time)
        
        noise = np.random.normal(0, self.noise_level, len(time))
        
        voltage += noise
        
        return time, voltage