from sys import exit

import random
from itertools import combinations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as fan
import math

plt.style.use('fivethirtyeight')

width = 1.0
height = 1.0

class Particle:
    def __init__(self, patch, id, speed=0.01):
        self.id = id
        self.xpos = random.random() * 0.9 + 0.05
        self.ypos = random.random() * 0.9 + 0.05
        self.xpos = 0.5
        self.ypos = 1.75
        self.size = random.random() * 0.03 + 0.01
        self.size = 0.05
        self.color = (random.random(), random.random(), random.random(), 1)
        self.patch = plt.Circle((self.xpos, self.ypos), self.size, color=self.color)
        patch.add_patch(self.patch)
        self.x = self.xpos
        self.y = self.ypos
        self.vx = random.random() * speed
        self.vy = random.random() * speed
        self.vx = -0.1
        self.vy = 0.0
        self.last_collision = None
        self.collision_count = 0
        self.ax = 0
        self.ay = 0
    def update(self):
        soft = 0.000000001
        scaler = 0.0001
        dx = 0.5 - self.x
        dy = 0.5 - self.y
        inv = (dx**2 + dy**2 + soft**2)**(-1.5)
        self.ax = self.ax + dx * inv * scaler
        self.ay = self.ay + dy * inv * scaler
        # self.vx = self.vx * (0.5 - self.x + 1)
        # print(self.vx, (0.5 - self.x + 1))
        # if self.y < 0.5:
        #     self.vy = self.vy + self.ay
        # else:
        #     self.vy = self.vy - self.ay
        # difx = 0.5 - self.x
        # dify = 0.5 - self.y
        # self.vx = difx * 0.001 + self.vx
        # self.vy = dify * 0.001 + self.vy
        # self.vx = self.vx + self.ax
        # self.vy = self.vy + (1.0 - self.y) * self.ay
        self.vx = self.vx + self.ax
        self.vy = self.vy + self.ay
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        # if self.x > 1 - self.size:
        #     self.x = 1 - self.size
        #     self.vx = -self.vx
        # if self.y > 1 - self.size:
        #     self.y = 1 - self.size
        #     self.vy = -self.vy
        # if self.x < 0 + self.size:
        #     self.x = 0 + self.size
        #     self.vx = -self.vx
        # if self.y < 0 + self.size:
        #     self.y = 0 + self.size
        #     self.vy = -self.vy
        self.patch.center = (self.x, self.y)
        # why dont triangle waves work with elastic collision???
        # self.x = math.asin(math.sin(time + self.xpos + self.xphi)) / math.pi + 0.5
        # self.y = math.asin(math.sin(time + self.ypos + self.yphi)) / math.pi + 0.5
        return (self.x, self.y)

particles = []

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(6, 6)

ax = plt.axes(xlim=(-20, 20.0), ylim=(-20, 20.0))

for i in range(1):
    particles.append(Particle(ax, i))
    ax.add_patch(plt.Circle((0.5, 0.5), 0.1))

time = 0
def animate(t):

    for p1, p2 in combinations(particles, 2):
        x = p1.x - p2.x
        y = p1.y - p2.y
        z = math.sqrt(x**2 + y**2)
        if z < (p1.size + p2.size):
            p1.last_collision = p2.id
            p2.last_collision = p1.id
            x = p1.x - p2.x
            y = p1.y - p2.y
            unx = x / math.sqrt(x**2 + y**2)
            uny = y / math.sqrt(x**2 + y**2)
            utx = -uny
            uty = unx
            v1n = p1.vx * unx + p1.vy * uny
            v1t = p1.vx * utx + p1.vy * uty
            v2n = p2.vx * unx + p2.vy * uny
            v2t = p2.vx * utx + p2.vy * uty

            v1tf = v1t
            v2tf = v2t
            v1nf = (v1n * (p1.size - p2.size) + 2.0 * p2.size * v2n) / (p1.size + p2.size)
            v2nf = (v2n * (p2.size - p1.size) + 2.0 * p1.size * v1n) / (p2.size + p1.size)

            v1nfx = v1nf * unx
            v1nfy = v1nf * uny
            v2nfx = v2nf * unx
            v2nfy = v2nf * uny

            v1tfx = v1tf * utx
            v1tfy = v1tf * uty
            v2tfx = v2tf * utx
            v2tfy = v2tf * uty

            dif = p1.size + p2.size - z
            dif = dif / 2.0
            p1.x = p1.x - dif
            p2.x = p2.x + dif
            p1.vx = v1nfx + v1tfx
            p1.vy = v1nfy + v1tfy
            p2.vx = v2nfx + v2tfx
            p2.vy = v2nfy + v2tfy

    for p in particles:
        x, y = p.update()


a = fan(plt.gcf(), animate, interval=10)


# plt.axis('scaled')
plt.show()
