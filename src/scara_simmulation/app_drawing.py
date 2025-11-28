import sys
import math as m
import json
from pathlib import Path

import numpy as np
import pygame

from .utils import load_segment_img, normalize_segments, Drawer
from .constants import WIDTH, HEIGHT, L1, L2, CENTER, MAX_R, MAX_W1, MAX_W2
from .models import ScaraSimulator


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BG = (25, 25, 25)
BLUE = (0, 0, 122)

SPEED_MULT = 1.0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SCARA Drawer - non-interactive demo")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

sim = ScaraSimulator(L1, L2, center=CENTER, max_w1=MAX_W1, max_w2=MAX_W2)

segments = None
if len(sys.argv) > 1:
    path = Path(sys.argv[1])
    if path.exists():
        try:
            segments = load_segment_img(str(path))
        except Exception as e:
            print(f"Error cargando {path}: {e}")
            segments = None

if segments is None:
    segments = [
        [[-0.5, 0.0], [0.0, -1.0], [0.5, 0.0]],
        [[0.25, -0.5], [-0.25, -0.5]],
    ]

x_min = CENTER[0]
x_max = CENTER[0] + MAX_R / m.sqrt(2)
y_min = CENTER[1]
y_max = CENTER[1] + MAX_R / m.sqrt(2)

segments_norm = normalize_segments(segments, x_min, x_max, y_min, y_max)
drawer = Drawer(simulator=sim, segments=segments_norm)

trace_segments = []
current_segment = []

running = True
drawing_time = 0.0

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    drawer.update(dt * SPEED_MULT)

    screen.fill(BG)
    BUTTON_RECT = pygame.Rect(10, 120, 100, 30)
    pygame.draw.rect(screen, (100, 100, 255), BUTTON_RECT)
    screen.blit(font.render("Faster", True, WHITE), (15, 125))


    (x1, y1), (x2, y2) = sim.get_vertices()
    if drawer.is_drawing():
        current_point = (int(x2), int(y2))
        current_segment.append(current_point)
    elif current_segment:
        trace_segments.append(current_segment)
        current_segment = []

    for seg in trace_segments:
        if len(seg) > 1:
            pygame.draw.lines(screen, BLUE, False, seg, 3)

    if len(current_segment) > 1:
        pygame.draw.lines(screen, BLUE, False, current_segment, 3)

    if not drawer.has_finished():
        pygame.draw.line(screen, WHITE, CENTER, (x1, y1), 5)
        pygame.draw.line(screen, WHITE, (x1, y1), (x2, y2), 5)
        pygame.draw.circle(screen, WHITE, (int(CENTER[0]), int(CENTER[1])), 8)
        pygame.draw.circle(screen, WHITE, (int(x1), int(y1)), 6)
        pygame.draw.circle(screen, WHITE, (int(x2), int(y2)), 6)

    if sim.target is not None and not drawer.has_finished():
        tx, ty = sim.target
        pygame.draw.circle(screen, RED, (int(tx), int(ty)), 6)

    status = "FINISHED" if drawer.has_finished() else ("DRAWING" if drawer.is_drawing() else "MOVING")
    screen.blit(font.render(f"State: {status}", True, WHITE), (10, 10))
    msg = "DRAWING" if drawer.is_drawing() else "MOVING"
    screen.blit(font.render(msg, True, WHITE), (10, 60))
    screen.blit(font.render(f"Time drawing: {drawing_time:.2f}s", True, WHITE), (10, 90))

    pygame.display.flip()

    if not drawer.has_finished():
        drawing_time += dt * SPEED_MULT

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if BUTTON_RECT.collidepoint(event.pos):
                SPEED_MULT *= 2
                if SPEED_MULT > 16:
                    SPEED_MULT = 16


pygame.quit()
print("Demo finished.")
