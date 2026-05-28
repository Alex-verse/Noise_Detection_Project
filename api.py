from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import subprocess

app = FastAPI()

# Enable CORS so local development testing still works seamlessly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOG_FILE = "noise_log.txt"
current_process = None 

# Ensure the log file exists so errors aren't thrown on first load
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("System Log Pipeline Initialized.\n")

@app.get("/api/logs")
def get_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
            return {"status": "success", "logs": list(reversed(lines[-15:]))}
    return {"status": "error", "message": "Log file not found"}

@app.get("/api/status")
def get_status():
    global current_process
    is_running = current_process is not None and current_process.poll() is None
    return {
        "system_active": True,
        "script_running": is_running,
        "log_size_bytes": os.path.getsize(LOG_FILE) if os.path.exists(LOG_FILE) else 0
    }

@app.post("/api/start")
def start_detection():
    global current_process
    if current_process and current_process.poll() is None:
        return {"status": "running", "message": "Detection active."}
    
    current_process = subprocess.Popen(["python", "noise_detector_v2.py"])
    return {"status": "success", "message": "Noise detection script initiated."}

@app.post("/api/stop")
def stop_detection():
    global current_process
    if current_process and current_process.poll() is None:
        current_process.terminate()
        current_process = None
        return {"status": "success", "message": "Noise detection stopped."}
    return {"status": "idle", "message": "No active process found."}

# --- SERVE YOUR FRONTEND DIRECTLY FROM THE BACKEND ---
@app.get("/")
def serve_frontend():
    """Serves the main interactive dashboard page at the root URL"""
    return FileResponse("index.html")

if __name__ == "__main__":
    import uvicorn
    # Render explicitly injects a PORT variable. Fallback to 8000 for local hosting.
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)