import sounddevice as sd
import numpy as np
import datetime

# ---------- SETTINGS ----------
DURATION = 1         # seconds per chunk
THRESHOLD = 0.001    # adjust based on your environment
LOG_FILE = "noise_log.txt"

# ---------- FUNCTION: CALCULATE RMS ----------
def get_rms(block):
    return np.sqrt(np.mean(block**2))

# ---------- FUNCTION: CALLBACK (RUNS CONTINUOUSLY) ----------
def callback(indata, frames, time, status):
    rms = get_rms(indata)
    if rms > THRESHOLD:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} | Noise detected | RMS: {rms:.6f}\n")
        print(f"🔊 Noise detected | RMS: {rms:.6f}")

# ---------- MAIN PROGRAM ----------
print("🎧 Listening for noise... (Press Ctrl + C to stop)\n")

try:
    with sd.InputStream(callback=callback, channels=1, samplerate=44100, blocksize=int(44100 * DURATION)):
        while True:
            pass

except KeyboardInterrupt:
    print("\n🛑 Detection stopped.")

    # ---------- SUMMARY ----------
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
            total_events = len(lines)
            print(f"\n📊 Total noise events detected: {total_events}")

            print("\n📁 Last few log entries:")
            for line in lines[-5:]:   # last 5 entries
                print(line.strip())

    except FileNotFoundError:
        print("No log file found yet.")
