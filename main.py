# main.py
import matplotlib.pyplot as plt

from instruments.signal_generator import SignalGenerator 
from instruments.spectrum_analyzer import SpectrumAnalyzer
from instruments.oscilloscope import Oscilloscope

from tests.test_runner import RFTestRunner


def main():
    print("RF Test Automation Framework")
    print("\033[1m------Python version started successfully------\n\033[0m")
    
    # SIGNAL GENERATOR
    generator = SignalGenerator()
    #configuration
    generator.configure(freq=1000000, amp=1.0, noise=0.05)
    generator.config_distortion(enabled=True, level=0.8)
    generator.config_interference(True, freq=1500000, amp=0.4)
    #generation
    time, voltage = generator.generate()

    print(f"\033[1mGenerated {len(voltage)} samples \033[0m")
    
    # OSCILLOSCOPE
    oscilloscope = Oscilloscope()
    
    amplitude = oscilloscope.measure_amplitude(voltage)
    rms = oscilloscope.measure_rms(voltage)
    noise = oscilloscope.measure_noise(voltage)
    transient_spikes = oscilloscope.detect_transient(voltage)
    
    print("\n\033[1mOscilloscope Measurements:\033[0m")
    print(f"Amplitude: {amplitude}")
    print(f"RMS: {rms}")
    print(f"Noise Level: {noise}")
    print(f"Transient Detected: {transient_spikes}")
    
    # Oscilloscope Plot - ONLY first 200 Samples 
    plt.figure()
    plt.plot(time[:200], voltage[:200])
    plt.title("Time Domain Signal - Oscilloscope")
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.grid()

    # SPECTRUM ANALYZER 
    analyzer = SpectrumAnalyzer(sample_rate_hz=generator.sample_rate_hz)
    
    peak_frequency, freqs, magnitude = analyzer.analyze(voltage)

    print(f"\n\033[1mDetected peak frequency:\033[0m {peak_frequency} Hz")
    # peak indices
    threshold = 0.05
    peak_frequencies = analyzer.find_peaks(freqs, magnitude, threshold)
    
    print("\n\033[1mFound Peak Frequencies:\033[0m")
    for i in peak_frequencies[:10]:
        print(f"{i} Hz")
    
    # classification of peaks
    classified = analyzer.classify_peaks(peak_frequencies, peak_frequency)

    print("\n\033[1mClassified Peaks:\033[0m")
    for f, label in classified:
        print(f"{f} Hz -> {label}")
    
    # Spectrum Analyzer Plot
    plt.figure()
    plt.plot(freqs, magnitude)
    plt.title("Frequency Spectrum (Spectrum Analyzer)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.xlim(0, 3000000)
    plt.grid()
    
        
    for f, label in classified:
        plt.axvline(x=f, linestyle='--')
        plt.text(f, max(magnitude)*0.5, label, rotation=90)
        
    #testrunner
    runner = RFTestRunner(expected_freq=1000000)
    #tests
    freq_result, freq_message = runner.check_frequency_accuracy(peak_frequency)
    interference_result, interference_message  = runner.check_interference(classified)
    harmonics_result, harmonics_message = runner.check_harmonics(classified)
    amplitude_result, amplitude_message = runner.check_amplitude(amplitude)
    
    print("\nTest Results")
    print(f"Frequency Test: {freq_result} - {freq_message}")
    print(f"Interference Test: {interference_result} - {interference_message}")
    print(f"Harmonics Test: {harmonics_result} - {harmonics_message}")
    print(f"Amplitude Test: {amplitude_result} - {amplitude_message}")
     
    
    

        
    print("\033[1m\nTests Complete\033[0m")
    print("Showing Plots")
    plt.show()
if __name__ == "__main__":
    main()