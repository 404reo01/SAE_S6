from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from plotter import plot_diagram

class Exporter(ABC):
    @abstractmethod
    def export(self, model, filename):
        pass

class SVGExporter(Exporter):
    def export(self, model, filename):
        fig, ax = plt.subplots()
        plot_diagram(ax, model)
        plt.savefig(filename, format='svg')
        plt.close(fig)

class ImageExporter(Exporter):
    def __init__(self, dpi=100):
        self.dpi = dpi

    def export(self, model, filename):
        fig, ax = plt.subplots()
        plot_diagram(ax, model)
        plt.savefig(filename, dpi=self.dpi)
        plt.close(fig)