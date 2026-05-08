#test_runner.py

class RFTestRunner:
    def __init__(self, expected_freq):
        self.expected_frequency_hz = expected_freq
    
    def check_frequency_accuracy(self, measured_frequency, tolerence=20000):
        difference = abs(measured_frequency - self.expected_frequency_hz)
        
        if difference <= tolerence:
            return "PASS", f"Frequency within tolerance ({difference:.2f} Hz Off)"
        else:
            return "FAIL", f"Frequency out of tolerance ({difference:.2f} Hz Off)"
    
    def check_interference(self, classifications):
        interference = [x for x in classifications if x[1] == "Interference" and x[1] != 0]
        if len(interference) == 0:
            return "PASS", f"No Inteference Detected"
        else:
            return "FAIL", f"Detected {len(interference)} Interference peak(s)"
        
    def check_harmonics(self, classifications, max_allowed_harmonics=1):
        harmonics = [x for x in classifications if "Harmonic" in x[1] and "1x" not in x[1]]
        
        if len(harmonics) <= max_allowed_harmonics:
            return "PASS", f"{len(harmonics)} harmonic peak(s) detected"
        else:
            return "FAIL", f"Too many harmonic peaks detected: {len(harmonics)}"
        
    def check_amplitude(self, measured_amp, expected_amp=1.0, tolerance=0.2):
        if abs(measured_amp - expected_amp) <= tolerance:
            return "PASS", f"Amplitude within tolerance"
        else:
            return "FAIL", f"Amplitude out of tolerance"
        