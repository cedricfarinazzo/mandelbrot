from PIL import Image
import complex
import sys, threading, multiprocessing


def get_color(generation, n):
    return int((n * 255) / generation) % 255


class Mandelbrot:

    A = (0, 0)
    B = (0, 0)
    w = 0
    h = 0
    precision = 0
    coeff = 0
    nbpixel = 0

    def __init__(self, A, B, precision):
        if precision is 0:
            raise ZeroDivisionError()
        self.A = A
        self.B = B
        self.w = B[0] - A[0]
        self.h = B[1] - A[1]
        self.precision = precision
        self.image = None
        self.coeff = 1 / self.precision
        self.nbpixel = self.w * self.h * self.coeff * self.coeff

    def generate(self, generation, threshold, zoom=1):
        print("Generation ...")

        dimW = int(self.w * self.coeff)
        dimW *= zoom

        dimH = int(self.h * self.coeff)
        dimH *= zoom

        self.image = Image.new('RGB', (dimW, dimH))

        i = self.A[0]
        count = 0
        while i < self.B[0]:
            j = self.A[1]
            while j < self.B[1]:
                c = complex.Complex()
                c.re = i
                c.im = j

                n = c.diverge(generation, threshold)
                color = get_color(generation, n)

                x = int((i - self.A[0]) * self.coeff * zoom)
                y = int((j - self.A[1]) * self.coeff * zoom)

                try:
                    self.image.putpixel((x, y), (color, color, color))
                except:
                    pass

                j += self.precision
                count += 1
            print(str(int(count / self.nbpixel * 100)) + "%")
            i += self.precision
        print("100%")

    def display(self):
        if self.image is None:
            return
        self.image.save("mandelbrot.png", quality=100)
        self.image.show()
        print("Done")


class MandelbrotMultiThread(Mandelbrot):
    globalcount = 0

    def __init__(self, A, B, precision):
        Mandelbrot.__init__(self, A, B, precision)
        self.globalcount = 0

    def compute(self, A, B, generation, threshold, IdThread, zoom=1):

        i = A[0]
        while i < B[0]:
            j = A[1]
            while j < B[1]:
                c = complex.Complex()
                c.re = i
                c.im = j

                n = c.diverge(generation, threshold)
                color = get_color(generation, n)

                x = int((i - self.A[0]) * self.coeff * zoom)
                y = int((j - self.A[1]) * self.coeff * zoom)

                try:
                    self.image.putpixel((x, y), (color, (IdThread * color) % 255, color))
                    self.image.putpixel((x, y), (color, color, color))
                except:
                    pass

                self.globalcount += 1
                j += self.precision
            print(str(int(self.globalcount / self.nbpixel * 100)) + "%  |   " + str(self.globalcount) + " / " + str(self.nbpixel))
            i += self.precision
        print("Thread N°" + str(IdThread) + " done !")

    def generate(self, generation, threshold, zoom=1):
        self.globalcount = 0

        dimW = int(self.w * self.coeff)
        dimW *= zoom

        dimH = int(self.h * self.coeff)
        dimH *= zoom

        self.nbpixel = dimW * dimH
        self.image = Image.new('RGB', (dimW, dimH))

        nbcpu = multiprocessing.cpu_count()
        wPerThread = (self.w) / nbcpu
        threads = []
        start = self.A[0]
        id = 1
        while start < self.B[0]:
            args = ((start, self.A[1]), (round(start + wPerThread, 6), self.B[1]), generation, threshold, id, zoom)
            print(args)
            th = threading.Thread(target=self.compute, args=args)
            threads.append(th)
            start += wPerThread
            start = round(start, 6)
            id += 1

        for th in threads:
            th.start()


        #COMPUTE RESTE
        #self.compute((start - wPerThread, self.A[1]), (start, self.B[1]), generation, threshold, id, zoom)
        #print(((start - wPerThread, self.A[1]), (start, self.B[1]), generation, threshold, id, zoom))

        for th in threads:
            th.join()

        print("Done")

    def display(self):
        Mandelbrot.display(self)
