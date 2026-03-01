def lire_points(fichier):
    points = []
    with open(fichier, 'r') as f:
        for ligne in f:
            ligne = ligne.strip()
            if ligne and ',' in ligne:  # double vérification
                parties = ligne.split(',')
                try:
                    x, y = float(parties[0].strip()), float(parties[1].strip())
                    points.append((x, y))
                except ValueError:
                    print(f"Ligne ignorée : {repr(ligne)}")
    return points

# Vérifions combien de points sont lus
points = lire_points('Claude/points.txt')
print(f"Nombre de points lus : {len(points)}")
for p in points:
    print(p)

def circumcircle(p1, p2, p3):
    ax, ay = p1
    bx, by = p2
    cx, cy = p3

    # Calcul du déterminant (si D ≈ 0, les points sont colinéaires)
    D = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))

    if abs(D) < 1e-10:
        return None  # points colinéaires, pas de cercle circonscrit

    ux = ((ax**2 + ay**2) * (by - cy) +
          (bx**2 + by**2) * (cy - ay) +
          (cx**2 + cy**2) * (ay - by)) / D

    uy = ((ax**2 + ay**2) * (cx - bx) +
          (bx**2 + by**2) * (ax - cx) +
          (cx**2 + cy**2) * (bx - ax)) / D

    rayon = ((ax - ux)**2 + (ay - uy)**2) ** 0.5

    return (ux, uy, rayon)

p1 = (0.0, 0.0)
p2 = (2.0, 0.0)
p3 = (1.0, 1.0)

result = circumcircle(p1, p2, p3)
print(f"Centre : ({result[0]:.4f}, {result[1]:.4f})")
print(f"Rayon  : {result[2]:.4f}")

