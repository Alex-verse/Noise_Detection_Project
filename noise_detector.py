import sounddevice as sd
import numpy as np
import datetime

DURATION = 1       # seconds per chunk
THRESHOLD = 0.0001 # adjust later if too sensitive

LOG_FILE = "noise_log.txt"

def get_rms(block):
    return np.sqrt(np.mean(block**2))

def callback(indata, frames, time, status):
    rms = get_rms(indata)
    if rms > THRESHOLD:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a") as f:
            f.write(f"Noise detected at {timestamp} | RMS: {rms:.6f}\n")
        print(f"🔊 Noise detected | RMS: {rms:.6f}")

print("Listening for noise... (Ctrl+C to stop)")
with sd.InputStream(callback=callback, channels=1, samplerate=44100, blocksize=int(44100 * DURATION)):
    while True:
        pass   