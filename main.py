# Implementazione di un algoritmo che, dati due punti, ricostruisce una funzione minimizzando ricorsivamente l'azione.

import numpy as np
import matplotlib.pyplot as plt

N = 100
m, k = 1.0, 2.0
x0, xf = 0, 1
t0, tf = 0, np.floor(2 * np.pi * np.sqrt(m / k)) / 2
dt = (tf - t0) / (N - 1)
eps = 10e-6
points = np.zeros(N, dtype=float)
points[0], points[-1] = x0, xf

def total_action(points: list[float], dt: float, m: float, k: float) -> float:
    x_left, x_right = points[:-1], points[1:]
    v = (x_right - x_left) / dt
    x_mean = 0.5 * (x_left + x_right)
    lag = 0.5 * (m * v**2 - k * x_mean ** 2)

    return dt * np.sum(lag)

def minimum(m: float, k: float, dt: float, xa: float, xb: float) -> float:
    return 0.5 * (xa + xb) * ((4*m + k*dt**2) / (4*m - k*dt**2))

xm = (xf - x0) / 2
S_old = total_action(points, dt, m, k)
diff = 1.0

while diff > eps:
    points[1:-1] = minimum(m, k, dt, points[:-2], points[2:])
    S_new = total_action(points, dt, m, k)
    diff = abs(S_new - S_old)
    S_old = S_new

plt.plot(np.linspace(t0, tf, N), points, marker='o')
plt.title("Traiettoria di Minima Azione")
plt.xlabel("Tempo (s)")
plt.ylabel("Posizione (x)")
plt.grid()
plt.show()
