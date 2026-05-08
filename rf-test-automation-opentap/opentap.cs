using OpenTap;

[Display("RF Signal Validation Step", Group: "RF Test Automation", Description: "Simulates RF Signal Validation and returns pass/fail results")]

public class RFSignalValidationStep: TestStep
{
    [Display("Expected Frequency Hz")]
    public double ExpectedFrequencyHz {get; set;} = 1000000;

    [Display("Measured Frequency Hz")]
    public double MeasuredFrequencyHz {get; set;} = 999000;

    [Display("Inteference Detected")]
    public bool InterferenceDetected {get; set;} = true;

    [Display("Harmonic Count")]
    public int HarmonicCount {get; set;} = 1;

    public override void run()
    {
        double toleranceHz = 20000;
        double error = System.Math.Abs(MeasuredFrequencyHz - ExpectedFrequencyHz);

        Log.Info($"Expected Frequency: {ExpectedFrequencyHz} Hz");
        Log.Info($"Measured Frequency: {MeasuredFrequencyHz} Hz");
        Log.Info($"Frequency Error: {error} Hz");
        Log.Info($"Harmonic Count: {HarmonicCount}");
        Log.Info($"Interference Detected: {InterferenceDetected}");

        if (error <= toleranceHz && !InterferenceDetected){
            UpgradeVerdict(Verdict.Pass);
        }
        else {
            UpgradeVerdict(Verdict.Fail);
        }
    }
}