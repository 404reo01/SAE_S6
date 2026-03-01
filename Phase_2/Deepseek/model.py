import numpy as np
from scipy.spatial import Voronoi

class VoronoiModel:
    def __init__(self):
        self.points = []
        self.voronoi = None

    def set_points(self, points):
        self.points = np.array(points)
        if len(self.points) >= 2:
            self.voronoi = Voronoi(self.points)
        else:
            self.voronoi = None

    def get_points(self):
        return self.points.tolist() if len(self.points) > 0 else []

    def get_polygons(self):
        if self.voronoi is None:
            return []
        polygons = []
        for point_index, region_index in enumerate(self.voronoi.point_region):
            region = self.voronoi.regions[region_index]
            if not region or -1 in region:
                polygons.append(None)
            else:
                polygon = self.voronoi.vertices[region]
                polygons.append(polygon.tolist())
        return polygons

    def get_vertices(self):
        return self.voronoi.vertices.tolist() if self.voronoi is not None else []

    def has_valid_diagram(self):
        return self.voronoi is not None