def super_triangle(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    dx = max_x - min_x
    dy = max_y - min_y
    delta = max(dx, dy) * 100  # suffisamment grand
    
    p1 = (min_x - delta,     min_y - delta)
    p2 = (min_x + 2 * delta, min_y - delta)
    p3 = (min_x - delta,     min_y + 2 * delta)
    
    return p1, p2, p3

def bowyer_watson(points):
    # 1. Initialisation avec le super-triangle
    st1, st2, st3 = super_triangle(points)
    triangles = [(st1, st2, st3)]

    # 2. Insertion point par point
    for point in points:
        triangles_invalides = []
        
        # Trouver les triangles dont le cercle circonscrit contient le point
        for triangle in triangles:
            cc = circumcircle(*triangle)
            if cc is None:
                continue
            cx, cy, r = cc
            # Distance entre le point et le centre du cercle
            dist = ((point[0] - cx)**2 + (point[1] - cy)**2) ** 0.5
            if dist < r - 1e-10:  # le point est DANS le cercle
                triangles_invalides.append(triangle)

        # Trouver les arêtes extérieures du polygone étoilé
        aretes = []
        for triangle in triangles_invalides:
            p1, p2, p3 = triangle
            aretes.append((p1, p2))
            aretes.append((p2, p3))
            aretes.append((p3, p1))
        
        # Une arête est extérieure si elle n'apparaît qu'une seule fois
        # (arêtes partagées entre 2 triangles invalides sont éliminées)
        aretes_exterieures = []
        for i, arete in enumerate(aretes):
            a, b = arete
            est_dupliquee = False
            for j, autre in enumerate(aretes):
                if i == j:
                    continue
                # Vérifier si c'est la même arête (dans les deux sens)
                if (a == autre[0] and b == autre[1]) or \
                   (a == autre[1] and b == autre[0]):
                    est_dupliquee = True
                    break
            if not est_dupliquee:
                aretes_exterieures.append(arete)

        # Supprimer les triangles invalides
        for t in triangles_invalides:
            triangles.remove(t)

        # Créer de nouveaux triangles en reliant le point aux arêtes extérieures
        for arete in aretes_exterieures:
            nouveau_triangle = (arete[0], arete[1], point)
            triangles.append(nouveau_triangle)

    # 3. Supprimer les triangles liés au super-triangle
    st_points = {st1, st2, st3}
    triangles = [t for t in triangles
                 if not any(p in st_points for p in t)]

    return triangles

points = lire_points('Claude/points.txt')
triangles = bowyer_watson(points)

print(f"Nombre de triangles : {len(triangles)}")
for i, t in enumerate(triangles):
    print(f"Triangle {i+1} : {t[0]} | {t[1]} | {t[2]}")

def extraire_aretes_voronoi(triangles):
    circumcentres = {}
    
    # Calculer le circumcentre de chaque triangle
    for triangle in triangles:
        cc = circumcircle(*triangle)
        if cc is not None:
            circumcentres[triangle] = (cc[0], cc[1])
    
    aretes_voronoi = []
    
    # Parcourir toutes les paires de triangles
    for i, t1 in enumerate(triangles):
        for j, t2 in enumerate(triangles):
            if j <= i:
                continue  # éviter les doublons
            
            # Compter les sommets en commun
            sommets_communs = [p for p in t1 if p in t2]
            
            if len(sommets_communs) == 2:  # ils partagent une arête
                if t1 in circumcentres and t2 in circumcentres:
                    aretes_voronoi.append((circumcentres[t1], circumcentres[t2]))
    
    return aretes_voronoi, circumcentres

aretes_voronoi, circumcentres = extraire_aretes_voronoi(triangles)

print(f"Nombre de sommets de Voronoï : {len(circumcentres)}")
print(f"Nombre d'arêtes de Voronoï  : {len(aretes_voronoi)}")
print("\nSommets de Voronoï :")
for t, cc in circumcentres.items():
    print(f"  ({cc[0]:.2f}, {cc[1]:.2f})")
print("\nArêtes de Voronoï :")
for a in aretes_voronoi:
    print(f"  ({a[0][0]:.2f}, {a[0][1]:.2f}) → ({a[1][0]:.2f}, {a[1][1]:.2f})")

def calculer_bounding_box(points, marge=3):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return (min(xs) - marge, max(xs) + marge,
            min(ys) - marge, max(ys) + marge)

def clipper_segment(p1, p2, bbox):
    """Clippe un segment à la bounding box avec l'algorithme de Cohen-Sutherland."""
    min_x, max_x, min_y, max_y = bbox

    def code(p):
        c = 0
        if p[0] < min_x: c |= 1
        if p[0] > max_x: c |= 2
        if p[1] < min_y: c |= 4
        if p[1] > max_y: c |= 8
        return c

    x1, y1 = p1
    x2, y2 = p2
    c1, c2 = code(p1), code(p2)

    while True:
        if not (c1 | c2):       # les deux dedans
            return (x1, y1), (x2, y2)
        elif c1 & c2:           # les deux du même côté dehors
            return None
        else:
            c = c1 if c1 else c2
            if c & 8:
                x = x1 + (x2 - x1) * (max_y - y1) / (y2 - y1)
                y = max_y
            elif c & 4:
                x = x1 + (x2 - x1) * (min_y - y1) / (y2 - y1)
                y = min_y
            elif c & 2:
                y = y1 + (y2 - y1) * (max_x - x1) / (x2 - x1)
                x = max_x
            else:
                y = y1 + (y2 - y1) * (min_x - x1) / (x2 - x1)
                x = min_x
            if c == c1:
                x1, y1, c1 = x, y, code((x, y))
            else:
                x2, y2, c2 = x, y, code((x, y))

def extraire_aretes_voronoi_complet(points, triangles):
    circumcentres = {}
    for triangle in triangles:
        cc = circumcircle(*triangle)
        if cc is not None:
            circumcentres[triangle] = (cc[0], cc[1])

    bbox = calculer_bounding_box(points, marge=5)
    aretes_voronoi = []

    # --- Arêtes intérieures (entre deux triangles adjacents) ---
    for i, t1 in enumerate(triangles):
        for j, t2 in enumerate(triangles):
            if j <= i:
                continue
            sommets_communs = [p for p in t1 if p in t2]
            if len(sommets_communs) == 2:
                if t1 in circumcentres and t2 in circumcentres:
                    seg = clipper_segment(circumcentres[t1],
                                         circumcentres[t2], bbox)
                    if seg:
                        aretes_voronoi.append(seg)

    # --- Arêtes semi-infinies (triangles sur l'enveloppe convexe) ---
    # Trouver les arêtes qui n'appartiennent qu'à un seul triangle
    toutes_aretes = []
    for triangle in triangles:
        p1, p2, p3 = triangle
        toutes_aretes.append((p1, p2, triangle))
        toutes_aretes.append((p2, p3, triangle))
        toutes_aretes.append((p3, p1, triangle))

    for i, (a, b, tri) in enumerate(toutes_aretes):
        est_frontiere = True
        for j, (c, d, _) in enumerate(toutes_aretes):
            if i == j:
                continue
            if (a == c and b == d) or (a == d and b == c):
                est_frontiere = False
                break

        if est_frontiere and tri in circumcentres:
            cx, cy = circumcentres[tri]
            
            min_x, max_x, min_y, max_y = bbox
            
            # Si le circumcentre est déjà hors de la bbox, pas besoin d'arête semi-infinie
            if not (min_x <= cx <= max_x and min_y <= cy <= max_y):
                continue

            # Vecteur de l'arête
            dx = b[0] - a[0]
            dy = b[1] - a[1]
            longueur = (dx**2 + dy**2) ** 0.5
            perp_x, perp_y = -dy / longueur, dx / longueur

            # Troisième sommet du triangle
            troisieme = [p for p in tri if p != a and p != b][0]

            # Vecteur du circumcentre vers le troisième sommet
            vers_t_x = troisieme[0] - cx
            vers_t_y = troisieme[1] - cy

            # Pointer à l'opposé du troisième sommet
            if (perp_x * vers_t_x + perp_y * vers_t_y) > 0:
                perp_x, perp_y = -perp_x, -perp_y

            facteur = 1000
            p_loin = (cx + perp_x * facteur, cy + perp_y * facteur)
            seg = clipper_segment((cx, cy), p_loin, bbox)
            if seg:
                aretes_voronoi.append(seg)

            return aretes_voronoi, circumcentres

points = lire_points('Claude/points.txt')
triangles = bowyer_watson(points)

aretes_voronoi, circumcentres = extraire_aretes_voronoi_complet(points, triangles)

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def visualiser_voronoi(points, triangles, aretes_voronoi, circumcentres):
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))

    # --- Triangulation de Delaunay (en gris clair) ---
    for triangle in triangles:
        p1, p2, p3 = triangle
        xs = [p1[0], p2[0], p3[0], p1[0]]
        ys = [p1[1], p2[1], p3[1], p1[1]]
        ax.plot(xs, ys, 'b-', linewidth=0.8, alpha=0.3)

    # --- Arêtes de Voronoï (en rouge) ---
    for arete in aretes_voronoi:
        x1, y1 = arete[0]
        x2, y2 = arete[1]
        ax.plot([x1, x2], [y1, y2], 'r-', linewidth=1.5)

    # --- Sommets de Voronoï (petits carrés verts) ---
    for cc in circumcentres.values():
        ax.plot(cc[0], cc[1], 'gs', markersize=4)

    # --- Points originaux (grands points noirs) ---
    for p in points:
        ax.plot(p[0], p[1], 'ko', markersize=7)
        ax.annotate(f"({p[0]}, {p[1]})", xy=p,
                    xytext=(5, 5), textcoords='offset points', fontsize=7)

    # --- Mise en forme ---
    ax.set_title("Diagramme de Voronoï (via triangulation de Delaunay)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')

    # Limiter la vue pour éviter que le sommet éloigné écrase tout
    xs_pts = [p[0] for p in points]
    ys_pts = [p[1] for p in points]
    marge = 3
    ax.set_xlim(min(xs_pts) - marge, max(xs_pts) + marge)
    ax.set_ylim(min(ys_pts) - marge, max(ys_pts) + marge)

    plt.tight_layout()
    plt.show()

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.colors as mcolors

def obtenir_cellules_voronoi(points, triangles, circumcentres):
    """Pour chaque point, trouver les circumcentres des triangles qui le contiennent."""
    cellules = {p: [] for p in points}
    for triangle, cc in circumcentres.items():
        for p in triangle:
            if p in cellules:
                cellules[p].append(cc)
    return cellules

def ordonner_polygone(sommets):
    """Ordonner les sommets d'un polygone dans le sens trigonométrique."""
    if len(sommets) < 3:
        return sommets
    cx = sum(s[0] for s in sommets) / len(sommets)
    cy = sum(s[1] for s in sommets) / len(sommets)
    import math
    return sorted(sommets, key=lambda s: math.atan2(s[1] - cy, s[0] - cx))

def visualiser_voronoi_complet(points, triangles, aretes_voronoi, circumcentres):
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))

    # Limites de la vue
    xs_pts = [p[0] for p in points]
    ys_pts = [p[1] for p in points]
    marge = 3
    x_min = min(xs_pts) - marge
    x_max = max(xs_pts) + marge
    y_min = min(ys_pts) - marge
    y_max = max(ys_pts) + marge

    # Palette de couleurs pour les cellules
    couleurs = list(mcolors.TABLEAU_COLORS.values())

    # --- Colorier les cellules de Voronoï ---
    cellules = obtenir_cellules_voronoi(points, triangles, circumcentres)
    for idx, (point, sommets_cc) in enumerate(cellules.items()):
        if len(sommets_cc) >= 3:
            sommets_ordonnes = ordonner_polygone(sommets_cc)
            polygone = Polygon(sommets_ordonnes, closed=True)
            couleur = couleurs[idx % len(couleurs)]
            patch = mpatches.Polygon(sommets_ordonnes, closed=True,
                                     facecolor=couleur, alpha=0.25,
                                     edgecolor='none')
            ax.add_patch(patch)

    # --- Triangulation de Delaunay (optionnelle, très transparente) ---
    for triangle in triangles:
        p1, p2, p3 = triangle
        xs = [p1[0], p2[0], p3[0], p1[0]]
        ys = [p1[1], p2[1], p3[1], p1[1]]
        ax.plot(xs, ys, 'b-', linewidth=0.5, alpha=0.15)

    # --- Arêtes de Voronoï ---
    for arete in aretes_voronoi:
        x1, y1 = arete[0]
        x2, y2 = arete[1]
        ax.plot([x1, x2], [y1, y2], 'r-', linewidth=1.8, zorder=3)

    # --- Sommets de Voronoï ---
    for cc in circumcentres.values():
        ax.plot(cc[0], cc[1], 'gs', markersize=4, zorder=4)

    # --- Points originaux avec numéros ---
    legendes = []
    for idx, p in enumerate(points):
        couleur = couleurs[idx % len(couleurs)]
        ax.plot(p[0], p[1], 'o', color=couleur, markersize=10,
                zorder=5, markeredgecolor='black', markeredgewidth=1.2)
        ax.annotate(f"P{idx+1}", xy=p,
                    xytext=(6, 6), textcoords='offset points',
                    fontsize=9, fontweight='bold')
        legendes.append(mpatches.Patch(color=couleur,
                                        label=f"P{idx+1} ({p[0]}, {p[1]})"))

    # --- Légende ---
    ax.legend(handles=legendes, loc='upper left',
              fontsize=8, framealpha=0.8)

    # --- Mise en forme ---
    ax.set_title("Diagramme de Voronoï (via triangulation de Delaunay)", fontsize=13)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    plt.tight_layout()
    plt.show()

