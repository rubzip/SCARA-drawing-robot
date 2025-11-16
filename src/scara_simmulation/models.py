import math as m


class ScaraArm:
    def __init__(self, length_1: float, length_2: float, steps: int = 100):
        self.length_1 = length_1
        self.length_2 = length_2
        self.angle_1: float = 0.0
        self.angle_2: float = 0.0

        self.ANGLE_STEP: float = m.pi / steps

    def _rotate_step(self, part: int, is_pos: bool = True):
        direction = 1 if is_pos else -1
        if part == 1:
            self.angle_1 += direction * self.ANGLE_STEP
            self.angle_1 = self.angle_1 % (2 * m.pi)
        elif part == 2:
            self.angle_2 += direction * self.ANGLE_STEP
            self.angle_2 = self.angle_2 % (2 * m.pi)
    
    def rotate_part_1(self, is_pos: bool = True):
        self._rotate_step(1, is_pos)
    
    def rotate_part_2(self, is_pos: bool = True):
        self._rotate_step(2, is_pos)

    Pos = tuple[float, float]
    def get_vertex_positions(self, center: Pos = (0.0, 0.0)) -> tuple[Pos, Pos]:
        x0, y0 = center
        x1 = x0 + self.length_1 * m.cos(self.angle_1)
        y1 = y0 + self.length_1 * m.sin(self.angle_1)

        x2 = x1 + self.length_2 * m.cos(self.angle_1 + self.angle_2)
        y2 = y1 + self.length_2 * m.sin(self.angle_1 + self.angle_2)

        return (x1, y1), (x2, y2)
