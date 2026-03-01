import numpy as np
import matplotlib.pyplot as plt

def plot_diagram(ax, model):
    """
    Trace le diagramme de Voronoi en coloriant chaque pixel selon le site le plus proche.
    Les points sont superposés en rouge.
    """
    if not model.has_valid_diagram():
        return

    points = np.array(model.get_points())
    if len(points) < 2:
        return

    # Déterminer les limites de la zone à afficher (avec une marge)
    margin = 5.0
    x_min, y_min = points.min(axis=0) - margin
    x_max, y_max = points.max(axis=0) + margin

    # Créer une grille de résolution (ajuster pour plus de précision / performance)
    resolution = 500
    x = np.linspace(x_min, x_max, resolution)
    y = np.linspace(y_min, y_max, resolution)
    xx, yy = np.meshgrid(x, y)
    grid = np.stack((xx, yy), axis=-1)  # shape (res, res, 2)

    # Calculer pour chaque point de la grille la distance à tous les sites
    # et trouver l'index du site le plus proche
    # (dimensions : grid (res,res,2) - points (n,2) -> distances (res,res,n))
    distances = np.linalg.norm(grid[:, :, np.newaxis, :] - points[np.newaxis, np.newaxis, :, :], axis=-1)
    labels = np.argmin(distances, axis=-1)  # (res, res)

    # Afficher l'image avec une palette de couleurs
    cmap = plt.get_cmap('tab20')
    # Normaliser les labels pour qu'ils correspondent aux indices de la colormap
    im = ax.imshow(labels, extent=(x_min, x_max, y_min, y_max), origin='lower',
                   cmap=cmap, alpha=0.5, interpolation='nearest')

    # Tracer les points par-dessus
    ax.plot(points[:, 0], points[:, 1], 'ro', markersize=5, zorder=3)

    # Ajuster l'aspect
    ax.set_aspect('equal')
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_title("Diagramme de Voronoi")