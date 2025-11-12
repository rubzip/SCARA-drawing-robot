import matplotlib.pyplot as plt
from typing import List
from models import Segment

def plot_segments(segments: List[Segment], figsize=(10,10)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect("equal")
    ax.invert_yaxis()
    for seg in segments:
        xs = [p.x for p in seg.points]
        ys = [p.y for p in seg.points]
        ax.plot(xs, ys, color='black', linewidth=0.5)
    plt.axis('off')
    return fig
