import random
from itertools import count
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as fan

plt.style.use('fivethirtyeight')

class Particle:
    def __init__(self, vx, vy):
        self.ymax = 100
        self.xmax = 100
        self.xpos = random.randint(0, 100)
        self.ypos = random.randint(0, 100)
        self.color = random.randint(0, 2550)
        self.vx = vx
        self.vy = vy
    def update(self, time):
        if self.xpos + self.vx > self.xmax:
            self.vx = -1 * self.vx
        if self.ypos + self.vy > self.ymax:
            self.vy = -1 * self.vy
        if self.xpos + self.vx < 0:
            self.vx = -1 * self.vx
        if self.ypos + self.vy < 0:
            self.vy = -1 * self.vy
        self.xpos = self.xpos + self.vx
        self.ypos = self.ypos + self.vy

particles = []
for i in range(1000):
    particles.append(Particle(random.random() * 5, random.random() * 5))
x_vals = []
y_vals = []
ax = plt.scatter([0, 100, 0], [0, 100, 0])
i = 0
def animate(t):
    frames = [[0, 0], [100, 100]]
    colors = [0, 1]
    i = 2
    for p in particles:
        frame = []
        p.update()
        frame.append(p.xpos)
        frame.append(p.ypos)
        frames.append(frame)
        colors.append(p.color)
        i = i + 2
    ax.set_offsets(frames)
    ax.set_array(np.array(colors))

a = fan(plt.gcf(), animate, interval=30)

plt.tight_layout()
plt.show()
