# SkyVis

Real-time object detection and position estimation for aerial surveillance. Teknofest AI in Transportation Competition submission.

## Setup

```bash
# Create environment
conda create -n yarisma python=3.8
conda activate yarisma
pip install -r requirements.txt

# Configure credentials in config/.env
TEAM_NAME=your_team_name
PASSWORD=your_password
EVALUATION_SERVER_URL=https://server-url
SESSION_NAME=your_session_name

# Run
python main.py
```

## Development

**Competition Rule**: Only modify `src/object_detection_model.py`

Train models using `scripts/training.ipynb` and update the model path in `ObjectDetectionModel`:
```python
self.model = YOLO("runs/train/weights/best.pt")
```

## Object Classes

- **Tasit** (0): Vehicle
- **Insan** (1): Human  
- **UAP** (2): UAV
- **UAI** (3): UAI

Landing status: Inilebilir (1), Inilemez (0), Inis Alani Degil (-1)

## License

MIT

