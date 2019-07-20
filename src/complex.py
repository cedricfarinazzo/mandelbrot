class Complex:

    re = 0
    im = 0

    def __init__(self):
        self.re = 0
        self.im = 0

    def __hash__(self):
        return hash((self.re, self.im))

    def __eq__(self, other):
        return self.re == other.re and self.im == other.im

    def __ne__(self, other):
        return not (self == other)

    def conjugate(self):
        c = Complex()
        c.re = self.re
        c.im = -self.im

    def __add__(self, other):
        c = Complex()
        c.re = self.re + other.re
        c.im = self.im + other.im
        return c

    def __sub__(self, other):
        c = Complex()
        c.re = self.re - other.re
        c.im = self.im - other.im
        return c

    def __mul__(self, other):
        c = Complex()
        c.re = (self.re * other.re) - (self.im * other.im)
        c.im = (self.re * other.im) + (self.im * other.re)
        return c

    def __abs__(self):
        c = Complex()
        c.re = self.re if self.re >= 0 else -self.re
        c.im = self.im if self.im >= 0 else -self.im
        return c

    def diverge(self, generation, threshold):
        n = 0
        diverge = False
        z = Complex()
        while n < generation and not diverge:
            zn = (z * z) + self

            delta = abs(zn - z)
            if delta.re >= threshold or delta.im >= threshold:
                diverge = True
            z = zn

            n += 1
        return n
