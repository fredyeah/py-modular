import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as fan

plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

i = 0
def animate(t):
    global i
    x_vals.append(i)
    y_vals.append(random.randint(0, 5))
    i = (i + 1) % 100
    plt.cla()
    plt.scatter(x_vals, y_vals)

a = fan(plt.gcf(), animate, interval=100)

plt.tight_layout()
plt.show()


# data = pd.read_csv('data.csv')
# x = data['x_value']
# y1 = data['total_1']
# y2 = data['total_2']
