import matplotlib.pyplot as plt
import numpy as np

from models import Point, Segment


def plot_points(points: list[Point], figsize=(10, 10)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect("equal")
    ax.invert_yaxis()
    xs = [int(p.x) for p in points]
    ys = [int(p.y) for p in points]
    w, h = max(xs), max(ys)
    img = np.full((h + 1, w + 1), 255, dtype=np.uint8)
    for x, y in zip(xs, ys):
        img[y, x] = 0
    ax.imshow(img, cmap="gray", origin="upper", interpolation="none")
    plt.axis("off")
    return fig


def scatter_points(points: list[Point], figsize=(10, 10)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect("equal")
    ax.invert_yaxis()
    xs = [p.x for p in points]
    ys = [p.y for p in points]
    ax.scatter(xs, ys, color="red", s=1)
    plt.axis("off")
    return fig


def plot_segments(segments: list[Segment], figsize=(10, 10)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect("equal")
    ax.invert_yaxis()
    for seg in segments:
        xs = [p.x for p in seg.points]
        ys = [p.y for p in seg.points]
        ax.plot(xs, ys, color="black", linewidth=0.5)
    plt.axis("off")
    return fig
