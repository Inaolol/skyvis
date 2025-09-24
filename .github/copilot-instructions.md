# Copilot Instructions for SkyVis

## Project Overview
SkyVis is a **Teknofest AI in Transportation Competition** submission that implements real-time object detection and position estimation for aerial surveillance. The system connects to a competition evaluation server, downloads frames, processes them with YOLO models, and submits predictions.

## Architecture Components

### Core Pipeline (`main.py`)
1. **Authentication**: Uses `.env` config for team credentials and server URL
2. **Frame Processing**: Downloads frames from competition server via `ConnectionHandler`
3. **Detection**: Processes images through `ObjectDetectionModel` (YOLO-based)
4. **Position Estimation**: Tracks camera movement using optical flow
5. **Submission**: Sends predictions back to evaluation server

### Key Modules

**`src/object_detection_model.py`** - The ONLY file competitors can modify
- Contains YOLO model loading and inference logic
- Implements frame-by-frame processing with FPS control (3 FPS)
- Handles image download/caching and prediction formatting
- Uses hardcoded model path: `"C:/Users/abdir/Desktop/models/best.pt"`

**`src/connection_handler.py`** - Server communication interface
- Handles authentication, frame fetching, and prediction submission
- Caches frames/translations to JSON files to avoid re-downloads
- Never modify this file per competition rules

**`src/position_estimator.py`** - Camera position tracking
- Uses camera calibration parameters for undistortion
- Implements Lucas-Kanade optical flow for position estimation
- Essential for translation prediction tasks

## Development Workflow

### Environment Setup
```bash
conda create -n yarisma python=3.8
conda activate yarisma
pip install -r requirements.txt
```

### Configuration
Create `config/.env` with competition credentials:
```
TEAM_NAME=team_name
PASSWORD=password
EVALUATION_SERVER_URL="competition_server_url"
SESSION_NAME=session_name
```

### Training Pipeline
- Use `scripts/training.ipynb` for YOLO model training
- Dataset utilities in `scripts/`: 
  - `folder2textYolo.py` for train/val splits
  - `visualize_yolo.py` for annotation visualization
  - `Voc_2_yolo.py` for format conversion

### Running System
```bash
python main.py  # Main competition interface
```

## Critical Patterns

### Object Classes (from `constants.py`)
```python
classes = {"Tasit": 0, "Insan": 1, "UAP": 2, "UAI": 3}
landing_statuses = {"Inilebilir": "1", "Inilemez": "0", "Inis Alani Degil": "-1"}
```

### Detection Output Format
- Bounding boxes as `DetectedObject` with landing status classification
- Position translations as `DetectedTranslation` 
- All predictions wrapped in `FramePredictions` for server submission

### Image Processing
- Frames are resized to half dimensions for performance: `(width // 2, height // 2)`
- YOLO inference with `conf=0.4, imgsz=800, device=0`
- Images cached locally in `_images/` directory

## Competition Constraints
- **Only modify `object_detection_model.py`** - all other files are protected
- Model must handle real-time processing (3 FPS target)
- Predictions submitted frame-by-frame to evaluation server
- Health status controls when system should activate (task 2)

## Key Files to Reference
- `src/object_detection_model.py` - Main development file
- `src/position_estimator.py` - Position tracking implementation  
- `scripts/training.ipynb` - Training workflow
- `runs/train/weights/best.pt` - Trained model weights location