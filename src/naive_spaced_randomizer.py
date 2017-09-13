import random

class naive_spaced_randomizer:
    """
    generates random points that are separated from one another in a given distance using a naive elimination
    """
    def __init__(self, w, h, d, r, n, max_tries=100000):
        """
        naive randomization- randomize and check if it is separated from all other points
        :param w: x dim size
        :param h: y dim size
        :param d: z dim size, use 1 for 2D
        :param r: minimal separation
        :param n: num of points to randomize
        :param max_tries: give up after
        """
        self.w=w
        self.h=h
        self.d=d
        self.r2=r**2
        self.n=n
        self.max_tries = max_tries

    def randomize_spaced_points(self):
        points = []
        for i in range(self.n):
            for j in range(self.max_tries):
                x = random.randint(0,self.w-1)
                y = random.randint(0, self.h-1)
                z = random.randint(0,self.d-1)
                point = (x,y,z)
                valid = True
                for p in points:
                    if (sum([(x[0]-x[1])**2 for x in zip(point,p)]) < self.r2):
                        valid = False
                        break
                if valid:
                    points.append(point)
                    break
                if j==self.max_tries-1:
                    raise Exception("Randomization hit max tries and failed")
        return points


