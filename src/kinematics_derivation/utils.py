import sympy as sp


def _translation(delta: sp.Symbol, idx: int):
    mat = sp.eye(4)
    mat[idx, 3] = delta
    return mat

def tx(delta: sp.Symbol):
    return _translation(delta, 0)

def tz(delta: sp.Symbol):
    return _translation(delta, 2)

def rz(theta: sp.Symbol):
    mat = sp.eye(4)
    mat[:3, :3] = sp.rot_axis3(theta)
    return mat

if __name__ == "__main__":
    a1, a2, q1, q2, q3 = sp.symbols("a1 a2 q1 q2 q3")
    q = [q1, q2, q3]

    m = sp.simplify(rz(q1) * tx(a1) * rz(q2) * tx(a2) * tz(q3))

    edge = sp.Matrix([0, 0, 0, 1]) 
    p = sp.simplify((m @ edge))[:3, :]

    j = sp.simplify(p.jacobian(q))

    j_inv = sp.simplify(j.inv())

    print("SCARA Robot")
    print("Rz(q1)Tx(a1)Rz(q2)Tx(a2)Tz(q3)")

    print("Transformation matrix. M(q1, q2, q3):")
    sp.pprint(m)

    print("Position. p(q1, q2, q3):")
    sp.pprint(p)

    print("Jacobian. J(q1, q2, q3):")
    sp.pprint(j)

    print("Jacobian. J^-1(q1, q2, q3):")
    sp.pprint(j_inv)
