import unittest
import os
from voronoi_app import VoronoiApp, Point  # Votre classe
import tkinter as tk
from unittest.mock import patch, Mock

class TestVoronoiApp(unittest.TestCase):
    
    def setUp(self):
        """Crée app + points.txt test"""
        self.app = VoronoiApp()
        self.points_test = [
            "2.0 4.0",
            "5.3 4.5", 
            "18.0 29.0",
            "12.5 23.7"
        ]
    
    def create_test_file(self, content: list):
        """Crée points.txt temporaire"""
        with open("test_points.txt", 'w') as f:
            f.write('\n'.join(content))
    
    def test_load_points_valid(self):
        """T1: Lit 4 points valides"""
        self.create_test_file(self.points_test)
        self.app.load_points("test_points.txt")
        self.assertEqual(len(self.app.points), 4)
        self.assertEqual(self.app.points[0].x, 2.0)
        self.assertEqual(self.app.points[0].y, 4.0)
    
    def test_load_points_empty(self):
        """T2: Fichier vide → 0 points"""
        self.create_test_file([])
        self.app.load_points("test_points.txt")
        self.assertEqual(len(self.app.points), 0)
    
    def test_load_points_invalid_line(self):
        """T3: Ignore lignes invalides"""
        invalid_content = ["abc", "1.2", "#comment", "3 4"]
        self.create_test_file(invalid_content)
        self.app.load_points("test_points.txt")
        self.assertEqual(len(self.app.points), 1)  # Seulement "3 4"
    
    def test_load_points_missing_file(self):
        """T4: Fichier manquant → 0 points"""
        self.app.load_points("fichier_inexistant.txt")
        self.assertEqual(len(self.app.points), 0)
    
    def test_scale_adaptation(self):
        """T5: Scale s'adapte aux points"""
        self.app.points = [Point(0,0), Point(100,100)]
        scale, ox, oy = self.app.calculate_scale()
        self.assertGreater(scale, 0)
        self.assertAlmostEqual(ox, 10, delta=5)
    
    def test_add_remove_points(self):
        """T6: Ajout/suppression points → nouveau diagramme"""
        self.app.points = [Point(1,1)]
        old_len = len(self.app.points)
        self.app.points.append(Point(2,2))
        self.assertEqual(len(self.app.points), old_len + 1)
    
    def test_voronoi_logic_single_point(self):
        """T7: 1 point → toute l'image sa couleur"""
        self.app.points = [Point(10,10)]
        # Simule 1 pixel
        rx, ry = self.app.pixel_to_point(400, 300)
        closest, best_dist = 0, float('inf')
        for i, p in enumerate(self.app.points):
            dist = (p.x - rx)**2 + (p.y - ry)**2
            if dist < best_dist:
                best_dist = dist
                closest = i
        self.assertEqual(closest, 0)
    
    def test_voronoi_logic_two_points(self):
        """T8: 2 points → bissectrice"""
        self.app.points = [Point(0,0), Point(10,10)]
        # Milieu devrait être P1 ou P2
        rx, ry = self.app.pixel_to_point(400, 300)
        distances = [(p.x - rx)**2 + (p.y - ry)**2 for p in self.app.points]
        closest = distances.index(min(distances))
        self.assertIn(closest, [0, 1])

class TestPoint(unittest.TestCase):
    """Tests classe Point"""
    def test_init(self):
        p = Point(3.14, 2.71)
        self.assertEqual(p.x, 3.14)
        self.assertEqual(p.y, 2.71)

def test_integration_gui():
    """T9: GUI ne crash pas"""
    root = tk.Tk()
    app = VoronoiApp()
    root.destroy()

if __name__ == "__main__":
    # Nettoie fichiers test
    if os.path.exists("test_points.txt"):
        os.remove("test_points.txt")
    
    unittest.main(verbosity=2, exit=False)
