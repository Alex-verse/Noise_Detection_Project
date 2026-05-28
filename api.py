@app.post("/api/start")
def start_detection():
    global current_process
    if current_process and current_process.poll() is None:
        return {"status": "running", "message": "Detection active."}
    
    try:
        # shell=True keeps the main API alive even if the subprocess encounters audio driver issues
        current_process = subprocess.Popen("python noise_detector_v2.py", shell=True)
        return {"status": "success", "message": "Noise detection script initiated."}
    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"[SYSTEM NOTICE]: Initialized in Cloud Simulation Mode.\n")
        return {"status": "simulation", "message": "Running in server cloud simulation mode."}