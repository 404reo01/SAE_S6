import math
import unittest
from voronoi import (
    lire_points,
    circumcircle,
    super_triangle,
    bowyer_watson,
    calculer_bbox,
    clipper_segment,
    extraire_voronoi,
    obtenir_cellules,
    ordonner_polygone
)

# ─────────────────────────────────────────────
# 1. TESTS LECTURE FICHIER
# ─────────────────────────────────────────────

class TestLirePoints(unittest.TestCase):

    def test_lecture_normale(self):
        """Vérifie que les points sont bien lus depuis un fichier valide."""
        import tempfile, os
        contenu = "2,4\n5.3,4.5\n18,19\n"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(contenu)
            nom = f.name
        points = lire_points(nom)
        os.unlink(nom)
        self.assertEqual(len(points), 3)
        self.assertEqual(points[0], (2.0, 4.0))
        self.assertEqual(points[1], (5.3, 4.5))

    def test_lignes_vides_ignorees(self):
        """Les lignes vides ne doivent pas générer de points."""
        import tempfile, os
        contenu = "2,4\n\n5,8\n\n"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(contenu)
            nom = f.name
        points = lire_points(nom)
        os.unlink(nom)
        self.assertEqual(len(points), 2)

    def test_coordonnees_negatives(self):
        """Les coordonnées négatives doivent être acceptées."""
        import tempfile, os
        contenu = "-3.5,2\n0,-1\n"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(contenu)
            nom = f.name
        points = lire_points(nom)
        os.unlink(nom)
        self.assertEqual(points[0], (-3.5, 2.0))
        self.assertEqual(points[1], (0.0, -1.0))


# ─────────────────────────────────────────────
# 2. TESTS CERCLE CIRCONSCRIT
# ─────────────────────────────────────────────

class TestCircumcircle(unittest.TestCase):

    def test_triangle_connu(self):
        """Triangle isocèle : circumcentre en (1, 0), rayon = 1."""
        cc = circumcircle((0, 0), (2, 0), (1, 1))
        self.assertIsNotNone(cc)
        self.assertAlmostEqual(cc[0], 1.0, places=5)
        self.assertAlmostEqual(cc[1], 0.0, places=5)
        self.assertAlmostEqual(cc[2], 1.0, places=5)

    def test_triangle_equilateral(self):
        """Le circumcentre d'un triangle équilatéral est son centroïde."""
        h = math.sqrt(3)
        cc = circumcircle((0, 0), (2, 0), (1, h))
        self.assertIsNotNone(cc)
        self.assertAlmostEqual(cc[0], 1.0, places=5)
        self.assertAlmostEqual(cc[1], h / 3, places=5)

    def test_points_colineaires(self):
        """Des points colinéaires doivent retourner None."""
        cc = circumcircle((0, 0), (1, 1), (2, 2))
        self.assertIsNone(cc)

    def test_rayon_positif(self):
        """Le rayon doit toujours être positif."""
        cc = circumcircle((0, 0), (4, 0), (2, 3))
        self.assertIsNotNone(cc)
        self.assertGreater(cc[2], 0)

    def test_point_sur_cercle(self):
        """Les 3 sommets doivent être exactement sur le cercle."""
        p1, p2, p3 = (0, 0), (4, 0), (2, 3)
        cc = circumcircle(p1, p2, p3)
        cx, cy, r = cc
        for p in [p1, p2, p3]:
            dist = math.sqrt((p[0]-cx)**2 + (p[1]-cy)**2)
            self.assertAlmostEqual(dist, r, places=5)


# ─────────────────────────────────────────────
# 3. TESTS SUPER TRIANGLE
# ─────────────────────────────────────────────

class TestSuperTriangle(unittest.TestCase):

    def test_contient_tous_les_points(self):
        """Tous les points doivent être à l'intérieur du super-triangle."""
        points = [(2, 4), (5, 8), (18, 19), (12, 13)]
        st = super_triangle(points)

        def dans_triangle(p, t):
            """Test d'appartenance par signe des produits vectoriels."""
            def signe(a, b, c):
                return (a[0]-c[0])*(b[1]-c[1]) - (b[0]-c[0])*(a[1]-c[1])
            d1 = signe(p, t[0], t[1])
            d2 = signe(p, t[1], t[2])
            d3 = signe(p, t[2], t[0])
            has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
            has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
            return not (has_neg and has_pos)

        for p in points:
            self.assertTrue(dans_triangle(p, st),
                            msg=f"Point {p} pas dans le super-triangle")

    def test_retourne_3_points(self):
        points = [(0, 0), (1, 1), (2, 0)]
        st = super_triangle(points)
        self.assertEqual(len(st), 3)


