from random import *
from time import time
from matplotlib.pyplot import *

#Recuperer données
def get_PPP() :
    PPP = []
    with open('Points.txt', 'r') as f:
        for couple in f.readlines() :
            PPP.append(tuple(map(float, couple.strip().split(','))))
    return PPP

PPP = get_PPP()

#Calculer la germe la plus proche
def plus_proche(coin_x, coin_y, PPP) : 
    res = 0
    nb_PPP = len(PPP)
    for i in range(nb_PPP) : 
        xres = PPP[res][0]
        yres = PPP[res][1]

        xi = PPP[i][0]
        yi = PPP[i][1]

        if((coin_x-xres)**2+(coin_y-yres)**2>(coin_x-xi)**2+(coin_y-yi)**2) : res = i

    return res
###########################################
#         Paramètres modifiables          #
##########################################

#Taille de la fenetre graphique
xmin = 0
xmax = 20

ymin = 0
ymax = 20

#Maillage de la fenetre
N = 100

#Nombre de point
nb_point = 20


FC = ['red', 
      'lightgoldenrodyellow', 
      'beige', 
      'firebrick', 
      'green', 
      'blue', 
      'orange', 
      'cyan', 
      'brown', 
      'salmon', 
      'indigo', 
      'magenta', 
      'turquoise', 
      'pink', 
      'lavender', 
      'fuchsia', 
      'peru', 
      'oldlace', 
      'darkkhaki', 
      'peachpuff',
      'tomato'
     ]
shuffle(FC)
hauteur = (ymax-ymin)/N
longueur = (xmax-xmin)/N

# Crée un graphique vide
fig, ax = subplots(figsize=(10, 10))#figsize permet de préciser la taille de la fenetre (largeur, hauteur)

xlim(xmin, xmax)
ylim(ymin, ymax)

tic = time.time()
for i in range(N) : 
    coin_x = xmin + longueur*i
    for j in range(N) : 
        coin_y = ymin + hauteur*j
        
        rect = Rectangle((coin_x, coin_y), longueur, hauteur, facecolor=FC[plus_proche(coin_x, coin_y, PPP)%len(FC)])
        ax.add_patch(rect)

for P in PPP : 
    rect = Rectangle((P[0], P[1]), longueur, hauteur, facecolor='black')
    ax.add_patch(rect)

tac = time.time()


fig.savefig('voronoi.png')
# Affiche le graphique
show()

toc = time.time()

print(tac-tic)
print(toc-tac)