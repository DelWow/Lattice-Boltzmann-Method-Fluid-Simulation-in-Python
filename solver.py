import numpy as np
from matplotlib import pyplot

plot_every = 100

def distance(x1,y1,x2,y2):
    return np.sqrt((x2-x1)**2 + (y2-y1)**2)

def main():
    Nx = 400  # Resolution x-direc
    Ny = 100  # Resolution y-direc
    rho0 = 100  # average density
    tau = .53  # collision timescale
    Nt = 30000  # number of timesteps

    # Lattice speeds and weights
    NL = 9
    idxs = np.arange(NL)
    cxs = np.array([0, 0, 1, 1, 1, 0, -1, -1, -1])
    cys = np.array([0, 1, 1, 0, -1, -1, -1, 0, 1])

    weights = np.array([4 / 9, 1 / 9, 1 / 36, 1 / 9, 1 / 36, 1 / 9, 1 / 36, 1 / 9, 1 / 36])
    X, Y = np.meshgrid(range(Nx), range(Ny))

    # Initial Conditions - flow to the right with potential perturbations
    F = np.ones((Ny, Nx, NL)) + 0.01 * np.random.randn(Ny, Nx, NL)
    F[:,:,3] = 2.3
    rho = np.sum(F, 2)
    for i in idxs:
        F[:, :, i] *= rho0 / rho

    # Cylindrical boundary
    cylinder = np.full((Ny, Nx), False)

    for y in range (0, Ny):
        for x in range (0, Nx):
            if(distance(Nx//4,Ny//2,x,y)<13):
                cylinder[y][x] = True

    # Main loop simulation
    for it in range(Nt):

        F[:, -1, [6,7,8]] = F[:, -2,[6,7,8]]
        F[:, 0, [2, 3, 4]] = F[:, 1,[2, 3, 4]]



        # Drift
        for i, cx, cy in zip(range(NL), cxs, cys):
            F[:, :, i] = np.roll(F[:, :, i], cx, axis=1)
            F[:, :, i] = np.roll(F[:, :, i], cy, axis=0)

        # Setting Reflective Boundaries
        bndryF = F[cylinder, :]
        bndryF = bndryF[:, [0, 5, 6, 7, 8, 1, 2, 3, 4]]

        # Calculate fluid vars
        rho = np.sum(F, 2)
        ux = np.sum(F * cxs, 2) / rho
        uy = np.sum(F * cys, 2) / rho

         # Boundary Apply
        F[cylinder, :] = bndryF
        ux[cylinder] = 0
        uy[cylinder] = 0

        # Collision Apply
        Feq = np.zeros(F.shape)
        for i, cx, cy, w in zip(range(NL), cxs, cys, weights):
            Feq[:, :, i] = rho * w * (
                    1 + 3 * (cx * ux + cy * uy) + 9 * (cx * ux + cy * uy) ** 2 / 2 - 3 *
                    (ux ** 2 + uy ** 2) / 2
                )

        F = F + -(1.0 / tau) * (F - Feq)

        if it % plot_every == 0:
            dUydx = uy[1:-1, 2:] - uy[1:-1, 0:-2]
            dUxdy = ux[2:, 1:-1] - ux[0:-2, 1:-1]
            curl = dUydx - dUxdy

            pyplot.imshow(curl, cmap="bwr")
            pyplot.pause(0.1)
            pyplot.cla()


if __name__ == "__main__":
    main()