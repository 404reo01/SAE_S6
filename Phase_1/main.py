from Diagramme.ReadPoints import LirePoints
from Diagramme.Calcul_germe import CalculerGerme
from Diagramme.Visualisation import Visualisation

lecteur = LirePoints("data/Points.txt") 
mes_points = lecteur.get_Points()
calculateur = CalculerGerme(mes_points)
visu = Visualisation(0, 20, 0, 20, 100)
visu.dessiner(calculateur)