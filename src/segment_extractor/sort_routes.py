from models import Segment

def compute_weight_matrix(segments: list[Segment]) -> list[list[float]]:
    n = len(segments)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        intial_p = segments[i].last()
        for j in range(n):
            if i != j:
                final_p = segments[j].first()
                matrix[i][j] = intial_p.distance(final_p)
    return matrix

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
