import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors

# ─────────────────────────────────────────────
# 1. LECTURE DU FICHIER
# ─────────────────────────────────────────────

def lire_points(fichier):
    points = []
    with open(fichier, 'r') as f:
        for ligne in f:
            ligne = ligne.strip()
            if ligne and ',' in ligne:
                parties = ligne.split(',')
                try:
                    x, y = float(parties[0].strip()), float(parties[1].strip())
                    points.append((x, y))
                except ValueError:
                    print(f"Ligne ignorée : {repr(ligne)}")
    return points


# ─────────────────────────────────────────────
# 2. CERCLE CIRCONSCRIT
# ─────────────────────────────────────────────

def circumcircle(p1, p2, p3):
    ax, ay = p1
    bx, by = p2
    cx, cy = p3
    D = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(D) < 1e-10:
        return None
    ux = ((ax**2 + ay**2) * (by - cy) +
          (bx**2 + by**2) * (cy - ay) +
          (cx**2 + cy**2) * (ay - by)) / D
    uy = ((ax**2 + ay**2) * (cx - bx) +
          (bx**2 + by**2) * (ax - cx) +
          (cx**2 + cy**2) * (bx - ax)) / D
    rayon = ((ax - ux)**2 + (ay - uy)**2) ** 0.5
    return (ux, uy, rayon)


# ─────────────────────────────────────────────
# 3. TRIANGULATION DE DELAUNAY (BOWYER-WATSON)
# ─────────────────────────────────────────────

