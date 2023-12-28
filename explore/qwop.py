from __future__ import annotations

import copy
import math

import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt

MAX_LENGTH = 40


def get_plan() -> list[float]:
    """
    TODO: make a plan, which is a list of 40 floats between -1.0 and 1.0.

    - The order of nums roughly correlates with the timesteps of the simulation.
    - You can call sim(plan) to get the distance traveled using that plan.
    """
    return [1 for _ in range(MAX_LENGTH)]


# ------------------- Do Not Edit Beyond This Point -------------------


def simulate_qwop(plan: list[float]) -> tuple[float, list[np.ndarray]]:
    """Simulates the game of QWOP."""
    if len(plan) > MAX_LENGTH:
        raise RuntimeError(
            f"Plan has length: {len(plan)}. Should have length {MAX_LENGTH}."
        )
    plan = np.clip(plan, -1.0, 1.0)
    dt = 0.1
    friction = 1.0
    gravity = 0.1
    mass = np.array([30, 10, 5, 10, 5, 10], dtype=float)
    edgel = np.array([0.5, 0.5, 0.5, 0.5, 0.9], dtype=float)
    edgesp = np.array([160.0, 180.0, 160.0, 180.0, 160.0], dtype=float)
    edgef = np.array([8.0, 8.0, 8.0, 8.0, 8.0], dtype=float)
    anglessp = np.array([20.0, 20.0, 10.0, 10.0], dtype=float)
    anglesf = np.array([8.0, 8.0, 4.0, 4.0], dtype=float)

    edge = np.array([[0, 1, 0, 3, 0], [1, 2, 3, 4, 5]], dtype=int)
    angles = np.array([[4, 4, 0, 2], [0, 2, 1, 3]], dtype=int)

    # vel and pos of the body parts, 0 is hip, 5 is head, others are joints
    v = np.zeros((6, 2), dtype=float)
    p = np.array(
        [[0, 1], [0, 0.5], [-0.25, 0], [0.25, 0.5], [0.25, 0], [0.15, 1.9]], dtype=float
    )
    spin = 0.0
    maxspin = 0.0
    lastang = 0.0

    data = []
    for i in range(200):
        # This is equivalent to a nested for loop:
        # for j in range(20):
        #     for k in range(10):  # k = i - j * 5
        j = (i // 10) * 2
        lamb = 0.1 * (i - j * 5) + 0.05
        t0 = ((plan[j - 2] if j > 0 else 0.5) * (1 - lamb)) + (plan[j] * lamb)
        t1 = ((plan[j - 1] if j > 0 else 0.0) * (1 - lamb)) + (plan[j + 1] * lamb)

        contact = p.T[1] <= 0
        clipped_p = np.clip(p.T[1], 0, None)
        if (clipped_p != p.T[1]).any():
            spin = 0
            p.T[1] = clipped_p

        anglesl = [-(2.8 + t0), -(2.8 - t0), -(1 - t1) * 0.9, -(1 + t1) * 0.9]

        disp = p[edge[1]] - p[edge[0]]  # (5, 2)
        dist = np.sqrt(disp.T[0] ** 2 + disp.T[1] ** 2) + 0.01  # (5, )
        dispn = disp.T / dist.T  # (5, 2)
        dispv = v[edge[1]] - v[edge[0]]  # (5, 2)

        distv = 2 * np.sum(disp * dispv, axis=1)  # (5,)

        # Array broadcasting: (5,) * (5, 2) -> (5, 2)
        forceedge = (((edgel - dist) * edgesp - distv * edgef) * dispn).T
        edgeang = np.arctan2(disp.T[1], disp.T[0])  # (5,)
        edgeangv = (dispv.T[0] * disp.T[1] - dispv.T[1] * disp.T[0]) / (dist**2)
        # (5, 2)

        spin += normalize_angle(edgeang[4] - lastang)
        spinc = spin - 0.005 * i
        if spinc > maxspin:
            maxspin = spinc
            lastang = edgeang[4]

        angv = edgeangv[angles[1]] - edgeangv[angles[0]]

        # (4, )
        angf = normalize_angle_array(
            edgeang[angles[1]] - edgeang[angles[0]] - anglesl
        ) * anglessp - angv * anglesf * np.min(dist[angles] / edgel[angles], axis=0)

        # Swap two axes, normalize, multiply first col by -1
        disp[:, [0, 1]] = disp[:, [1, 0]]
        edgetorque = disp / (dist**2).reshape(5, 1)
        edgetorque[:, 0] *= -1

        for z in range(4):
            i0, i1 = angles.T[z]
            forceedge[i0] += angf[z] * edgetorque[i0]
            forceedge[i1] -= angf[z] * edgetorque[i1]

        f = np.zeros((6, 2), dtype=float)
        for z in range(5):
            i0, i1 = edge.T[z]
            f[i0] -= forceedge[z]
            f[i1] += forceedge[z]

        for z in range(6):
            f[z][1] -= gravity * mass[z]
            v[z] += f[z] * dt / mass[z]

            if contact[z]:
                fric = 0.0
                if v[z][1] < 0.0:
                    fric = -v[z][1]
                    v[z][1] = 0.0

                s = np.sign(v[z][0])
                if v[z][0] * s < fric * friction:
                    v[z][0] = 0
                else:
                    v[z][0] -= fric * friction * s
            p[z] += v[z] * dt

        data.append(copy.deepcopy(p.T))
        if contact[0] or contact[5]:
            break

    total_distance = p[5][0]
    print(f"Total distance: {total_distance}")
    return total_distance, data


def normalize_angle_array(ang_arr: np.ndarray) -> float:
    for i, ang in enumerate(ang_arr):
        if ang > math.pi:
            ang_arr[i] -= 2 * math.pi
        elif ang < -math.pi:
            ang_arr[i] += 2 * math.pi
    return ang_arr


def normalize_angle(ang: float) -> float:
    if ang > math.pi:
        ang -= 2 * math.pi
    elif ang < -math.pi:
        ang += 2 * math.pi
    return ang


def create_movie(data: list[np.ndarray], show_movie: bool = True) -> None:
    """
    The following code is given as an example to store a video of the run and to display
    the run in a graphics window. You will treat sim(plan) as a black box objective
    function and maximize it.
    """
    # draw the simulation
    fig = plt.figure()
    fig.set_dpi(100)
    fig.set_size_inches(12, 3)

    ax = plt.axes(xlim=(-1, 12), ylim=(0, 3))

    joints = [5, 0, 1, 2, 1, 0, 3, 4]
    patch = plt.Polygon([[0, 0], [0, 0]], closed=None, fill=None, edgecolor="k")
    head = plt.Circle((0, 0), radius=0.15, fc="k", ec="k")

    def init() -> tuple[plt.Patch, plt.Patch]:
        ax.add_patch(patch)
        ax.add_patch(head)
        return patch, head

    def animate(j: int) -> tuple[plt.Patch, plt.Patch]:
        points = [(data[j][0][i], data[j][1][i]) for i in joints]
        patch.set_xy(points)
        head.center = (data[j][0][5], data[j][1][5])
        return patch, head

    movie = animation.FuncAnimation(
        fig, animate, init_func=init, frames=len(data), interval=20
    )
    movie.save("animation.gif", fps=50)
    if show_movie:
        plt.show()


def graph_plan(plan: np.ndarray) -> None:
    plt.plot(np.arange(MAX_LENGTH), plan)
    plt.xlabel("Timestep")
    plt.ylabel("Action")
    plt.title("QWOP Running Mechanics")
    plt.show()


def main() -> None:
    master_plan = get_plan()
    _, result_data = simulate_qwop(master_plan)
    create_movie(result_data)
    graph_plan(master_plan)


if __name__ == "__main__":
    main()
