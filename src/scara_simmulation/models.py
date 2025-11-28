import math as m
import numpy as np
from src.scara_kinematics.scara_kinematics import ScaraKinematics


class ScaraModel:
    """SCARA 2D arm model for simulation purposes."""
    def __init__(self, length_1: float, length_2: float, max_w1: float, max_w2: float, center: tuple[float, float] = None):
        self.length_1 = length_1
        self.length_2 = length_2

        self.max_w1 = abs(max_w1)
        self.max_w2 = abs(max_w2)
        
        self.angle_1: float = 0.0
        self.angle_2: float = m.pi / 2

        self.center = center if center else (0, 0)

    def rotate(self, w1: float, w2: float, dt: float):
        w1_eff = min(self.max_w1, max(-self.max_w1, w1))
        w2_eff = min(self.max_w2, max(-self.max_w2, w2))

        self.angle_1 += w1_eff * dt
        self.angle_2 += w2_eff * dt

        self.angle_1 = self.angle_1 % (2 * m.pi)
        self.angle_2 = self.angle_2 % (2 * m.pi)

    def get_vertex_positions(self) -> tuple[tuple[float, float], tuple[float, float]]:
        x0, y0 = self.center

        x1 = x0 + self.length_1 * m.cos(self.angle_1)
        y1 = y0 + self.length_1 * m.sin(self.angle_1)

        x2 = x1 + self.length_2 * m.cos(self.angle_1 + self.angle_2)
        y2 = y1 + self.length_2 * m.sin(self.angle_1 + self.angle_2)

        return (x1, y1), (x2, y2)
    
    def get_q(self) -> tuple[float, float]:
        return self.angle_1, self.angle_2
    
    def reset(self, angle_1: float = 0.0, angle_2: float = m.pi / 2):
        self.angle_1 = angle_1
        self.angle_2 = angle_2


class ScaraSimulator:
    """Scara 2D arm simulator using ScaraKinmeatics + ScaraModel."""
    def __init__(self, length_1: float, length_2: float,
                 angle_1: float = 0.0, angle_2: float = 0.0,
                 z: float = 0.0, max_w1: float = 1.0, max_w2: float = 1.0,
                 center: tuple[float, float] = (0,0)):
        
        q = np.array([[angle_1], [angle_2], [z]])
        q_dot_max = np.array([[max_w1], [max_w2], [np.inf]])

        self.kinematics = ScaraKinematics(length_1, length_2, q, q_dot_max=q_dot_max)
        self.arm = ScaraModel(length_1, length_2, max_w1, max_w2, center=center)
        self.target: tuple[float, float] | None = None
        self.center = np.array([[center[0]], [center[1]], [0]])

    def set_target(self, pos: tuple[float, float]):
        """Sets a new target position for the end-effector."""
        self.target = pos

    def update(self, dt: float = 0.016, k: float = 1.0):
        """Updates the arm position towards the target using controller."""
        if self.target_is_achieved():
            return
        
        tx, ty = self.target
        desired_p = np.array([[tx], [ty], [0]]) - self.center

        q1, q2 = self.arm.get_q()
        self.kinematics.set_measurements(q1=q1, q2=q2)

        current_p = self.kinematics.get_p()
        desired_p_dot = desired_p - current_p
        
        q_dot = self.kinematics.get_q_dot(desired_p_dot, normalize=True)
        w1, w2 = q_dot[0,0], q_dot[1,0]
        self.arm.rotate(w1, w2, dt)

        q1, q2 = self.arm.get_q()
        self.kinematics.set_measurements(q1=q1, q2=q2)

    def get_vertices(self) -> tuple[tuple[float, float], tuple[float, float]]:
        """Returns vertex positions for drawing."""
        return self.arm.get_vertex_positions()
    
    def reset(self, angle_1: float = 0.0, angle_2: float = m.pi / 2):
        """Resets the arm to given angles."""
        self.arm.reset(angle_1, angle_2)
        self.kinematics.set_measurements(q1=angle_1, q2=angle_2)
    
    def target_is_achieved(self, eps: float = 0.1) -> bool:
        """Checks if the target position is achieved within a tolerance."""
        if self.target is None:
            return True
        
        tx, ty = self.target
        _, effector = self.get_vertices()
        ex, ey = effector
        return abs(tx - ex) < eps and abs(ty - ey) < eps
