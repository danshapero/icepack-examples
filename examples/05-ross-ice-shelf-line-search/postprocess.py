
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    with open("costs.txt", "r") as costs_file:
        slope = float(costs_file.readline())
        beta_min, cost_min = [float(s) for s in costs_file.readline().split()]

        betas, costs = [], []
        for line in costs_file:
            beta, cost = [float(s) for s in line.split()]
            betas.append(beta)
            costs.append(cost)

    betas = np.array(betas)
    costs = np.array(costs)

    N = np.size(betas)
    A = np.zeros((N, 3))
    A[:, 0] = np.ones(N)
    A[:, 1] = betas
    A[:, 2] = betas**2

    x, _, _, _ = np.linalg.lstsq(A, costs)

    fig = plt.figure()
    ax = fig.gca()
    ax.scatter(betas, costs, color = 'b')
    ax.scatter([beta_min], [cost_min], color = 'r')

    Betas = np.sort(betas)
    ax.plot(Betas, x[0] + x[1] * Betas + x[2] * Betas**2, color = 'k')

    plt.show()
