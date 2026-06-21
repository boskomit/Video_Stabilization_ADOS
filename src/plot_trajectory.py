import matplotlib.pyplot as plt

def plot_trajectory(trajectory):

    plt.figure(figsize=(10, 5))

    plt.plot(trajectory[:,0], label="X")

    plt.plot(trajectory[:,1], label="Y")

    plt.legend()
    plt.grid()
    plt.show()