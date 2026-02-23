import tkinter as tk
from voronoi_logic import load_points, Point, VoronoiSolver
import heapq

class VoronoiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SAÉ S6 - Générateur de Diagramme de Voronoï")
        self.width, self.height, self.padding = 800, 600, 50
        
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white")
        self.canvas.pack(pady=10)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack()
        tk.Button(btn_frame, text="Charger et Générer", command=self.load_and_solve).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Exporter SVG", command=self.export_svg).pack(side=tk.LEFT, padx=5)
        
        self.status = tk.Label(self.root, text="En attente de fichier...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.points = []
        self.colors = ["#FFB3BA", "#BAFFC9", "#BAE1FF", "#FFFFBA", "#FFDFBA", "#E0BBE4", "#D4F0F0", "#FEC8D8"]

    def calculate_scale(self):
        if not self.points: return
        min_x, max_x = min(p.x for p in self.points), max(p.x for p in self.points)
        min_y, max_y = min(p.y for p in self.points), max(p.y for p in self.points)
        data_w, data_h = max(1, max_x - min_x), max(1, max_y - min_y)
        self.scale = min((self.width - 2*self.padding)/data_w, (self.height - 2*self.padding)/data_h)
        self.offset_x = min_x - (self.width/self.scale - data_w)/2
        self.offset_y = min_y - (self.height/self.scale - data_h)/2

    def transform(self, px, py):
        return (px - self.offset_x) * self.scale, self.height - ((py - self.offset_y) * self.scale)

    def draw_final_diagram(self):
        """Calcule et affiche le diagramme complet."""
        self.canvas.delete("all")
        if not self.points: return

        # 1. Rendu des zones (Pixel-based Voronoi pour le fond)
        step = 3  # Précision
        for x in range(0, self.width, step):
            for y in range(0, self.height, step):
                rx = (x / self.scale) + self.offset_x
                ry = ((self.height - y) / self.scale) + self.offset_y
                
                best_dist = float('inf')
                closest_idx = 0
                for i, p in enumerate(self.points):
                    d = (p.x - rx)**2 + (p.y - ry)**2
                    if d < best_dist:
                        best_dist = d
                        closest_idx = i
                
                self.canvas.create_rectangle(x, y, x+step, y+step, 
                                           fill=self.colors[closest_idx % len(self.colors)], 
                                           outline="")

        # 2. Dessiner les germes par-dessus
        for p in self.points:
            x, y = self.transform(p.x, p.y)
            self.canvas.create_oval(x-4, y-4, x+4, y+4, fill="white", outline="black", width=2)

    def load_and_solve(self):
        """Charge le fichier et exécute tout l'algorithme instantanément."""
        pts = load_points("Points.txt")
        if pts:
            self.points = pts
            self.calculate_scale()
            
            # On initialise le solver juste pour valider la structure de données
            self.solver = VoronoiSolver(self.points)
            
            # On vide la file d'événements (Simulation complète)
            while self.solver.event_queue:
                event = heapq.heappop(self.solver.event_queue)
                if event.site:
                    self.solver.handle_site_event(event.site, event.y)
                else:
                    self.solver.handle_circle_event(event, event.y)
            
            self.draw_final_diagram()
            self.status.config(text=f"Diagramme généré pour {len(self.points)} points.")

 
    def export_svg(self):
        if not self.points:
            self.status.config(text="Erreur : Aucun point chargé.")
            return

        try:
            filename = "voronoi_final.svg"
            with open(filename, "w", encoding="utf-8") as f:
                # 1. En-tête SVG et fond blanc
                f.write(f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
                f.write(f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">\n')
                f.write(f'  <rect width="100%" height="100%" fill="white" />\n')

                # 2. Export des zones colorées (Regions)
                # On utilise un step légèrement plus grand pour éviter un fichier trop lourd
                step = 5 
                f.write('  <g id="regions">\n')
                for x in range(0, self.width, step):
                    for y in range(0, self.height, step):
                        # On retrouve les coordonnées mathématiques pour chaque pixel SVG
                        rx = (x / self.scale) + self.offset_x
                        ry = ((self.height - y) / self.scale) + self.offset_y
                        
                        best_dist = float('inf')
                        closest_idx = 0
                        for i, p in enumerate(self.points):
                            d = (p.x - rx)**2 + (p.y - ry)**2
                            if d < best_dist:
                                best_dist = d
                                closest_idx = i
                        
                        color = self.colors[closest_idx % len(self.colors)]
                        f.write(f'    <rect x="{x}" y="{y}" width="{step}" height="{step}" fill="{color}" />\n')
                f.write('  </g>\n')

                # 3. Export des germes (Sites) uniquement
                # On retire la boucle sur les "vertices" (points verts) qui posait problème
                f.write('  <g id="germes">\n')
                for p in self.points:
                    px, py = self.transform(p.x, p.y)
                    f.write(f'    <circle cx="{px}" cy="{py}" r="5" fill="white" stroke="black" stroke-width="2" />\n')
                f.write('  </g>\n')

                f.write('</svg>')
            
            self.status.config(text=f"Export réussi : {filename}")
            
        except Exception as e:
            self.status.config(text=f"Erreur export : {str(e)}")
if __name__ == "__main__":
    root = tk.Tk()
    app = VoronoiApp(root)
    root.mainloop()