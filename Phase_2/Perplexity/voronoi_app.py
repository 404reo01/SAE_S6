import tkinter as tk
import math
from typing import List, Tuple

class Point:
    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

class VoronoiApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Voronoi - points.txt")
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack()
        
        tk.Button(self.root, text="🔄 Lire & Dessiner", command=self.refresh).pack()
        
        self.points = []
        self.colors = ['red', 'green', 'blue', 'orange', 'purple', 'yellow']
    
    def load_points(self):
        """LIT VOTRE points.txt"""
        self.points = []
        with open("Phase_2/Perplexity/points.txt", 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    x, y = map(float, line.split())
                    self.points.append(Point(x, y))
        print(f"✅ {len(self.points)} points lus")
    
    def refresh(self):
        self.load_points()  # ← LIT points.txt
        self.draw_voronoi()
    
    # ... TOUT LE RESTE IDENTIQUE (pixel_to_point, point_to_pixel, draw_voronoi)
    def pixel_to_point(self, x: int, y: int) -> Tuple[float, float]:
        if not self.points: return 0, 0
        minx, maxx = min(p.x for p in self.points), max(p.x for p in self.points)
        miny, maxy = min(p.y for p in self.points), max(p.y for p in self.points)
        scale = min(780/(maxx-minx), 580/(maxy-miny))
        ox = 10; oy = 10
        return (x-ox)/scale, ((590-oy)-y)/scale

    def point_to_pixel(self, px: float, py: float) -> Tuple[int, int]:
        if not self.points: return 400, 300
        minx, maxx = min(p.x for p in self.points), max(p.x for p in self.points)
        miny, maxy = min(p.y for p in self.points), max(p.y for p in self.points)
        scale = min(780/(maxx-minx), 580/(maxy-miny))
        ox = 10; oy = 10
        x = px * scale + ox
        y = (590 - oy) - (py * scale)
        return int(x), int(y)

    def draw_voronoi(self):
        self.canvas.delete("all")
        step = 2
        for x in range(0, 800, step):
            for y in range(0, 600, step):
                rx, ry = self.pixel_to_point(x, y)
                closest = 0
                best_dist = float('inf')
                for i, p in enumerate(self.points):
                    dist = (p.x - rx)**2 + (p.y - ry)**2
                    if dist < best_dist:
                        best_dist = dist
                        closest = i
                color = self.colors[closest % len(self.colors)]
                self.canvas.create_rectangle(x, y, x+step, y+step, fill=color)

        for i, p in enumerate(self.points):
            px, py = self.point_to_pixel(p.x, p.y)
            self.canvas.create_oval(px-8, py-8, px+8, py+8, fill='white', outline='black', width=3)
            self.canvas.create_text(px+20, py-10, text=f'P{i+1}', font=('Arial', 12))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = VoronoiApp()
    app.run()
