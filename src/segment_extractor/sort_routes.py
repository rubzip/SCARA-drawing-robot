from models import Segment
from processing import compute_weight_matrix

def greedy_tsp(weight_matrix: tuple[tuple[int]], start: int = 0) -> list[int]:
    n = len(weight_matrix)
    visited = [False] * n
    visited[start] = True
    path = [start]

    for _ in range(n - 1):
        actual = path[-1]
        best_i = None
        best_score = float("inf")

        for i in range(n):
            if visited[i]:
                continue
            current_score = weight_matrix[actual][i]
            if current_score < best_score:
                best_i = i
                best_score = current_score
        
        visited[best_i] = True
        path.append(best_i)
    
    return path

def sort_segments(segments: list[Segment], tsp_algorithm: callable = greedy_tsp):
    w = compute_weight_matrix(segments)
    path = tsp_algorithm(w)
    return [segments[i] for i in path]
