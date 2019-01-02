import mandelbrot

"""

# Single Thread

A = (-1.25, -0.75)
B = (-0.4, 0.75)
precision = 0.0005

m = mandelbrot.Mandelbrot(A, B, precision)
m.generate(100, 4)

print("Drawing")
m.display()
"""


# Multi Thread

A = (-2.1, -1.5)
B = (1.3, 1.6)
precision = 0.000750

m = mandelbrot.MandelbrotMultiThread(A, B, precision)

m.generate(100, 4)

print("Drawing")
m.display()


"""
# OpenCL

A = (-2.1, -1.5)
B = (1.3, 1.6)
precision = 0.000750

m = mandelbrot.MandelbrotOpenCV(A, B, precision)

m.generate(100, 4)

print("Drawing")
m.display()
"""
