from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import subprocess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOG_FILE = "noise_log.txt"
current_process = None 

@app.get("/api/logs")
def get_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
            return {"status": "success", "logs": list(reversed(lines[-15:]))}
    return {"status": "error", "message": "Log file not found"}

# --- ADD THIS MISSING ROUTE TO FIX THE 404 ---
@app.get("/api/status")
def get_status():
    global current_process
    # Check if the process exists and is actively running
    is_running = current_process is not None and current_process.poll() is None
    return {
        "system_active": True,
        "script_running": is_running,
        "log_size_bytes": os.path.getsize(LOG_FILE) if os.path.exists(LOG_FILE) else 0
    }
# ---------------------------------------------

@app.post("/api/start")
def start_detection():
    global current_process
    if current_process and current_process.poll() is None:
        return {"status": "running", "message": "Detection is already active!"}
    
    current_process = subprocess.Popen(["python", "noise_detector_v2.py"])
    return {"status": "success", "message": "Noise detection script initiated."}

@app.post("/api/stop")
def stop_detection():
    global current_process
    if current_process and current_process.poll() is None:
        current_process.terminate()
        current_process = None
        return {"status": "success", "message": "Noise detection stopped."}
    return {"status": "idle", "message": "No active script process found."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)