import json

import cv2
from pathlib import Path
import numpy as np

from models import Point, Segment

def load_img(path: str) -> np.ndarray:
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Error: {path}")
    return img

def save_segment_image(segments: List[Segment], path: str):
    for s in segments:
        if not isinstance(s, Segment):
            raise ValueError("Expected segment class")
    
    json_obj = [s.to_json() for s in segments]
    print(json_obj[:10])
    
    with open(path, 'w') as f:
        json.dump(json_obj, f)

def load_segment_image(path: str) -> List[Segment]:
    with open(path, 'r') as f:
        json_obj = json.load(f)
    
    segments = []
    for seg_data in json_obj:
        points = [Point(x, y) for x, y in seg_data]
        segments.append(Segment(points))
    
    return segments
