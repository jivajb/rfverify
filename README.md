# RFVerify

**RF Test Automation Framework** — Python + OpenTAP/C#

RFVerify is a modular RF test automation framework that synthesizes configurable signals, injects real-world impairments, and automatically validates signal quality with PASS/FAIL results. It mirrors the architecture of production RF test systems — with a Python core for signal analysis and an OpenTAP/C# prototype demonstrating how the same validation logic integrates into Keysight's PathWave test environment.

---

## Features

- **Signal Synthesis** — Configurable frequency, amplitude, noise level, harmonic distortion, and external interference injection
- **Time-Domain Analysis** — Oscilloscope-style measurements: amplitude, RMS, noise floor, transient spike detection
- **Frequency-Domain Analysis** — FFT-based spectrum analysis with DC removal, peak detection, harmonic classification, and interference identification
- **Automated Pass/Fail Engine** — `RFTestRunner` evaluates frequency accuracy, harmonic count, and interference against configurable thresholds
- **OpenTAP Integration** — C# prototype (`RFSignalValidationStep`) packages the validation workflow as a formal, Verdict-based test step deployable in Keysight's PathWave Test Automation environment

---

## Architecture

```
rfverify/
├── instruments/
│   ├── signal_generator.py     # Signal synthesis + impairment injection
│   ├── spectrum_analyzer.py    # FFT pipeline, peak detection, classification
│   └── oscilloscope.py         # Time-domain measurements
├── tests/
│   └── test_runner.py          # RFTestRunner — automated pass/fail logic
├── main.py                     # Full test workflow execution
├── real_signal_generator.py    # Hardware-ready signal generation layer
└── rf-test-automation-opentap/
    └── opentap.cs              # OpenTAP/C# test step prototype
```

---

## How It Works

### 1. Signal Generation
Configure a test signal with real-world impairments:
```python
generator = SignalGenerator()
generator.configure(freq=1_000_000, amp=1.0, noise=0.05)
generator.config_distortion(enabled=True, level=0.8)
generator.config_interference(True, freq=1_500_000, amp=0.4)
time, voltage = generator.generate()
```

### 2. Time-Domain Analysis (Oscilloscope)
```python
oscilloscope = Oscilloscope()
amplitude = oscilloscope.measure_amplitude(voltage)
rms       = oscilloscope.measure_rms(voltage)
noise     = oscilloscope.measure_noise(voltage)
transient = oscilloscope.detect_transient(voltage)
```

### 3. Frequency-Domain Analysis (Spectrum Analyzer)
```python
analyzer = SpectrumAnalyzer(sample_rate_hz=generator.sample_rate_hz)
peak_frequency, freqs, magnitude = analyzer.analyze(voltage)
peak_frequencies = analyzer.find_peaks(freqs, magnitude, threshold=0.05)
classified = analyzer.classify_peaks(peak_frequencies, peak_frequency)
# → [(1000000, '1x Fundamental'), (2000000, '2x Harmonic'), (1500000, 'Interference')]
```

### 4. Automated Pass/Fail
```python
runner = RFTestRunner(expected_freq=1_000_000)
runner.check_frequency_accuracy(peak_frequency)  # tolerance: ±20 kHz
runner.check_interference(classified)
runner.check_harmonics(classified, max_allowed_harmonics=1)
runner.check_amplitude(amplitude)
```

### 5. OpenTAP Test Step (C#)
The `RFSignalValidationStep` packages the same validation logic as a configurable OpenTAP test step with `[Display]` attributes for frequency, interference, and harmonic inputs — outputting a `Verdict.Pass` or `Verdict.Fail` result directly into Keysight's PathWave Test Automation environment.

---

## FFT Pipeline

The spectrum analyzer implements a full DSP pipeline:
1. Compute FFT via `np.fft.fft`
2. Map bins to frequencies with `np.fft.fftfreq`
3. Take magnitude via `np.abs`
4. Isolate positive frequencies (`[:n // 2]`)
5. Remove DC component (`[0] = 0`)
6. Detect dominant peak via `np.argmax`
7. Find all peaks above threshold
8. Classify each peak as fundamental, harmonic (2x, 3x...), or interference

---

## Installation

```bash
git clone https://github.com/jivajb/RFVerify.git
cd RFVerify
pip install -r requirements.txt
python main.py
```

**Requirements:** Python 3.8+, NumPy, matplotlib, PyVISA (for hardware integration)

---

## OpenTAP Integration

The `rf-test-automation-opentap/opentap.cs` file demonstrates how the Python validation workflow can be packaged as a production test step in [Keysight's PathWave Test Automation](https://www.keysight.com/us/en/products/software/pathwave-test-software/pathwave-test-automation-software.html) environment (built on OpenTAP).

To use with OpenTAP:
1. Install [OpenTAP](https://www.opentap.io/)
2. Add `opentap.cs` as a plugin
3. Configure `ExpectedFrequencyHz`, `MeasuredFrequencyHz`, `InterferenceDetected`, `HarmonicCount`
4. Run as a test step — outputs `Verdict.Pass` or `Verdict.Fail`

---

## Hardware Extension

The instrument abstraction layer is structured for real hardware integration via **PyVISA** (GPIB/USB/LAN). `real_signal_generator.py` provides the foundation for connecting to physical signal generators and oscilloscopes.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Signal Analysis | Python, NumPy, matplotlib |
| Test Framework | pytest |
| Instrument Control | PyVISA (GPIB/USB/LAN) |
| Test Automation | OpenTAP, C# (.NET) |
| IDE | Visual Studio / VS Code |
