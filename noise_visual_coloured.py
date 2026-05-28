# safe_noise_visual.py
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import time
import queue
import threading
import datetime
import sys

# === PARAMETERS ===
DURATION = 0.1           # seconds per audio chunk
THRESHOLD = 0.02         # noise threshold (tune as needed)
SAMPLE_RATE = 44100
BUFFER = 50              # number of readings to display
LOG_FILENAME = "noise_log.txt"

# === QUEUE ===
rms_queue = queue.Queue()

# === AUDIO CALLBACK (must be fast!) ===
def audio_callback(indata, frames, time_info, status):
    # status may contain warnings (overflow) — you can inspect if needed
    # compute rms on first channel (flatten) and push to queue
    try:
        # indata shape: (frames, channels)
        data = indata[:, 0] if indata.ndim > 1 else indata
        rms = float(np.sqrt(np.mean(data.astype('float32')**2)))
        rms_queue.put((time.time(), rms))
    except Exception:
        # never let exceptions escape callback
        return

# === PLOT SETUP (main thread) ===
plt.ion()
fig, ax = plt.subplots()
x = list(range(BUFFER))
rms_values = [0.0] * BUFFER
line, = ax.plot(x, rms_values, color='green', linewidth=2)
ax.set_ylim(0, 0.05)  # adjust initial limit; tune later
ax.set_xlim(0, BUFFER-1)
ax.set_xlabel("Samples (latest)")
ax.set_ylabel("RMS")
ax.set_title("Real-Time Noise Detection (safe)")

# Ensure axes autoscale sensibly
fig.tight_layout()

# === LOG FILE (opened in main thread) ===
log_file = open(LOG_FILENAME, "a", buffering=1)  # line-buffered

print("Starting audio stream... (press Ctrl+C to stop)")

# === START STREAM IN CONTEXT MANAGER ===
stream = None
try:
    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='float32',
        blocksize=int(SAMPLE_RATE * DURATION),
        callback=audio_callback
    )
    stream.start()

    last_plot_time = 0.0
    while True:
        # poll queue — read all pending items (non-blocking)
        got_any = False
        while not rms_queue.empty():
            ts, rms = rms_queue.get()
            got_any = True
            # update buffer
            rms_values.append(rms)
            if len(rms_values) > BUFFER:
                rms_values.pop(0)
            # log if above threshold
            if rms > THRESHOLD:
                tstamp = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
                msg = f"{tstamp} | Noise detected | RMS: {rms:.6f}"
                print("🔴", msg)
                try:
                    log_file.write(msg + "\n")
                except Exception:
                    pass

        # update plot at a reasonable rate (e.g. 10 Hz)
        now = time.time()
        if now - last_plot_time > 0.1:
            try:
                line.set_ydata(rms_values)
                ax.relim()
                ax.autoscale_view(scaley=True)
                # change color if last RMS > threshold
                if rms_values and rms_values[-1] > THRESHOLD:
                    line.set_color('red')
                else:
                    line.set_color('green')
                fig.canvas.draw()
                fig.canvas.flush_events()
            except Exception as e:
                # ignore GUI transient errors
                # print("Plot update error:", e)
                pass
            last_plot_time = now

        time.sleep(0.01)  # small sleep to reduce CPU usage

except KeyboardInterrupt:
    print("\n🛑 Stopped by user (KeyboardInterrupt).")
except Exception as e:
    print("\n❗ Error:", str(e))
    print("Traceback (if any) will be printed below.")
    import traceback
    traceback.print_exc()
finally:
    try:
        if stream is not None:
            stream.stop()
            stream.close()
    except Exception:
        pass
    try:
        log_file.close()
    except Exception:
        pass
    plt.ioff()
    try:
        plt.show()
    except Exception:
        pass
    print("Exited cleanly.")
    sys.exit(0)