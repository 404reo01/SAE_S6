import time
import random
import matplotlib.pyplot as plt
from voronoi_logic import VoronoiSolver, Point

# --- ALGO MANUEL ---
def plus_proche(coin_x, coin_y, points_list): 
    res = 0
    for i in range(len(points_list)): 
        xres, yres = points_list[res].x, points_list[res].y
        xi, yi = points_list[i].x, points_list[i].y
        if ((coin_x-xres)**2 + (coin_y-yres)**2 > (coin_x-xi)**2 + (coin_y-yi)**2): 
            res = i
    return res

def run_manuel(points, N=100):
    xmin, xmax, ymin, ymax = 0, 20, 0, 20
    longueur = (xmax-xmin)/N
    hauteur = (ymax-ymin)/N
    for i in range(N):
        for j in range(N):
            plus_proche(xmin + longueur*i, ymin + hauteur*j, points)

# --- ALGO FORTUNE ---
def run_fortune(points):
    solver = VoronoiSolver(points)
    import heapq
    while solver.event_queue:
        event = heapq.heappop(solver.event_queue)
        if event.site:
            solver.handle_site_event(event.site, event.y)
        else:
            solver.handle_circle_event(event, event.y)

# --- BENCHMARK ---
def benchmark():
    tailles = [5, 10, 20, 50, 100]
    t_manuel, t_fortune = [], []

    print(f"{'Germes':<10} | {'Manuel (s)':<12} | {'Fortune (s)':<12}")
    print("-" * 40)

    for n in tailles:
        pts = [Point(random.uniform(0, 20), random.uniform(0, 20)) for _ in range(n)]

        # Mesure Manuel
        start = time.perf_counter()
        run_manuel(pts, N=100)
        t_manuel.append(time.perf_counter() - start)

        # Mesure Fortune
        start = time.perf_counter()
        run_fortune(pts)
        t_fortune.append(time.perf_counter() - start)

        print(f"{n:<10} | {t_manuel[-1]:<12.5f} | {t_fortune[-1]:<12.5f}")

    # Graphique
    plt.figure(figsize=(10, 6))
    plt.plot(tailles, t_manuel, label="Manuel (Maillage N=100)", marker='s', color='red')
    plt.plot(tailles, t_fortune, label="Fortune (Géométrique)", marker='o', color='blue')
    plt.xlabel("Nombre de germes")
    plt.ylabel("Temps de calcul (secondes)")
    plt.title("Comparaison de Complexité : Maillage vs Fortune")
    plt.legend()
    plt.grid(True)
    plt.savefig("analyse_performance.png")
    plt.show()

if __name__ == "__main__":
    benchmark()