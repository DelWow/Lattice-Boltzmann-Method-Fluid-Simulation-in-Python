
# Lattice Boltzmann Method Fluid Simulation in Python

This project implements a 2D fluid flow simulation around a cylinder using the **Lattice Boltzmann Method (LBM)** in Python. The simulation visualizes the flow field evolution over time, showcasing phenomena such as vortex shedding and the formation of a Von Kármán vortex street behind the cylinder.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Simulation Parameters](#simulation-parameters)
  - [Adjusting the Cylinder Obstacle](#adjusting-the-cylinder-obstacle)
- [Results](#results)
- [Code Explanation](#code-explanation)
  - [Functions](#functions)
  - [Key Variables](#key-variables)
  - [Lattice Velocities and Weights](#lattice-velocities-and-weights)
  - [Simulation Steps](#simulation-steps)
- [License](#license)


## Overview

The **Lattice Boltzmann Method** is a computational approach for simulating fluid dynamics. Instead of solving the Navier-Stokes equations directly, LBM models the fluid using particle distribution functions on a discrete lattice mesh, making it highly parallelizable and efficient for certain types of flow simulations.

This project simulates laminar flow past a cylindrical obstacle in a 2D domain, allowing visualization of fluid behavior such as boundary layer formation, flow separation, and vortex dynamics.

## Features

- **2D Fluid Flow Simulation**: Simulate incompressible, laminar flow in two dimensions.
- **Cylinder Obstacle**: Introduce a fixed cylindrical obstacle in the flow field.
- **Visualization**: Real-time visualization of the vorticity (curl) of the flow using Matplotlib.
- **Customizable Parameters**: Adjust grid size, time steps, viscosity, and other simulation parameters.
- **Educational Tool**: Ideal for learning and teaching computational fluid dynamics concepts.

## Prerequisites

- **Python 3.x**
- **NumPy**: For numerical computations.
- **Matplotlib**: For visualization.

Install the required Python packages using pip:

```bash
pip install numpy matplotlib
```

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/lbm-fluid-simulation.git
   cd lbm-fluid-simulation
   ```

2. **Ensure Dependencies are Installed**

   Install the required packages if you haven't already:

   ```bash
   pip install -r requirements.txt
   ```

   *Note: You may need to create a `requirements.txt` file with the dependencies listed.*

## Usage

Run the simulation script:

```bash
python simulation.py
```

*Replace `simulation.py` with the actual filename if different.*

The simulation will start, and a visualization window will display the flow field evolution. The simulation may take some time depending on the number of time steps and grid resolution.

## Simulation Parameters

You can adjust simulation parameters at the beginning of the script to customize the simulation:

```python
Nx = 400          # Grid resolution in x-direction
Ny = 100          # Grid resolution in y-direction
rho0 = 100        # Initial average density
tau = 0.53        # Relaxation time (related to viscosity)
Nt = 30000        # Number of time steps
plot_every = 100  # Visualization update interval
```

- **Grid Resolution (`Nx`, `Ny`)**: Higher values increase accuracy but require more computation.
- **Density (`rho0`)**: Average density of the fluid.
- **Relaxation Time (`tau`)**: Controls the viscosity; smaller values correspond to lower viscosity.
- **Time Steps (`Nt`)**: Total number of iterations; more steps allow the simulation to develop further.
- **Visualization Interval (`plot_every`)**: Frequency of updating the visualization.

### Adjusting the Cylinder Obstacle

The cylinder is defined in the code as:

```python
# Cylindrical boundary
cylinder = np.full((Ny, Nx), False)

for y in range(Ny):
    for x in range(Nx):
        if distance(Nx // 4, Ny // 2, x, y) < 13:
            cylinder[y][x] = True
```

- **Position**: Centered at `(Nx // 4, Ny // 2)`. Modify these values to move the cylinder.
- **Radius**: Currently `13` grid units. Change this value to adjust the size.

## Results

The simulation visualizes the **vorticity** (curl) of the flow field, allowing you to observe complex flow patterns such as vortex shedding behind the cylinder.

![Simulation Snapshot](https://via.placeholder.com/800x400?text=Simulation+Snapshot)

*An example snapshot of the flow field during the simulation.*

## Code Explanation

### Functions

- **`distance(x1, y1, x2, y2)`**: Calculates the Euclidean distance between two points.
- **`main()`**: The main function where the simulation is set up and executed.

### Key Variables

- **`F`**: Distribution function representing particle probabilities in each lattice direction.
- **`rho`**: Fluid density at each lattice point.
- **`ux`, `uy`**: Fluid velocity components in x and y directions.
- **`Feq`**: Equilibrium distribution function used in the collision step.

### Lattice Velocities and Weights

Defined for the D2Q9 model (2 dimensions, 9 velocities):

```python
cxs = np.array([0, 0, 1, 1, 1, 0, -1, -1, -1])
cys = np.array([0, 1, 1, 0, -1, -1, -1, 0, 1])
weights = np.array([4/9, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36])
```

### Simulation Steps

1. **Initialization**: Set up the initial conditions for `F`, `rho`, and the cylinder obstacle.
2. **Main Loop**: Iterate over time steps:
   - **Streaming (Drift)**: Shift the distribution functions according to their velocities.
   - **Boundary Conditions**: Apply reflective boundary conditions at the cylinder surface.
   - **Collision**: Relax the distribution functions towards equilibrium (`Feq`).
   - **Macroscopic Variables**: Compute density and velocity fields.
   - **Visualization**: Plot the curl of the velocity field at specified intervals.


## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

