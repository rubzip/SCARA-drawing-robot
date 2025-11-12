from scipy.spatial import KDTree
import numpy as np
import cv2

from models import Point, Segment

def get_border_points(img: np.ndarray, threshold_1: float, threshold_2: float) -> list[Point]:
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    edges = cv2.Canny(blurred, threshold_1, threshold_2)
    coords = np.column_stack(np.where(edges > 0))
    points = [Point(float(x), float(y)) for y, x in coords]
    return points

def points_to_segments_kdtree(points: list[Point], distance_threshold: float = 5) -> list[Segment]:
    if not points:
        return []

    unvisited = set(points)
    segments = []

    coords = np.array([(p.x, p.y) for p in points])
    point_map = {(p.x, p.y): p for p in points}
    kdtree = KDTree(coords)

    while unvisited:
        current = unvisited.pop()
        segment_points = [current]

        for _ in range(2):
            segment_points = segment_points[::-1]
            while True:
                idx_neighbors = kdtree.query_ball_point([segment_points[-1].x, segment_points[-1].y], distance_threshold)
                neighbors = [point_map[tuple(coords[i])] for i in idx_neighbors if point_map[tuple(coords[i])] in unvisited]
                if not neighbors:
                    break
                next_point = min(neighbors, key=lambda q: segment_points[-1].distance(q))
                segment_points.append(next_point)
                unvisited.remove(next_point)

        segments.append(Segment(segment_points))

    return segments

def simplify_segment(segment: Segment, eps: float = 2.) -> Segment:
    """Ramer-Douglas-Peucker algorithm implementation"""
    
    if len(segment) < 2:
        return None

    coords = np.array([[p.x, p.y] for p in segment])
    def _rdp(points: np.ndarray):
        dmax = 0.0
        index = 0
        start, end = points[0], points[-1]
        for i in range(1, len(points) - 1):
            p = points[i]
            d = np.abs(np.cross(end - start, start - p)) / np.linalg.norm(end - start)
            if d > dmax:
                index = i
                dmax = d
        if dmax > eps:
            rec1 = _rdp(points[:index+1])
            rec2 = _rdp(points[index:])
            return np.vstack((rec1[:-1], rec2))
        else:
            return np.vstack((start, end))

    rdp_coords = _rdp(coords)
    simplified_points = [Point(float(x), float(y)) for x, y in rdp_coords]
    simplified_segment = Segment(simplified_points)

    if len(simplified_segment) == 2 and simplified_segment.first().distance(simplified_segment.last()) < eps:
        return None
    return simplified_segment
    
def simplify_segments(segments: list[Segment], eps: float = 2.) -> list[Segment]:
    simplified_segments = [simplify_segment(s, eps) for s in segments]
    filtered_segments = [s for s in simplified_segments if s is not None and len(s) >= 2]
    return filtered_segments

def normalize_segments(segments: list[Segment]) -> list[Segment]:
    min_x = min(min(p.x for p in s) for s in segments)
    min_y = min(min(p.y for p in s) for s in segments)
    max_x = max(max(p.x for p in s) for s in segments)
    max_y = max(max(p.y for p in s) for s in segments)

    w = max(max_x - min_x, max_y - min_y)

    return [
        Segment([
            Point((p.x - min_x) / w, (p.y - min_y) / w) 
            for p in s
        ]) for s in segments
    ]
