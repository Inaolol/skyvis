import torch

if torch.cuda.is_available():
    print("GPU is available! 🎮")
else:
    print("No GPU detected. Using CPU instead. 🏋️‍♂️")