def visualiser_interactif(points_initiaux, fichier):
    points = list(points_initiaux)

    def recalculer_et_afficher(ax, points):
        ax.clear()
        if len(points) < 3:
            for p in points:
                ax.plot(p[0], p[1], 'ko', markersize=8)
            ax.set_title("Ajoutez au moins 3 points (clic gauche)")
            ax.grid(True, alpha=0.3)
            fig.canvas.draw()
            return

        triangles = bowyer_watson(points)
        aretes_voronoi, circumcentres = extraire_aretes_voronoi_complet(points, triangles)

        xs_pts = [p[0] for p in points]
        ys_pts = [p[1] for p in points]
        marge = 3
        x_min, x_max = min(xs_pts) - marge, max(xs_pts) + marge
        y_min, y_max = min(ys_pts) - marge, max(ys_pts) + marge

        couleurs = list(mcolors.TABLEAU_COLORS.values())
        cellules = obtenir_cellules_voronoi(points, triangles, circumcentres)

        for idx, (point, sommets_cc) in enumerate(cellules.items()):
            if len(sommets_cc) >= 3:
                sommets_ordonnes = ordonner_polygone(sommets_cc)
                couleur = couleurs[idx % len(couleurs)]
                patch = mpatches.Polygon(sommets_ordonnes, closed=True,
                                         facecolor=couleur, alpha=0.25,
                                         edgecolor='none')
                ax.add_patch(patch)

        for triangle in triangles:
            p1, p2, p3 = triangle
            ax.plot([p1[0], p2[0], p3[0], p1[0]],
                    [p1[1], p2[1], p3[1], p1[1]],
                    'b-', linewidth=0.5, alpha=0.15)

        for arete in aretes_voronoi:
            ax.plot([arete[0][0], arete[1][0]],
                    [arete[0][1], arete[1][1]], 'r-', linewidth=1.8, zorder=3)

        for idx, p in enumerate(points):
            couleur = couleurs[idx % len(couleurs)]
            ax.plot(p[0], p[1], 'o', color=couleur, markersize=10,
                    zorder=5, markeredgecolor='black', markeredgewidth=1.2)
            ax.annotate(f"P{idx+1}", xy=p, xytext=(6, 6),
                        textcoords='offset points', fontsize=9, fontweight='bold')

        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title(f"Diagramme de Voronoï — {len(points)} points "
                     f"(clic gauche = ajouter, clic droit = supprimer dernier)")
        fig.canvas.draw()

    def on_click(event):
        if event.inaxes != ax:
            return
        if event.button == 1:  # clic gauche → ajouter
            nouveau = (round(event.xdata, 2), round(event.ydata, 2))
            points.append(nouveau)
            # Sauvegarder dans le fichier
            with open(fichier, 'w') as f:
                for p in points:
                    f.write(f"{p[0]},{p[1]}\n")
        elif event.button == 3:  # clic droit → supprimer dernier
            if points:
                points.pop()
        recalculer_et_afficher(ax, points)

    fig, ax = plt.subplots(figsize=(12, 10))
    fig.canvas.mpl_connect('button_press_event', on_click)
    recalculer_et_afficher(ax, points)
    plt.show()

# Visualisation statique avec toutes les améliorations
visualiser_voronoi_complet(points, triangles, aretes_voronoi, circumcentres)

# Visualisation interactive (clic gauche = ajouter, clic droit = supprimer)
visualiser_interactif(points, 'Claude/points.txt')