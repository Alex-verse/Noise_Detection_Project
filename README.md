# Noise Detection Project

## Overview
A real-time noise detection and logging system built using Python, FastAPI, and HTML. The application monitors microphone input, visualizes audio activity, and records noise events when sound levels exceed a predefined threshold.

## Features
- Real-time microphone monitoring
- Noise level detection
- Waveform visualization
- Noise event logging
- Web-based interface using FastAPI

## Technologies Used
- Python
- FastAPI
- HTML
- Audio Processing
- Signal Processing

## Project Structure

Noise_Detection_Project/
├── api.py
├── noise_detector.py
├── noise_visual.py
├── index.html
├── noise_log.txt
├── requirements.txt

## How It Works
1. Captures audio from the microphone.
2. Analyzes the incoming audio signal.
3. Displays waveform visualization.
4. Detects high-noise events.
5. Logs noise incidents for future reference.

## Installation

```bash
pip install -r requirements.txt
```

## Run the Project

```bash
python api.py
```

Open the application in your browser and start monitoring noise levels.

## Future Improvements
- AI-based sound classification 
- Database integration
- Email/SMS alerts
- Mobile-friendly dashboard

## Author
Shivam Mishra