def super_triangle(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    delta = max(max_x - min_x, max_y - min_y) * 100
    return (
        (min_x - delta,     min_y - delta),
        (min_x + 2 * delta, min_y - delta),
        (min_x - delta,     min_y + 2 * delta)
    )

def bowyer_watson(points):
    st1, st2, st3 = super_triangle(points)
    triangles = [(st1, st2, st3)]

    for point in points:
        invalides = []
        for tri in triangles:
            cc = circumcircle(*tri)
            if cc is None:
                continue
            cx, cy, r = cc
            if ((point[0] - cx)**2 + (point[1] - cy)**2) ** 0.5 < r - 1e-10:
                invalides.append(tri)

        aretes = []
        for tri in invalides:
            p1, p2, p3 = tri
            aretes += [(p1, p2), (p2, p3), (p3, p1)]

        aretes_ext = []
        for i, (a, b) in enumerate(aretes):
            dupliquee = any(
                i != j and ((a == c and b == d) or (a == d and b == c))
                for j, (c, d) in enumerate(aretes)
            )
            if not dupliquee:
                aretes_ext.append((a, b))

        for t in invalides:
            triangles.remove(t)
        for arete in aretes_ext:
            triangles.append((arete[0], arete[1], point))

    st_pts = {st1, st2, st3}
    return [t for t in triangles if not any(p in st_pts for p in t)]


# ─────────────────────────────────────────────
# 4. EXTRACTION DES ARÊTES DE VORONOÏ
# ─────────────────────────────────────────────

def calculer_bbox(points, marge=5):
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    return (min(xs) - marge, max(xs) + marge, min(ys) - marge, max(ys) + marge)

def clipper_segment(p1, p2, bbox):
    """Algorithme de Cohen-Sutherland."""
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
        if not (c1 | c2):
            return (x1, y1), (x2, y2)
        elif c1 & c2:
            return None
        else:
            c = c1 if c1 else c2
            if c & 8:
                x = x1 + (x2 - x1) * (max_y - y1) / (y2 - y1); y = max_y
            elif c & 4:
                x = x1 + (x2 - x1) * (min_y - y1) / (y2 - y1); y = min_y
            elif c & 2:
                y = y1 + (y2 - y1) * (max_x - x1) / (x2 - x1); x = max_x
            else:
                y = y1 + (y2 - y1) * (min_x - x1) / (x2 - x1); x = min_x
            if c == c1:
                x1, y1, c1 = x, y, code((x, y))
            else:
                x2, y2, c2 = x, y, code((x, y))

def extraire_voronoi(points, triangles):
    bbox = calculer_bbox(points)
    min_x, max_x, min_y, max_y = bbox

    circumcentres = {}
    for tri in triangles:
        cc = circumcircle(*tri)
        if cc is not None:
            circumcentres[tri] = (cc[0], cc[1])

    aretes = []

    # Arêtes intérieures
    for i, t1 in enumerate(triangles):
        for j, t2 in enumerate(triangles):
            if j <= i:
                continue
            communs = [p for p in t1 if p in t2]
            if len(communs) == 2 and t1 in circumcentres and t2 in circumcentres:
                seg = clipper_segment(circumcentres[t1], circumcentres[t2], bbox)
                if seg:
                    aretes.append(seg)

    # Arêtes semi-infinies
    toutes = []
    for tri in triangles:
        p1, p2, p3 = tri
        toutes += [(p1, p2, tri), (p2, p3, tri), (p3, p1, tri)]

    for i, (a, b, tri) in enumerate(toutes):
        frontiere = all(
            not ((a == c and b == d) or (a == d and b == c))
            for j, (c, d, _) in enumerate(toutes) if i != j
        )
        if not frontiere or tri not in circumcentres:
            continue
        cx, cy = circumcentres[tri]
        if not (min_x <= cx <= max_x and min_y <= cy <= max_y):
            continue

        dx, dy = b[0] - a[0], b[1] - a[1]
        longueur = (dx**2 + dy**2) ** 0.5
        perp_x, perp_y = -dy / longueur, dx / longueur

        troisieme = [p for p in tri if p != a and p != b][0]
        vers_x, vers_y = troisieme[0] - cx, troisieme[1] - cy
        if perp_x * vers_x + perp_y * vers_y > 0:
            perp_x, perp_y = -perp_x, -perp_y

        p_loin = (cx + perp_x * 1000, cy + perp_y * 1000)
        seg = clipper_segment((cx, cy), p_loin, bbox)
        if seg:
            aretes.append(seg)

    return aretes, circumcentres


# ─────────────────────────────────────────────
# 5. CELLULES VORONOÏ CLIPPÉES À LA BBOX
# ─────────────────────────────────────────────

def obtenir_cellules(points, aretes, bbox):
    """
    Pour chaque point, collecter les sommets des arêtes de Voronoï
    qui forment sa cellule, en cherchant les arêtes dont les deux
    extrémités sont équidistantes à ce point.
    """
    min_x, max_x, min_y, max_y = bbox
    coins = [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)]

    cellules = {p: set() for p in points}

    for seg in aretes:
        s1, s2 = seg
        # Trouver les deux points de Voronoï les plus proches de ce segment
        # = les deux points dont cette arête est la frontière
        mid = ((s1[0]+s2[0])/2, (s1[1]+s2[1])/2)
        distances = sorted(points, key=lambda p: (p[0]-mid[0])**2 + (p[1]-mid[1])**2)
        # Les deux points les plus proches du milieu de l'arête
        p1, p2 = distances[0], distances[1]
        cellules[p1].add(s1)
        cellules[p1].add(s2)
        cellules[p2].add(s1)
        cellules[p2].add(s2)

    # Ajouter les coins de bbox au point le plus proche
    for coin in coins:
        pt = min(points, key=lambda p: (p[0]-coin[0])**2 + (p[1]-coin[1])**2)
        cellules[pt].add(coin)

    return {p: list(s) for p, s in cellules.items()}

def ordonner_polygone(sommets):
    cx = sum(s[0] for s in sommets) / len(sommets)
    cy = sum(s[1] for s in sommets) / len(sommets)
    return sorted(sommets, key=lambda s: math.atan2(s[1] - cy, s[0] - cx))


# ─────────────────────────────────────────────
# 6. VISUALISATION STATIQUE
# ─────────────────────────────────────────────

