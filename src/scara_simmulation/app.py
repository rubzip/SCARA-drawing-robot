import math as m
import numpy as np
import pygame
import sys

from .constants import WIDTH, HEIGHT, L1, L2, CENTER, MAX_R, MAX_W1, MAX_W2
from .models import ScaraSimulator

WHITE = (255, 255, 255)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

sim = ScaraSimulator(L1, L2, center=CENTER, max_w1=MAX_W1, max_w2=MAX_W2)
is_running = False

target = list(CENTER)
sim.set_target(target)

font = pygame.font.SysFont(None, 28)

while True:
    dt = clock.get_time() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                is_running = not is_running
            if event.key == pygame.K_r:
                sim.reset()
                target = list(CENTER)
                sim.set_target(target)

    # Move target with arrows
    keys = pygame.key.get_pressed()
    speed = 200 * dt
    if keys[pygame.K_UP]: target[1] -= speed
    if keys[pygame.K_DOWN]: target[1] += speed
    if keys[pygame.K_LEFT]: target[0] -= speed
    if keys[pygame.K_RIGHT]: target[0] += speed

    # Limit target inside circle
    dx = target[0] - CENTER[0]
    dy = target[1] - CENTER[1]
    dist = m.hypot(dx, dy)
    if dist > MAX_R:
        target[0] = CENTER[0] + dx * MAX_R / dist
        target[1] = CENTER[1] + dy * MAX_R / dist

    sim.set_target(tuple(target))

    if is_running:
        sim.update(dt)

    screen.fill((25, 25, 25))

    # Draw arm
    (x1, y1), (x2, y2) = sim.get_vertices()
    pygame.draw.line(screen, WHITE, CENTER, (x1, y1), 5)
    pygame.draw.line(screen, WHITE, (x1, y1), (x2, y2), 5)
    pygame.draw.circle(screen, WHITE, CENTER, 10)
    pygame.draw.circle(screen, WHITE, (int(x1), int(y1)), 8)
    pygame.draw.circle(screen, WHITE, (int(x2), int(y2)), 10)

    # Draw target
    pygame.draw.circle(screen, RED, (int(target[0]), int(target[1])), 10)

    # UI
    screen.blit(font.render(f"SPACE = Run/Pause  |  State: {'RUNNING' if is_running else 'STOPPED'}", True, (255,255,255)), (20,20))
    screen.blit(font.render("Arrow keys = Move target", True, (255,255,255)), (20,50))
    screen.blit(font.render("R = Reset", True, (255,255,255)), (20,80))

    pygame.display.flip()
    clock.tick(60)
