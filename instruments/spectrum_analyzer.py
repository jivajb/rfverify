# spectrum_analyzer.py 
# FFT method (Fast Fourier Transform)
import numpy as np

class SpectrumAnalyzer:
    def __init__(self, sample_rate_hz):
        self.sample_rate_hz = sample_rate_hz
    
    def analyze(self, voltage):
        n = len(voltage)
        
        fft_result = np.fft.fft(voltage)
        freqs = np.fft.fftfreq(n, d=1 / self.sample_rate_hz)
        
        magnitude = np.abs(fft_result)
        
        # positive freqs only
        positive_freqs = freqs[:n // 2]
        positive_magnitude = magnitude[:n // 2]
        
        positive_magnitude_no_dc = positive_magnitude.copy()
        positive_magnitude_no_dc[0] =0
        
        # peak freqs
        peak_index = np.argmax(positive_magnitude_no_dc)
        peak_frequency = positive_freqs[peak_index]
        
        return peak_frequency, positive_freqs, positive_magnitude
    
    def find_peaks(self, freqs, magnitude, threshold=0.2):
        max_magnitude = np.max(magnitude)
        peak_indices = np.where(magnitude > threshold * max_magnitude)[0]
        
        peak_frequencies = freqs[peak_indices]
        
        return peak_frequencies
        
    def classify_peaks(self, peak_freqs, fundamental_freq, tolerance=0.05):
        classifications = []
        
        for f in peak_freqs:
            if abs(f) < 1e-9:
                classifications.append((f, "DC"))
                continue
            
            ratio = f / fundamental_freq
            rounded = round(ratio)
            
            if abs(ratio - rounded) < tolerance:
                classifications.append((f, f"Harmonic ({rounded}x)"))
            else:
                classifications.append((f, f"Interference"))
            
        return classifications
        
        
        