def visualiser(points, triangles, aretes, circumcentres):
    bbox = calculer_bbox(points)
    min_x, max_x, min_y, max_y = bbox
    couleurs = list(mcolors.TABLEAU_COLORS.values())

    fig, ax = plt.subplots(figsize=(12, 10))

    # Cellules coloriées et clippées
    cellules = obtenir_cellules(points, aretes, bbox)
    for idx, (pt, sommets) in enumerate(cellules.items()):
        if len(sommets) >= 3:
            poly = ordonner_polygone(sommets)
            patch = mpatches.Polygon(poly, closed=True,
                                     facecolor=couleurs[idx % len(couleurs)],
                                     alpha=0.3, edgecolor='none')
            ax.add_patch(patch)

    # Triangulation Delaunay (très transparente)
    for tri in triangles:
        p1, p2, p3 = tri
        ax.plot([p1[0], p2[0], p3[0], p1[0]],
                [p1[1], p2[1], p3[1], p1[1]],
                'b-', linewidth=0.5, alpha=0.15)

    # Arêtes Voronoï
    for seg in aretes:
        ax.plot([seg[0][0], seg[1][0]], [seg[0][1], seg[1][1]],
                'r-', linewidth=1.8, zorder=3)

    # Sommets Voronoï
    for cc in circumcentres.values():
        ax.plot(cc[0], cc[1], 'gs', markersize=4, zorder=4)

    # Points + légende
    legendes = []
    for idx, p in enumerate(points):
        c = couleurs[idx % len(couleurs)]
        ax.plot(p[0], p[1], 'o', color=c, markersize=10, zorder=5,
                markeredgecolor='black', markeredgewidth=1.2)
        ax.annotate(f"P{idx+1}", xy=p, xytext=(6, 6),
                    textcoords='offset points', fontsize=9, fontweight='bold')
        legendes.append(mpatches.Patch(color=c, label=f"P{idx+1} ({p[0]}, {p[1]})"))

    ax.legend(handles=legendes, loc='upper left', fontsize=8, framealpha=0.8)
    ax.set_title("Diagramme de Voronoï (via triangulation de Delaunay)", fontsize=13)
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.grid(True, alpha=0.3); ax.set_aspect('equal')
    ax.set_xlim(min_x, max_x); ax.set_ylim(min_y, max_y)
    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────
# 7. VISUALISATION INTERACTIVE
# ─────────────────────────────────────────────

def visualiser_interactif(points_initiaux, fichier):
    points = list(points_initiaux)
    couleurs = list(mcolors.TABLEAU_COLORS.values())

    def rafraichir(ax):
        ax.clear()
        if len(points) < 3:
            for p in points:
                ax.plot(p[0], p[1], 'ko', markersize=8)
            ax.set_title("Ajoutez au moins 3 points (clic gauche)")
            ax.grid(True, alpha=0.3)
            fig.canvas.draw()
            return

        tris = bowyer_watson(points)
        aretes, ccs = extraire_voronoi(points, tris)
        bbox = calculer_bbox(points)
        min_x, max_x, min_y, max_y = bbox

        cellules = obtenir_cellules(points, aretes, bbox)
        for idx, (pt, sommets) in enumerate(cellules.items()):
            if len(sommets) >= 3:
                poly = ordonner_polygone(sommets)
                patch = mpatches.Polygon(poly, closed=True,
                                         facecolor=couleurs[idx % len(couleurs)],
                                         alpha=0.3, edgecolor='none')
                ax.add_patch(patch)

        for tri in tris:
            p1, p2, p3 = tri
            ax.plot([p1[0], p2[0], p3[0], p1[0]],
                    [p1[1], p2[1], p3[1], p1[1]],
                    'b-', linewidth=0.5, alpha=0.15)

        for seg in aretes:
            ax.plot([seg[0][0], seg[1][0]], [seg[0][1], seg[1][1]],
                    'r-', linewidth=1.8, zorder=3)

        for idx, p in enumerate(points):
            c = couleurs[idx % len(couleurs)]
            ax.plot(p[0], p[1], 'o', color=c, markersize=10, zorder=5,
                    markeredgecolor='black', markeredgewidth=1.2)
            ax.annotate(f"P{idx+1}", xy=p, xytext=(6, 6),
                        textcoords='offset points', fontsize=9, fontweight='bold')

        ax.set_xlim(min_x, max_x); ax.set_ylim(min_y, max_y)
        ax.set_aspect('equal'); ax.grid(True, alpha=0.3)
        ax.set_title(f"Voronoï — {len(points)} points  |  "
                     f"clic gauche = ajouter  |  clic droit = supprimer dernier")
        fig.canvas.draw()

    def on_click(event):
        if event.inaxes != ax:
            return
        if event.button == 1:
            points.append((round(event.xdata, 2), round(event.ydata, 2)))
            with open(fichier, 'w') as f:
                for p in points:
                    f.write(f"{p[0]},{p[1]}\n")
        elif event.button == 3 and points:
            points.pop()
        rafraichir(ax)

    fig, ax = plt.subplots(figsize=(12, 10))
    fig.canvas.mpl_connect('button_press_event', on_click)
    rafraichir(ax)
    plt.show()

