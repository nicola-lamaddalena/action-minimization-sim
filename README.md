The idea of this algorithm is to find the physical trajectory by minimizing the action between two fixed points, applying iteratively a local approximation to update the internal points of a discretized path.

Defining the lagrangian of the system as $L=T-V$, where $T$ is the kinetic energy and $V$ is the potential energy, the true trajectory can be find by minimizing a quantity called the action, defined as $S=\int_{t_0}^{t_1}dt L(x,\dot{x}).$ Applying the condition $\delta S=0$ the Euler-Lagrange equation can be derived.

## Harmonic oscillator
The harmonic oscillator is the simplest system that can be studied using this formalism. Its lagrangian is given by the following equation: $L(x,\dot{x})=\frac{1}{2}m \dot{x}^{2} - \frac{1}{2}k x^{2},$ where $m$ is the mass of the body and $k$ is the elastic costant of the system.

Applying the Principle of least action gives: $\delta S = 0 \iff \delta \frac{1}{2}\left[\int_{t_0}^{t_1}dt (m\dot{x}^{2} - kx^{2})\right] = 0.$

To resolve this problem using a numerical algorithm, first we fix the spatial extremes of the interval, $x_A$ and $x_B$, and then we fix the initial time $t_0$ and the final time $t_f$. After fixing the total number of grid points $N$, we define a costant time step as $\Delta t = \frac{t_f - t_0}{N-1}$. 

For any generic segment between a known point $x_A$ and an unknown adjacent point $x_M$, we must discretize both velocity and position. The velocity is approximated as the finite difference $v=(x_M-x_A)/\Delta t$, while the spatial coordinate for the potential energy is approximated as the midpoint $\bar{x}=(x_A+x_M)/2$.
Substituting these into the lagrangian yields the discrete lagrangian for a single segment: $L_{discrete}=\frac{1}{2}m\left(\frac{x_M-x_A}{\Delta t}\right)^2 - \frac{1}{2}k\left(\frac{x_A+x_M}{2}\right)^2$.

Considering the two adjacent segments (from $x_A$ to $x_M$, and from $x_M$ to $x_B$), the action, which is an integral in the continuum, can be approximated as the sum of two rectangles with base $\Delta t$ and height given by the value of the lagrangian in each interval: $S_{discrete}=\Delta t (L_1 + L_2).$ By plugging in our descrete approximations, we can express the action of this sub-system purely as a function of $x_M$. We then apply the Principle of least action by taking the derivative with respect to the unknown coordinate $x_M$ and setting it equal to zero: $\frac{\partial S_{discrete}}{\partial x_M}=0.$

This yields an explicit formula to calculate the optimal position for any point given its two neighbors. By applying this update rule iteratively and simultaneously to all internal points of the grid (relaxation method), the system evolves toward the physical trajectory. The algorithm stops when the variation of the total action between successive iterations falls below a chosen tollerance ($\varepsilon$).

