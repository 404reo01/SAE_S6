import unittest
import tempfile
import os
from model import VoronoiModel
from point_loader import PointLoader, PointLoadError
from exporters import SVGExporter, ImageExporter

class TestVoronoiModel(unittest.TestCase):
    def setUp(self):
        self.model = VoronoiModel()
        self.points = [(2,4), (5.3,4.5), (18,29), (12.5,23.7)]
        self.model.set_points(self.points)

    def test_set_points(self):
        self.assertEqual(len(self.model.get_points()), 4)
        self.assertTrue(self.model.has_valid_diagram())

    def test_polygons(self):
        polygons = self.model.get_polygons()
        self.assertEqual(len(polygons), 4)

    def test_invalid_points(self):
        # Tester avec un seul point : le diagramme ne doit pas être valide
        self.model.set_points([(1,2)])
        self.assertFalse(self.model.has_valid_diagram())
        self.assertEqual(len(self.model.get_points()), 1)

class TestPointLoader(unittest.TestCase):
    def test_load_valid(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("2,4\n5.3,4.5\n18,29\n12.5,23.7")
            tmpname = f.name
        points = PointLoader.load(tmpname)
        self.assertEqual(points, [(2.0,4.0), (5.3,4.5), (18.0,29.0), (12.5,23.7)])
        os.unlink(tmpname)

    def test_load_invalid(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("2,4\nabc,def")
            tmpname = f.name
        with self.assertRaises(PointLoadError):
            PointLoader.load(tmpname)
        os.unlink(tmpname)

class TestExporters(unittest.TestCase):
    def setUp(self):
        self.model = VoronoiModel()
        self.model.set_points([(0,0), (1,1), (2,0)])

    def test_svg_export(self):
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tmp:
            tmp.close()
            exporter = SVGExporter()
            exporter.export(self.model, tmp.name)
            self.assertTrue(os.path.exists(tmp.name))
            os.unlink(tmp.name)

    def test_image_export(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp.close()
            exporter = ImageExporter()
            exporter.export(self.model, tmp.name)
            self.assertTrue(os.path.exists(tmp.name))
            os.unlink(tmp.name)

if __name__ == "__main__":
    unittest.main()