# ─────────────────────────────────────────────
# 4. TESTS BOWYER-WATSON
# ─────────────────────────────────────────────

class TestBowyerWatson(unittest.TestCase):

    def test_nombre_triangles(self):
        """Pour n points, on attend environ 2n-h-2 triangles."""
        points = [(2, 4), (5, 4), (18, 19), (12, 13), (5, 8), (7, 9)]
        triangles = bowyer_watson(points)
        self.assertGreater(len(triangles), 0)

    def test_chaque_triangle_a_3_sommets(self):
        points = [(0, 0), (5, 0), (2, 4), (4, 3)]
        triangles = bowyer_watson(points)
        for t in triangles:
            self.assertEqual(len(t), 3)

    def test_pas_de_point_dans_circumcircle(self):
        """Propriété de Delaunay : aucun point dans le circumcircle d'un triangle."""
        points = [(2, 4), (5, 4), (18, 19), (12, 13), (5, 8)]
        triangles = bowyer_watson(points)
        for tri in triangles:
            cc = circumcircle(*tri)
            if cc is None:
                continue
            cx, cy, r = cc
            for p in points:
                if p in tri:
                    continue
                dist = math.sqrt((p[0]-cx)**2 + (p[1]-cy)**2)
                self.assertGreaterEqual(dist, r - 1e-9,
                    msg=f"Point {p} dans le circumcircle du triangle {tri}")

    def test_minimum_3_points(self):
        """3 points forment exactement 1 triangle."""
        points = [(0, 0), (4, 0), (2, 3)]
        triangles = bowyer_watson(points)
        self.assertEqual(len(triangles), 1)

    def test_aucun_sommet_du_super_triangle(self):
        """Les sommets du super-triangle ne doivent pas apparaître."""
        points = [(2, 4), (5, 8), (9, 3)]
        st = super_triangle(points)
        triangles = bowyer_watson(points)
        for tri in triangles:
            for sommet in tri:
                self.assertNotIn(sommet, st)


# ─────────────────────────────────────────────
# 5. TESTS BOUNDING BOX ET CLIPPING
# ─────────────────────────────────────────────

class TestBboxEtClipping(unittest.TestCase):

    def test_bbox_avec_marge(self):
        points = [(0, 0), (10, 10)]
        min_x, max_x, min_y, max_y = calculer_bbox(points, marge=5)
        self.assertEqual(min_x, -5)
        self.assertEqual(max_x, 15)
        self.assertEqual(min_y, -5)
        self.assertEqual(max_y, 15)

    def test_segment_entierement_dedans(self):
        bbox = (0, 10, 0, 10)
        seg = clipper_segment((2, 2), (8, 8), bbox)
        self.assertIsNotNone(seg)
        self.assertAlmostEqual(seg[0][0], 2)
        self.assertAlmostEqual(seg[1][0], 8)

    def test_segment_entierement_dehors(self):
        bbox = (0, 10, 0, 10)
        seg = clipper_segment((15, 15), (20, 20), bbox)
        self.assertIsNone(seg)

    def test_segment_coupant_la_bbox(self):
        bbox = (0, 10, 0, 10)
        seg = clipper_segment((5, 5), (15, 5), bbox)
        self.assertIsNotNone(seg)
        self.assertAlmostEqual(seg[1][0], 10)  # clippé à x=10
        self.assertAlmostEqual(seg[1][1], 5)


# ─────────────────────────────────────────────
# 6. TESTS ORDONNER POLYGONE
# ─────────────────────────────────────────────

class TestOrdonnerPolygone(unittest.TestCase):

    def test_ordre_trigonometrique(self):
        """Les sommets doivent être ordonnés dans le sens trigo."""
        sommets = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        ordonnes = ordonner_polygone(sommets)
        angles = [math.atan2(s[1], s[0]) for s in ordonnes]
        self.assertEqual(angles, sorted(angles))

    def test_moins_de_3_sommets(self):
        """Moins de 3 sommets : retourner tel quel sans erreur."""
        sommets = [(0, 0), (1, 1)]
        result = ordonner_polygone(sommets)
        self.assertEqual(len(result), 2)


# ─────────────────────────────────────────────
# LANCEMENT
# ─────────────────────────────────────────────

if __name__ == '__main__':
    unittest.main(verbosity=2)