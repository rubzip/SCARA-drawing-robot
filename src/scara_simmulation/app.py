import pygame
import math
from models import ScaraArm
from constants import CENTER, LENGTH_1, LENGTH_2

# --- Configuración ---
WIDTH, HEIGHT = 800, 600
FPS = 60
SCALE = 100
COLOR = (0, 0, 255)

# --- Inicializar Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SCARA Robot Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

# --- Instancia del brazo ---
arm = ScaraArm(LENGTH_1, LENGTH_2)

# --- Función para transformar coordenadas matemáticas a pantalla ---
def to_screen(pos):
    x, y = pos
    return int(WIDTH / 2 + x * SCALE), int(HEIGHT / 2 - y * SCALE)

# --- Loop principal ---
running = True
while running:
    clock.tick(FPS)
    screen.fill((30, 30, 30))

    # --- Manejo de eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        arm.rotate_part_1(True)
    if keys[pygame.K_d]:
        arm.rotate_part_1(False)
    if keys[pygame.K_w]:
        arm.rotate_part_2(True)
    if keys[pygame.K_s]:
        arm.rotate_part_2(False)

    # --- Obtener posiciones ---
    (x1, y1), (x2, y2) = arm.get_vertex_positions(CENTER)
    base_pos = to_screen(CENTER)
    joint1_pos = to_screen((x1, y1))
    end_pos = to_screen((x2, y2))

    # --- Dibujar brazo ---
    pygame.draw.line(screen, COLOR, base_pos, joint1_pos, 5)
    pygame.draw.line(screen, COLOR, joint1_pos, end_pos, 5)
    pygame.draw.circle(screen, COLOR, base_pos, 8)
    pygame.draw.circle(screen, COLOR, joint1_pos, 8)
    pygame.draw.circle(screen, COLOR, end_pos, 8)

    # --- Dibujar info de vértices ---
    info_lines = [
        f"Base: {CENTER}",
        f"Joint1: ({x1:.2f}, {y1:.2f})",
        f"End Effector: ({x2:.2f}, {y2:.2f})",
        f"Angles: θ1={math.degrees(arm.angle_1):.1f}°, θ2={math.degrees(arm.angle_2):.1f}°"
    ]
    for i, line in enumerate(info_lines):
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (10, 10 + i * 20))

    # --- Actualizar pantalla ---
    pygame.display.flip()

pygame.quit()
