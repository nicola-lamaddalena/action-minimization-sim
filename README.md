# Action Minimization Trajectory Simulation

The goal of this algorithm is to find the physical trajectory of a system by minimizing the action between two fixed points, applying a local approximation iteratively to update the internal points of a discretized path.

## Theoretical Framework

Defining the Lagrangian of the system as:

$$
L = T - V
$$

where $T$ is the kinetic energy and $V$ is the potential energy, the physical trajectory is found by minimizing the action $S$:

$$
S = \int_{t_0}^{t_1} L(x, \dot{x}) \, dt
$$

Applying the Principle of Least Action ($\delta S = 0$) yields the classical Euler-Lagrange equations of motion.

## The Harmonic Oscillator

The simple harmonic oscillator is described by the Lagrangian:

$$
L(x, \dot{x}) = \frac{1}{2}m \dot{x}^{2} - \frac{1}{2}k x^{2}
$$

where $m$ is the mass and $k$ is the elastic constant. The stationary action condition is written as:

$$
\delta \int_{t_0}^{t_1} \left( \frac{1}{2}m\dot{x}^{2} - \frac{1}{2}kx^{2} \right) dt = 0
$$

## Discretization Scheme

To solve this problem numerically, we fix the boundary spatial coordinates $x(t_0) = x_0$ and $x(t_f) = x_f$. Given $N$ total grid points, the constant time step is:

$$
\Delta t = \frac{t_f - t_0}{N - 1}
$$

For any interval between two adjacent points $x_A$ and $x_M$, velocity is approximated via finite differences and position via the midpoint coordinate:

$$
v = \frac{x_M - x_A}{\Delta t}
$$

$$
\bar{x} = \frac{x_A + x_M}{2}
$$

Substituting these approximations into the Lagrangian yields the discrete Lagrangian for a single segment:

$$
L_{\text{discrete}} = \frac{1}{2}m \left( \frac{x_M - x_A}{\Delta t} \right)^2 - \frac{1}{2}k \left( \frac{x_A + x_M}{2} \right)^2
$$

## Step-by-Step Derivation of the Update Rule

Consider two adjacent segments spanning three consecutive points: $x_A$ (left neighbor), $x_M$ (unknown middle point), and $x_B$ (right neighbor). The local discrete action $S_{\text{loc}}$ over these two sub-intervals is:

$$
S_{\text{loc}}(x_M) = \Delta t \left( L_1 + L_2 \right)
$$

Substituting the discrete kinematics gives:

$$
S_{\text{loc}}(x_M) = \Delta t \left[ \frac{1}{2}m \left( \frac{x_M - x_A}{\Delta t} \right)^2 - \frac{1}{2}k \left( \frac{x_A + x_M}{2} \right)^2 + \frac{1}{2}m \left( \frac{x_B - x_M}{\Delta t} \right)^2 - \frac{1}{2}k \left( \frac{x_M + x_B}{2} \right)^2 \right]
$$

To minimize $S_{\text{loc}}$ with respect to $x_M$, we set its partial derivative to zero:

$$
\frac{\partial S_{\text{loc}}}{\partial x_M} = 0
$$

Differentiating term by term:

$$
\Delta t \left[ \frac{m}{\Delta t^2}(x_M - x_A) - \frac{k}{4}(x_A + x_M) - \frac{m}{\Delta t^2}(x_B - x_M) - \frac{k}{4}(x_M + x_B) \right] = 0
$$

Simplifying by removing $\Delta t$ and regrouping terms:

$$
\frac{m}{\Delta t} (2x_M - x_A - x_B) - \frac{k \Delta t}{4} (2x_M + x_A + x_B) = 0
$$

Isolating $x_M$ on the left side:

$$
2x_M \left( \frac{m}{\Delta t} - \frac{k \Delta t}{4} \right) = (x_A + x_B) \left( \frac{m}{\Delta t} + \frac{k \Delta t}{4} \right)
$$

$$
2x_M \left( \frac{4m - k\Delta t^2}{4\Delta t} \right) = (x_A + x_B) \left( \frac{4m + k\Delta t^2}{4\Delta t} \right)
$$

Multiplying both sides by $\frac{2\Delta t}{4m - k\Delta t^2}$ yields the explicit update formula for $x_M$:

$$
x_M = \frac{x_A + x_B}{2} \left( \frac{4m + k\Delta t^2}{4m - k\Delta t^2} \right)
$$

## Stability Limit (Jacobi Conjugate Point Constraint)

According to Jacobi's theorem, the action path represents a strict minimum only if the total simulation time $t_f - t_0$ does not exceed half of the natural oscillation period $T$:

$$
t_f - t_0 < \frac{T}{2} = \pi \sqrt{\frac{m}{k}}
$$

Beyond this time threshold, the path becomes a saddle point, causing the relaxation solver to diverge.

## Relaxation Algorithm

1. Initialize an array $X$ of length $N$ with fixed boundary conditions $X[0] = x_0$ and $X[N-1] = x_f$, using linear interpolation for internal points.

2. Simultaneously update all internal points $X[1:-1]$ using NumPy slicing and the derived update rule.

3. Compute the total action $S$ of the entire discretized path.

4. Repeat iteratively until the absolute change in total action between successive iterations falls below the threshold $\varepsilon$:

$$
\vert{}S_{\text{new}} - S_{\text{old}}\vert{} < \varepsilon
$$