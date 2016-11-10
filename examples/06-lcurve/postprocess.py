
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    with open("lcurve.txt", "r") as f:
        alphas, errs, costs = [], [], []
        for line in f:
            alpha, err, cost = [float(s) for s in line.split()]
            alphas.append(alpha)
            errs.append(err)
            costs.append(cost)

    alphas, errs, costs = np.array(alphas), np.array(errs), np.array(costs)

    plt.figure()
    plt.plot(np.log(errs), np.log(costs))
    plt.xlabel("log(error)")
    plt.ylabel("log(roughness)")
    plt.show()
