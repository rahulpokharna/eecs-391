import matplotlib.pyplot as plt
import numpy as np
import csv
from sklearn.metrics import pairwise_distances_argmin
import random

# Implemented from https://jakevdp.github.io/PythonDataScienceHandbook/05.11-k-means.html 

def kmeans(k):
    data = []
    with open('irisdata.csv', 'rt') as f:
        reader = csv.reader(f)
        for row in reader:
            temp = []
            for x in range(2):
                temp.append(row[x + 2])
            data.append(temp)
        legend = data.pop(0)

    data = np.array(data)
    data = data.astype(np.float)

    centers = []
    for x in range(k):
        cent = [random.uniform(1, 5), random.uniform(0, 2)]
        centers.append(cent)
    centers = np.array(centers)
    print(centers)

    def draw_points(ax, c, factor=1):
        ax.scatter(data[:, 0], data[:, 1], c=c, cmap='viridis',
                s=50 * factor, alpha=0.3)

    def draw_centers(ax, centers, factor=1, alpha=1.0):
        ax.scatter(centers[:, 0], centers[:, 1],
                c=np.arange(k), cmap='viridis', s=200 * factor,
                alpha=alpha)
        ax.scatter(centers[:, 0], centers[:, 1],
                c='black', s=50 * factor, alpha=alpha)

    def make_ax(fig, gs):
        ax = fig.add_subplot(gs)
        ax.xaxis.set_major_formatter(plt.NullFormatter())
        ax.yaxis.set_major_formatter(plt.NullFormatter())
        return ax

    fig = plt.figure(figsize=(15, 4))
    gs = plt.GridSpec(4, 15, left=0.02, right=0.98, bottom=0.05, top=0.95, wspace=0.2, hspace=0.2)
    ax0 = make_ax(fig, gs[:4, :4])
    ax0.text(0.98, 0.98, "Random Initialization", transform=ax0.transAxes,
            ha='right', va='top', size=16)
    draw_points(ax0, 'gray', factor=2)
    draw_centers(ax0, centers, factor=2)

    for i in range(k):
        ax1 = make_ax(fig, gs[:2, 4 + 2 * i:6 + 2 * i])
        ax2 = make_ax(fig, gs[2:, 5 + 2 * i:7 + 2 * i])

        # E-step
        y_pred = pairwise_distances_argmin(data, centers)
        draw_points(ax1, y_pred)
        draw_centers(ax1, centers)

        # M-step
        new_centers = np.array([data[y_pred == i].mean(0) for i in range(k)])
        draw_points(ax2, y_pred)
        draw_centers(ax2, centers, alpha=0.3)
        draw_centers(ax2, new_centers)
        for i in range(k):
            ax2.annotate('', new_centers[i], centers[i],
                        arrowprops=dict(arrowstyle='->', linewidth=1))


        # Finish iteration
        centers = new_centers
        ax1.text(0.95, 0.95, "E-Step", transform=ax1.transAxes, ha='right', va='top', size=14)
        ax2.text(0.95, 0.95, "M-Step", transform=ax2.transAxes, ha='right', va='top', size=14)


    # Final E-step
    y_pred = pairwise_distances_argmin(data, centers)
    axf = make_ax(fig, gs[:4, -4:])
    draw_points(axf, y_pred, factor=2)
    draw_centers(axf, centers, factor=2)
    axf.text(0.98, 0.98, "Final Clustering", transform=axf.transAxes,
            ha='right', va='top', size=16)

kmeans(2)
plt.show()
kmeans(3)
plt.show()