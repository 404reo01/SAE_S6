import unittest
import math
from voronoi_logic import Point, get_circumcircle, Event, VoronoiSolver

class TestVoronoi(unittest.TestCase):

    def test_circumcircle_basic(self):
        """Teste le calcul du cercle circonscrit pour un triangle rectangle simple."""
        p1 = Point(0, 0)
        p2 = Point(4, 0)
        p3 = Point(0, 3)
        # Le centre d'un triangle rectangle est le milieu de l'hypoténuse : (2, 1.5)
        # Le rayon est 2.5. Le bas du cercle est 1.5 - 2.5 = -1.0
        center, event_y = get_circumcircle(p1, p2, p3)
        
        self.assertAlmostEqual(center.x, 2.0)
        self.assertAlmostEqual(center.y, 1.5)
        self.assertAlmostEqual(event_y, -1.0)

    def test_event_priority(self):
        """Vérifie que la file d'attente traite les Y les plus hauts en premier."""
        e1 = Event(10, 50) # Plus haut
        e2 = Event(10, 100) # Le plus haut
        e3 = Event(10, 20)  # Le plus bas
        
        events = []
        import heapq
        heapq.heappush(events, e1)
        heapq.heappush(events, e2)
        heapq.heappush(events, e3)
        
        first = heapq.heappop(events)
        self.assertEqual(first.y, 100)
        
        second = heapq.heappop(events)
        self.assertEqual(second.y, 50)

    def test_collinear_points(self):
        """Vérifie que des points alignés ne produisent pas de cercle."""
        p1 = Point(0, 0)
        p2 = Point(1, 1)
        p3 = Point(2, 2)
        res = get_circumcircle(p1, p2, p3)
        self.assertIsNone(res)

if __name__ == '__main__':
    unittest.main()