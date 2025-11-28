import numpy as np

class ScaraKinematics:
    """SCARA Arm 3DOF. Movement: Rz(q1)Tx(a1)Rz(q2)Tx(a2)Tz(q3)"""
    def __init__(self, a1: float, a2: float, q: np.ndarray, q_dot_max: np.ndarray = None):
        self.__validate_input(q)
        self.q = q.copy()

        self.q_dot_max = None
        if q_dot_max is not None:
            self.__validate_input(q_dot_max)
            self.q_dot_max = q_dot_max.copy()

        self.a1 = a1
        self.a2 = a2

    def set_measurements(self, q1: float = None, q2: float = None, q3: float = None):
        """After doing a measurement, update the internal q state."""
        if q1 is not None:
            self.q[0] = q1
        if q2 is not None:
            self.q[1] = q2
        if q3 is not None:
            self.q[2] = q3

    def get_p(self, q: np.ndarray = None) -> np.ndarray:
        """Returns end-effector position given joint angles q."""
        q = self.__get_q(q)
        q1, q2, q3 = q.flatten()

        p = np.array([
            [self.a1 * np.cos(q1) + self.a2 * np.cos(q1 + q2)],
            [self.a1 * np.sin(q1) + self.a2 * np.sin(q1 + q2)],
            [q3]
        ])
        return p

    def get_jacobian(self, q: np.ndarray = None) -> np.ndarray:
        """Returns the Jacobian matrix at joint angles q."""
        q = self.__get_q(q)
        q1, q2, _ = q.flatten()
        
        J = np.zeros((3,3))
        J[0,0] = - self.a1 * np.sin(q1) - self.a2*np.sin(q1 + q2)
        J[0,1] = - self.a2 * np.sin(q1 + q2)
        J[1,0] = self.a1 * np.cos(q1) + self.a2 * np.cos(q1 + q2)
        J[1,1] = self.a2 * np.cos(q1 + q2)
        J[2,2] = 1
        return J

    def get_p_dot(self, q_dot: np.ndarray, q: np.ndarray = None) -> np.ndarray:
        """Returns the end-effector velocity given joint velocities q_dot."""
        q = self.__get_q(q)
        self.__validate_input(q_dot)

        J = self.get_jacobian(q)
        p_dot = J @ q_dot
        return p_dot

    def get_inverse_jacobian(self, q: np.ndarray, use_pseudo: bool = True) -> np.ndarray:
        """Returns the inverse of the Jacobian matrix at joint angles q."""
        q = self.__get_q(q)
        J = self.get_jacobian(q)
        try:
            J_inv = np.linalg.inv(J)
        except np.linalg.LinAlgError:
            if use_pseudo:
                J_inv = np.linalg.pinv(J)
                print("Jacobiano singular, usando pseudo-inversa")
            else:
                raise
        return J_inv

    def get_q_dot(self, p_dot: np.ndarray, current_q: np.ndarray = None, normalize: bool = False) -> np.ndarray:
        """Computes joint velocities q_dot to move towards desired end-effector position."""
        q = self.__get_q(current_q)
        self.__validate_input(p_dot)

        J_inv = self.get_inverse_jacobian(q)
        q_dot = J_inv @ p_dot
        if normalize and self.q_dot_max is not None:
            q_dot = self.__scale(q_dot, self.q_dot_max)
        return q_dot

    def __get_q(self, q: np.ndarray = None) -> np.ndarray:
        """In case a method doesnt provide q, takes the class value"""
        if q is None:
            return self.q.copy()
        self.__validate_input(q)
        return q.copy()

    def __validate_input(self, q: np.ndarray):
        """Checks that q is a valid input. (3x1 or 3,) ndarray"""
        if not isinstance(q, np.ndarray):
            raise ValueError("q should be an ndarray")
        if q.shape not in [(3,), (3,1)]:
            raise ValueError("q.shape should be (3,) or (3,1)")

    def __scale(self, x: np.ndarray, max_x: np.ndarray) -> np.ndarray:
        """Scales x so that no element exceeds max_x, preserving ratios."""
        ratios = np.abs(x) / max_x
        scale = np.max(ratios)
        if scale > 1:
            return x / scale
        return x
