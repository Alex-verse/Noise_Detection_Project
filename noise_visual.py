import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# Settings
DURATION = 0.5       # seconds per chunk
THRESHOLD = 0.001     # noise threshold
LOG_FILE = "noise_log.txt"

rms_values = []  # store RMS values for plotting
timestamps = []  # store time data

def get_rms(block):
    return np.sqrt(np.mean(block**2))

def callback(indata, frames, time, status):
    rms = get_rms(indata)
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    # Add data for live graph
    rms_values.append(rms)
    timestamps.append(current_time)

    # Keep graph short (last 50 readings)
    if len(rms_values) > 50:
        rms_values.pop(0)
        timestamps.pop(0)

    # Log if noise crosses threshold
    if rms > THRESHOLD:
        with open(LOG_FILE, "a") as f:
            f.write(f"[{datetime.datetime.now()}] Noise detected | RMS: {rms:.6f}\n")
        print(f"🔊 Noise detected | RMS: {rms:.6f}")

plt.ion()  # interactive mode ON
fig, ax = plt.subplots()
line, = ax.plot([], [], 'g-')
ax.set_ylim(0, 0.01)
ax.set_xlabel("Time")
ax.set_ylabel("RMS Level")
ax.set_title("Live Noise Detection")

print("🎧 Listening for noise... (Ctrl+C to stop)\n")

try:
    with sd.InputStream(callback=callback, channels=1, samplerate=44100, blocksize=int(44100 * DURATION)):
        while True:
            if rms_values:
                line.set_xdata(np.arange(len(rms_values)))
                line.set_ydata(rms_values)
                ax.set_xlim(0, len(rms_values))
                plt.pause(0.05)
except KeyboardInterrupt:
    print("\n🛑 Detection stopped.")
    plt.ioff()
    plt.show()