# ─────────────────────────────────────────────
# EXPORT SVG
# ─────────────────────────────────────────────

def exporter_svg(points, aretes, fichier_svg='voronoi.svg'):
    bbox = calculer_bbox(points)
    min_x, max_x, min_y, max_y = bbox
    largeur = max_x - min_x
    hauteur = max_y - min_y
    marge = 20  # marge en pixels

    couleurs = list(mcolors.TABLEAU_COLORS.values())
    cellules = obtenir_cellules(points, aretes, bbox)

    # Fonction pour convertir coordonnées → pixels SVG (y inversé)
    def to_svg(x, y):
        px = (x - min_x) / largeur * 800 + marge
        py = (1 - (y - min_y) / hauteur) * 600 + marge
        return px, py

    lignes = []
    lignes.append(f'<svg xmlns="http://www.w3.org/2000/svg" '
                  f'width="{800 + 2*marge}" height="{600 + 2*marge}">')

    # Cellules colorées
    for idx, (pt, sommets) in enumerate(cellules.items()):
        if len(sommets) >= 3:
            poly = ordonner_polygone(sommets)
            couleur = couleurs[idx % len(couleurs)]
            pts_svg = " ".join(f"{to_svg(s[0], s[1])[0]:.2f},{to_svg(s[0], s[1])[1]:.2f}"
                               for s in poly)
            lignes.append(f'  <polygon points="{pts_svg}" '
                          f'fill="{couleur}" fill-opacity="0.4" stroke="none"/>')

    # Arêtes de Voronoï
    for seg in aretes:
        x1, y1 = to_svg(*seg[0])
        x2, y2 = to_svg(*seg[1])
        lignes.append(f'  <line x1="{x1:.2f}" y1="{y1:.2f}" '
                      f'x2="{x2:.2f}" y2="{y2:.2f}" '
                      f'stroke="red" stroke-width="1.5"/>')

    # Points originaux
    for idx, p in enumerate(points):
        couleur = couleurs[idx % len(couleurs)]
        px, py = to_svg(p[0], p[1])
        lignes.append(f'  <circle cx="{px:.2f}" cy="{py:.2f}" r="6" '
                      f'fill="{couleur}" stroke="black" stroke-width="1.2"/>')
        lignes.append(f'  <text x="{px+8:.2f}" y="{py-8:.2f}" '
                      f'font-size="11" font-weight="bold">P{idx+1}</text>')

    lignes.append('</svg>')

    with open(fichier_svg, 'w') as f:
        f.write("\n".join(lignes))

    print(f"SVG exporté : {fichier_svg}")

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    FICHIER = 'points.txt'

    points = lire_points(FICHIER)
    triangles = bowyer_watson(points)
    aretes, circumcentres = extraire_voronoi(points, triangles)

    exporter_svg(points, aretes, 'voronoi.svg')

    # Visualisation statique
    visualiser(points, triangles, aretes, circumcentres)

    # Visualisation interactive
    visualiser_interactif(points, FICHIER)

