import math
import heapq

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

class Arc:
    def __init__(self, site, left=None, right=None):
        self.site = site
        self.left = left
        self.right = right
        self.event = None 

class Event:
    def __init__(self, x, y, site=None, is_circle=False, center=None, arc=None):
        self.x = x
        self.y = y
        self.site = site
        self.is_circle = is_circle
        self.center = center 
        self.arc = arc       
        self.valid = True    

    def __lt__(self, other):
        if abs(self.y - other.y) < 1e-9:
            return self.x < other.x
        return self.y > other.y

def load_points(filename):
    """Charge les points depuis un fichier texte (format: x,y)."""
    points = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    points.append(Point(float(parts[0]), float(parts[1])))
    except Exception as e:
        print(f"Erreur de lecture : {e}")
    return points

def get_circumcircle(p1, p2, p3):
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    x3, y3 = p3.x, p3.y
    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if abs(d) < 1e-9: return None 
    cx = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / d
    cy = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / d
    radius = math.sqrt((x1 - cx)**2 + (y1 - cy)**2)
    return Point(cx, cy), cy - radius

class VoronoiSolver:
    def __init__(self, points):
        self.event_queue = []
        for p in points:
            heapq.heappush(self.event_queue, Event(p.x, p.y, site=p))
        self.root = None
        self.vertices = [] 

    def check_circle_event(self, arc, sweep_y):
        if arc.event: arc.event.valid = False
        if not arc.left or not arc.right: return
        res = get_circumcircle(arc.left.site, arc.site, arc.right.site)
        if res:
            center, event_y = res
            if event_y <= sweep_y:
                new_event = Event(center.x, event_y, is_circle=True, center=center, arc=arc)
                arc.event = new_event
                heapq.heappush(self.event_queue, new_event)

    def handle_site_event(self, site, sweep_y):
        if not self.root:
            self.root = Arc(site)
            return
        curr = self.root
        while curr.right:
            x_inter = self.get_breakpoint(curr.site, curr.right.site, sweep_y)
            if site.x > x_inter: curr = curr.right
            else: break
        old_right = curr.right
        new_arc = Arc(site, left=curr)
        split_arc = Arc(curr.site, left=new_arc, right=old_right)
        new_arc.right = split_arc
        curr.right = new_arc
        if old_right: old_right.left = split_arc
        self.check_circle_event(curr, sweep_y)
        self.check_circle_event(split_arc, sweep_y)

    def handle_circle_event(self, event, sweep_y):
        if not event.valid: return
        self.vertices.append(event.center)
        arc = event.arc
        if arc.left: arc.left.right = arc.right
        if arc.right: arc.right.left = arc.left
        if arc.left: self.check_circle_event(arc.left, sweep_y)
        if arc.right: self.check_circle_event(arc.right, sweep_y)

    def get_breakpoint(self, left_site, right_site, sweep_y):
        if abs(left_site.y - right_site.y) < 1e-9:
            return (left_site.x + right_site.x) / 2.0
        h1, k1 = left_site.x, left_site.y
        h2, k2 = right_site.x, right_site.y
        a = 1.0/(2*(k1-sweep_y)) - 1.0/(2*(k2-sweep_y))
        b = -h1/(k1-sweep_y) + h2/(k2-sweep_y)
        c = (h1**2 + k1**2 - sweep_y**2)/(2*(k1-sweep_y)) - (h2**2 + k2**2 - sweep_y**2)/(2*(k2-sweep_y))
        delta = b**2 - 4*a*c
        return (-b + math.sqrt(max(0, delta))) / (2*a)
    
class Edge:
    def __init__(self, p1, p2, site_left, site_right):
        self.p1 = p1  # Sommet de départ
        self.p2 = p2  # Sommet d'arrivée (None si infini au début)
        self.site_left = site_left
        self.site_right = site_right