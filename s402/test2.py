import numpy
from matplotlib import pyplot

figure, axis = pyplot.subplots(1, 1, figsize=(20, 20))

x = numpy.linspace(-10, 10, 100)
y = numpy.sin(x)

axis.plot(x, y)

pyplot.title("Grafica del seno")

pyplot.savefig("g1.png")

pyplot.show()