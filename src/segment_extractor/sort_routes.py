from io_img import load_segment_image
from processing import compute_weight_matrix

def greedy_tsp(weight_matrix: tuple[tuple[int]], start: int = 0):
    n = len(weight_matrix)
    visited = [False] * n
    __path__








