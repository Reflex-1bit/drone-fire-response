# 🔥 Drone Fire Response System

Autonomous drone swarm system for real-time wildfire detection and suppression. Detects fires using a fine-tuned YOLOv8 computer vision model and coordinates a swarm of drones to suppress flames until emergency services arrive.

## Demo

> *(Add demo GIF/video here after recording)*

## How It Works

1. **Detection** — YOLOv8 model fine-tuned on 4,000+ fire/smoke images monitors a live video feed
2. **Alert** — If fire is detected in 3+ consecutive frames, the swarm coordinator is triggered
3. **Dispatch** — Nearest available drone(s) are dispatched to the fire location
4. **Suppression** — Drone(s) hover over the fire and deploy suppressant payload
5. **Dashboard** — Live Flask dashboard shows drone positions, battery, payload, and status in real-time

## Tech Stack

- **Python** — core logic
- **YOLOv8 (Ultralytics)** — real-time fire/smoke detection
- **OpenCV** — video processing
- **Flask** — dashboard backend
- **Threading** — concurrent drone simulation

## Project Structure

```
drone-fire-response/
├── detection/
│   ├── detect.py       # Run fire detection on video/webcam
│   └── train.py        # Fine-tune YOLOv8 on fire dataset
├── simulation/
│   └── swarm_sim.py    # Drone swarm coordination logic
├── dashboard/
│   ├── app.py          # Flask server
│   └── templates/
│       └── index.html  # Live map dashboard
├── data/               # Place your dataset here
└── requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
```

### Run Detection
```bash
python detection/detect.py path/to/video.mp4
# or for webcam:
python detection/detect.py
```

### Train on Fire Dataset
1. Download fire dataset from [Roboflow](https://universe.roboflow.com/search?q=fire+detection) in YOLOv8 format
2. Place in `data/fire_dataset/`
3. Run:
```bash
python detection/train.py
```

### Run Dashboard
```bash
python dashboard/app.py
# Open http://localhost:5000
```

### Run Swarm Simulation
```bash
python simulation/swarm_sim.py
```

## Results

| Metric | Value |
|--------|-------|
| mAP50 | TBD |
| Precision | TBD |
| Recall | TBD |
| Avg dispatch time | TBD |

*(Update after training)*
