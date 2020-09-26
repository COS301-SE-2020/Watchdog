from face_detection import FastMTCNN
from PIL import Image
import torch

"""
   This demonstrates how to use the face_detection module
   Expected output:
	Image ID: 0 Detected Face: True
	Image ID: 1 Detected Face: False
"""
# NB: include the following instantiations below
# optimisations if GPU is present
device = 'cuda' if torch.cuda.is_available() else 'cpu'

fast_mtcnn = FastMTCNN(
    stride=4,
    min_confidence=90,
    resize=1,
    margin=14,
    factor=0.6,
    keep_all=True,
    device=device
)
ROOT = '../data/sample/'
filenames = ['face_in_image.jpg', 'face_not_in_image.jpg']
frames = [Image.open(ROOT+file) for file in filenames]

for i, frame in enumerate(frames):
    face_detected = fast_mtcnn(frame)
    print(f"Image ID: {i} Detected Face: {face_detected}")
