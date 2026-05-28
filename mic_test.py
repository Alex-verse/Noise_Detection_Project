import sounddevice as sd
import numpy as np

print("=== Sounddevice audio devices ===")
print(sd.query_devices())

sr = 44100
duration = 1.0  # seconds

print(f"\nRecording {duration} second(s) at {sr} Hz. Please make a short sound near the mic...")
recording = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype='float64')
sd.wait()

# compute RMS loudness
rms = np.sqrt(np.mean(recording**2))
print(f"RMS value: {rms:.6f}")

# small check scale comment
if rms < 1e-6:
    print("Note: very small RMS (quiet). Try making a louder sound near the mic and run again.")
else:
    print("Mic test OK.")