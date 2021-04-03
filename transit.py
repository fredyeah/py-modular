import requests
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as fan

from sys import exit

import smopy


# exit()

plt.style.use('fivethirtyeight')

width = 0.1
height = 0.1
xpos = 13.0
ypos = 51.0

params = {
    "north": ypos + height,
    "west": xpos,
    "south": ypos,
    "east": xpos + width
}

url = "https://v5.vbb.transport.rest/radar"

x_vals = []
y_vals = []

i = 0
def animate(t):
    # global url
    # global params
    data = requests.get(url, params=params).json()
    for d in data:
        x_vals.append(d['location']['longitude'])
        y_vals.append(d['location']['latitude'])
        # print(d)

    map = smopy.Map((xpos, ypos, xpos + width, ypos + height), z=4)
    x, y = map.to_pixels(48.86151, 2.33474)
    ax = map.show_mpl(figsize=(8, 6))
    ax.plot(x, y, 'or', ms=10, mew=2);

    # plt.xlim(xpos, xpos + width)
    # plt.ylim(ypos, ypos + height)
    # plt.cla()
    #
    # plt.plot(x, y, 'or', ms=10, mew=2);
    # plt.scatter([xpos, xpos + width], [ypos, ypos + height])
    # plt.scatter(x_vals, y_vals)

a = fan(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()
