import time
import numpy as np
from scipy.spatial import Voronoi
import matplotlib.pyplot as plt
import pandas as pd

# ---------- Méthode manuelle ----------
def plus_proche(coin_x, coin_y, points_list):
    """
    Retourne l'indice du point le plus proche de (coin_x, coin_y).
    points_list est une liste d'objets avec attributs x et y.
    """
    res = 0
    for i in range(len(points_list)):
        xres, yres = points_list[res].x, points_list[res].y
        xi, yi = points_list[i].x, points_list[i].y
        # Comparaison des distances au carré (évite sqrt inutile)
        if ((coin_x - xres)**2 + (coin_y - yres)**2 > (coin_x - xi)**2 + (coin_y - yi)**2):
            res = i
    return res

def run_manuel(points, N=100):
    """
    Parcourt une grille NxN dans la zone [0,20]x[0,20] et, pour chaque cellule,
    trouve le point le plus proche via plus_proche.
    """
    xmin, xmax, ymin, ymax = 0, 20, 0, 20
    longueur = (xmax - xmin) / N
    hauteur = (ymax - ymin) / N
    for i in range(N):
        for j in range(N):
            plus_proche(xmin + longueur * i, ymin + hauteur * j, points)

# ---------- Méthode scipy ----------
def run_scipy(points_array):
    """
    Construit le diagramme de Voronoi à l'aide de scipy.spatial.Voronoi.
    """
    vor = Voronoi(points_array)
    return vor  # on retourne l'objet, mais on ne mesure que le temps de construction

# ---------- Benchmark ----------
def benchmark():
    # Paramètres à faire varier
    nb_points_list = [10, 50, 100, 200, 500]
    resolutions = [50, 100, 200, 500]  # valeurs de N
    repetitions = 3  # nombre de répétitions pour lisser les mesures

    results = []

    for nb_points in nb_points_list:
        # Génération aléatoire des points dans [0,20]
        points_array = np.random.uniform(0, 20, (nb_points, 2))

        # Conversion en objets pour la méthode manuelle
        class Point:
            def __init__(self, x, y):
                self.x = x
                self.y = y
        points_manuels = [Point(p[0], p[1]) for p in points_array]

        for N in resolutions:
            # Mesure du temps pour la méthode manuelle
            t_manual = 0.0
            for _ in range(repetitions):
                start = time.perf_counter()
                run_manuel(points_manuels, N)
                end = time.perf_counter()
                t_manual += (end - start)
            t_manual /= repetitions

            # Mesure du temps pour la méthode scipy
            t_scipy = 0.0
            for _ in range(repetitions):
                start = time.perf_counter()
                run_scipy(points_array)
                end = time.perf_counter()
                t_scipy += (end - start)
            t_scipy /= repetitions

            # Stockage des résultats
            results.append({
                'nb_points': nb_points,
                'N': N,
                'manual_time': t_manual,
                'scipy_time': t_scipy,
                'ratio': t_manual / t_scipy if t_scipy > 0 else float('inf')
            })

            print(f"Points: {nb_points:3d}, N={N:3d} -> Manuel: {t_manual:.6f}s, Scipy: {t_scipy:.6f}s, Ratio: {t_manual/t_scipy:.2f}")

    return results

# ---------- Exécution et visualisation ----------
if __name__ == "__main__":
    results = benchmark()
    df = pd.DataFrame(results)
    print("\n--- Tableau récapitulatif ---")
    print(df.to_string(index=False))

    # Tracé des courbes (temps en fonction de N, pour chaque nombre de points)
    plt.figure(figsize=(12, 8))
    for nb_points in df['nb_points'].unique():
        subset = df[df['nb_points'] == nb_points]
        plt.plot(subset['N'], subset['manual_time'], 'o-', label=f'Manuel {nb_points} pts')
        plt.plot(subset['N'], subset['scipy_time'], 's-', label=f'Scipy {nb_points} pts')
    plt.xlabel('Résolution N (grille N×N)')
    plt.ylabel('Temps moyen (s)')
    plt.title('Comparaison des performances : méthode manuelle vs scipy.spatial.Voronoi')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Éventuellement, afficher le ratio en échelle logarithmique
    plt.figure(figsize=(10, 6))
    for nb_points in df['nb_points'].unique():
        subset = df[df['nb_points'] == nb_points]
        plt.plot(subset['N'], subset['ratio'], 'o-', label=f'Ratio pour {nb_points} pts')
    plt.xlabel('Résolution N')
    plt.ylabel('Ratio manuel / scipy')
    plt.title('Rapport des temps d\'exécution')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.show()