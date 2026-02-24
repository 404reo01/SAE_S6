from matplotlib.pyplot import subplots, show
from matplotlib.patches import Rectangle
from random import shuffle
import time


class Visualisation:
    def __init__(self, xmin, xmax, ymin, ymax, N):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.N = N

        self.FC = [
            'red', 'lightgoldenrodyellow', 'beige', 'firebrick', 'green', 
            'blue', 'orange', 'cyan', 'brown', 'salmon', 'indigo', 
            'magenta', 'turquoise', 'pink', 'lavender', 'fuchsia', 
            'peru', 'oldlace', 'darkkhaki', 'peachpuff', 'tomato'
        ]
        shuffle(self.FC)

    def dessiner(self, calculateur):
        hauteur = (self.ymax - self.ymin) / self.N
        longueur = (self.xmax - self.xmin) / self.N

        fig, ax = subplots(figsize=(10, 10))
        ax.set_xlim(self.xmin, self.xmax)
        ax.set_ylim(self.ymin, self.ymax)

        tic = time.time()
        
        for i in range(self.N): 
            coin_x = self.xmin + longueur * i
            for j in range(self.N): 
                coin_y = self.ymin + hauteur * j
                
                indice_proche = calculateur.plus_proche(coin_x, coin_y)
                couleur = self.FC[indice_proche % len(self.FC)]
                
                rect = Rectangle((coin_x, coin_y), longueur, hauteur, facecolor=couleur)
                ax.add_patch(rect)

        for P in calculateur.points: 
            rect = Rectangle((P[0], P[1]), longueur, hauteur, facecolor='black')
            ax.add_patch(rect)

        tac = time.time()
        print(f"Temps de calcul et dessin : {tac - tic:.3f} secondes")

        fig.savefig('resultats/phase1/voronoi.png')
        show()