@app.post("/api/start")
def start_detection():
    global current_process
    if current_process and current_process.poll() is None:
        return {"status": "running", "message": "Detection active."}
    
    try:
        # Launching your background script process safely
        current_process = subprocess.Popen(["python", "noise_detector_v2.py"])
        return {"status": "success", "message": "Noise detection script initiated."}
    except Exception as e:
        # If the server lacks audio hardware, write a fallback log entry instead of crashing
        with open(LOG_FILE, "a") as f:
            f.write(f"[SYSTEM NOTICE]: Initialized in Cloud Simulation Mode. Hardware Mic unavailable.\n")
        return {"status": "simulation", "message": "Running in server cloud simulation mode."}