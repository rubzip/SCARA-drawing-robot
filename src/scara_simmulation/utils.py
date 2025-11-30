import json
from .models import ScaraSimulator

def load_segment_img(fname: str) -> list[list[list[float, float]]]:
    with open(fname, 'r') as f:
        segments = json.load(f)
    return segments

def normalize_segments(segments: list[list[list[float, float]]], x_min: float, x_max: float, y_min: float, y_max: float) -> list[list[list[float, float]]]:
    """
    Moves a segment image into rectangle
    """
    all_x = [p[0] for seg in segments for p in seg]
    all_y = [p[1] for seg in segments for p in seg]

    orig_min_x, orig_max_x = min(all_x), max(all_x)
    orig_min_y, orig_max_y = min(all_y), max(all_y)

    orig_width  = orig_max_x - orig_min_x
    orig_height = orig_max_y - orig_min_y
    orig_ratio  = orig_width / orig_height if orig_height != 0 else 1

    dest_width  = x_max - x_min
    dest_height = y_max - y_min
    dest_ratio  = dest_width / dest_height if dest_height != 0 else 1

    if orig_ratio > dest_ratio:
        scale = dest_width / orig_width
        offset_x = x_min
        offset_y = y_min + (dest_height - orig_height * scale) / 2
    else:
        scale = dest_height / orig_height
        offset_x = x_min + (dest_width - orig_width * scale) / 2
        offset_y = y_min

    normalized = []
    for seg in segments:
        new_seg = []
        for x, y in seg:
            nx = (x - orig_min_x) * scale + offset_x
            ny = (y - orig_min_y) * scale + offset_y
            new_seg.append([nx, ny])
        normalized.append(new_seg)

    return normalized

class Drawer:
    def __init__(self, simulator: ScaraSimulator, segments: list[list[list[float, float]]], eps: float = 1.):
        self.simulator = simulator
        self.segments = segments

        self._has_finished = False
        self._is_drawing = False

        self.current_segment = 0
        self.current_point = 0

        point = self.segments[self.current_segment][self.current_point]
        self.simulator.set_target(point)

        self.eps = eps

    def _set_next_target(self):
        if self._has_finished:
            return
        
        self.current_point += 1
        if self.current_point == len(self.segments[self.current_segment]):
            self._is_drawing = False
            self.current_segment += 1
            self.current_point = 0
        else:
            self._is_drawing = True
        
        if self.current_segment == len(self.segments):
            self._has_finished = True
            return
        
        point = self.segments[self.current_segment][self.current_point]
        self.simulator.set_target(point)

    def update(self, dt: float = 0.016):
        self.simulator.update(dt)
        if self.simulator.target_is_achieved(self.eps):
            self._set_next_target()

    def get_vertices(self) -> tuple[tuple[float, float], tuple[float, float]]:
        return self.simulator.get_vertices()
    
    def has_finished(self) -> bool:
        return self._has_finished
    
    def is_drawing(self) -> bool:
        return self._is_drawing
