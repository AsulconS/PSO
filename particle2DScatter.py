from mpl_toolkits import mplot3d
from random import random, seed
from datetime import datetime
from matplotlib.animation import FuncAnimation

import numpy as np
import matplotlib.pyplot as plt

class Particle2DScatter(object):
    def __init__(self, figNum = 1, n = 100, vw = 1, wMin = 0.4, wMax = 0.9, c1 = 0.75, c2 = 0.75, it = 500, crit = 'min'):
        self.n = n                      # n  = number of particles
        self.w = wMax                   # w  = inertia constant
        self.c1 = c1                    # c1 = cognitive constant
        self.c2 = c2                    # c2 = social constant
        self.it = it                    # it = number of iterations
        self.vw = vw                    # vw = velocity vector weight (step)
        self.nRange = range(self.n)
        self.wls = np.linspace(wMin, wMax, it)

        self.crit = crit

        self.fig = plt.figure(num = figNum)
        self.ax  = plt.axes()
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_title('Particle Swarm Optimization')
        self.genContours()

        self.ani = FuncAnimation(self.fig, self.update, frames = self.it + 1, init_func = self.setup, blit = False, interval = 1)

    def setup(self):
        seed(0)
        self.xp = np.asarray([-3 + 6 * random() for i in self.nRange])
        self.yp = np.asarray([-3 + 6 * random() for i in self.nRange])

        self.X = np.asarray([[self.xp[i], self.yp[i], self.f(self.xp[i], self.yp[i])] for i in self.nRange])
        self.V = np.asarray([[random(), random()] for i in self.nRange])

        self.P = np.copy(self.X)
        self.initFirstGlobalBest()

        self.sc = self.ax.scatter(self.xp, self.yp, marker = '<', color = 'black', s = 8, alpha = 1)
        return self.sc

    def update(self, i):
        if self.cit > 0:
            print('w =', self.w)
            self.step()
            self.sc.set_offsets(np.c_[self.xp, self.yp])
        else:
            print('Global Minimum reached! G = ', self.G[2], ' at [', self.G[0], ', ', self.G[1], ']', sep = '')
            self.end()
        return self.sc

    def step(self):
        seed(datetime.now())
        for i in self.nRange:
            r1 = self.getRandom()
            r2 = self.getRandom()
            self.V[i][0] = self.w * self.V[i][0] + self.c1 * r1 * (self.P[i][0] - self.X[i][0]) + self.c2 * r2 * (self.G[0] - self.X[i][0])
            self.V[i][1] = self.w * self.V[i][1] + self.c1 * r1 * (self.P[i][1] - self.X[i][1]) + self.c2 * r2 * (self.G[1] - self.X[i][1])
            self.X[i][0] = self.X[i][0] + self.V[i][0] * self.vw
            self.X[i][1] = self.X[i][1] + self.V[i][1] * self.vw
            self.X[i][2] = self.f(self.X[i][0], self.X[i][1])
            self.xp[i] = self.X[i][0]
            self.yp[i] = self.X[i][1]

            if self.criteria(self.X[i][2], self.P[i][2]):
                self.P[i] = self.X[i].copy()
                if self.criteria(self.X[i][2], self.G[2]):
                    self.G = self.X[i].copy()

        self.cit = self.cit - 1
        self.cw = self.cw - 1
        self.w = self.wls[self.cw]

    def end(self):
        if self.mode == 'show':
            plt.close(fig = self.fig)

    def initFirstGlobalBest(self):
        self.G = self.X[0].copy()
        for i in self.nRange:
            if self.criteria(self.X[i][2], self.G[2]):
                self.G = self.X[i].copy()

    def f(self, x, y):
        return  3 * (1 - x)**2 * np.exp(-x**2 - (y + 1)**2) -\
                10 * (x / 5 - x**3 - y**5) * np.exp(-x**2 - y**2) -\
                (1 / 3) * np.exp(-(x + 1)**2 - y**2)

    def criteria(self, a, b):
        if self.crit == 'min':
            return a < b
        elif self.crit == 'max':
            return a > b
        elif self.crit == 'c4':
            return abs(4 - a) < abs(4 - b)
        elif self.crit == 'c-4':
            return abs(-4 - a) < abs(-4 - b)
        else:
            return False

    def genContours(self):
        xls = np.linspace(-3, 3, 48)
        yls = np.linspace(-3, 3, 48)

        self.SX, self.SY = np.meshgrid(xls, yls)
        self.SZ = self.f(self.SX, self.SY)

        self.cset = self.ax.imshow(self.SZ, extent = [-3, 3, -3, 3], interpolation = 'bilinear', origin = 'lower', cmap = 'jet')

        self.fig.colorbar(self.cset, ax = self.ax)

    def getRandom(self, a = 0, b = 1):
        return a + (b - a) * random()

    def save(self, writer, filename):
        self.mode = 'save'
        print('Exporting . . . Please, wait')

        self.cit = self.it
        self.cw = self.it - 1
        self.w = self.wls[self.cw]
        self.ani.save(filename, writer = writer.getWriter())

    def show(self):
        self.mode = 'show'

        self.cit = self.it
        self.cw = self.it - 1
        self.w = self.wls[self.cw]
        plt.show()
