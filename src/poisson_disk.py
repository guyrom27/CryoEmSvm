import scipy
from random import random

#reference: http://connor-johnson.com/2015/04/08/poisson-disk-sampling/
#article: http://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph07-poissondisk.pdf
class pds:

    def __init__(self, w, h, d, r, n, k=30):
        """

        :param w: x dim size
        :param h: y dim size
        :param d: z dim size
        :param r: minimal separation
        :param n: amount of points
        :param k: amount of points to try around each initial point (default 30)
        """
        # w and h are the width and height of the field
        self.w = w
        self.h = h
        self.d = d

        # n is the number of test points
        self.n = n
        #k is the number of attempts is a single sphere
        self.k = k
        self.r2 = r ** 2.0
        self.A = 3.0 * self.r2
        # cs is the cell size
        self.cs = r / scipy.sqrt(3)
        # gw and gh are the number of grid cells
        self.gw = int(scipy.ceil(self.w / self.cs))
        self.gh = int(scipy.ceil(self.h / self.cs))
        self.gd = int(scipy.ceil(self.h / self.cs))

        self.bin_shape = [1, self.gw, self.gw * self.gh]

        # create a grid and a queue
        self.grid = [None] * self.gd * self.gw * self.gh
        self.queue = list()
        # set the queue size and sample size to zero
        self.qs, self.ss = 0, 0

    def distance(self, x, y, z):
        # find where (x,y,z) sits in the grid
        [x_idx, y_idx, z_idx] = self.find_bin([x,y,z])
        # determine a neighborhood of cells around (x,y,z)
        x0 = max(x_idx - 2, 0)
        y0 = max(y_idx - 2, 0)
        z0 = max(z_idx - 2, 0)
        x1 = max(x_idx - 3, self.gw)
        y1 = max(y_idx - 3, self.gh)
        z1 = max(z_idx - 3, self.gd)
        # search around (x,y,z)
        for z_idx in range(z0, z1):
            for y_idx in range(y0, y1):
                for x_idx in range(x0, x1):
                    step = self.to_3d([x_idx,y_idx,z_idx])
                    # if the sample point exists on the grid
                    if self.grid[step]:
                        s = self.grid[step]
                        dx = (s[0] - x) ** 2.0
                        dy = (s[1] - y) ** 2.0
                        dz = (s[2] - z) ** 2.0
                        # and it is too close
                        if dx + dy + dz < self.r2:
                            # then barf
                            return False
        return True

    def find_bin(self, s):
        return [int(x / self.cs) for x in s]

    def to_3d(self, s):
        return sum([x[0]*x[1] for x in zip(s,self.bin_shape)])


    def set_point(self, x, y, z):
        s = [x, y, z]
        self.queue.append(s)
        self.qs += 1

        # find where (x,y) sits in the grid

        step = self.to_3d(self.find_bin(s))

        if (self.grid[step] != None):
            print("hello")
            assert(False)
        self.grid[step] = s
        self.ss += 1

        return s

    def create_point_grid(self):
        while self.ss < self.n:
            if (self.qs == 0):
                print("randomization failed")
                exit(1)
            idx_in_q = int(random() * self.qs)
            s = self.queue[idx_in_q]
            for i in range(self.k):

                phi = 2 * scipy.pi * random()
                theta = scipy.pi * random()
                r = scipy.sqrt(self.A * random() + self.r2)

                x = int(s[0] + r * scipy.sin(theta) * scipy.cos(phi))
                y = int(s[1] + r * scipy.sin(theta) * scipy.sin(phi))
                z = int(s[2] + r * scipy.cos(theta))

                if (x >= 0) and (x < self.w):
                    if (y >= 0) and (y < self.h):
                        if (z >= 0) and (z < self.d):
                            if (self.distance(x, y, z)):
                                self.set_point(x, y, z)
                                if (self.ss >= self.n):
                                    break
            del self.queue[idx_in_q]
            self.qs -= 1


    def randomize_spaced_points(self):
        if self.ss == 0:
            [x,y,z] = [random() * i for i in [self.w, self.h, self.d]]
            self.set_point(x, y, z)
        self.create_point_grid()
        sample = list(filter(None, self.grid))
        return sample

if __name__ == '__main__':
    r = 2
    n = 40
    for i in range(100):
        obj = pds(10, 20, 10, r, n)
        sample1 = obj.randomize_spaced_points()
        for i in enumerate(sample1):
            for j in range(i[0]+1, len(sample1)):
                if sum([(x[1]-x[0])**2 for x in zip(i[1],sample1[j])]) < r:
                    assert(False)
        assert(len(sample1) == n)
