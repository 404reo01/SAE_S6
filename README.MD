# Déterminer un diagramme de Voronoï 


Dans le cadre de la Saé du semestre 6 de BUT 3 informatique, nous devions réaliser un projet qui permet de générer des diagrammes de Voronoï à partir de fichiers qui contiennent une liste de points sous forme de paire de nombres qui correspondent aux coordonnées. 

## 1. Technique de génération


Le principe de génération de notre algorithme est simple et repose sur un découpage en grille. Dans un premier temps, on place les points de départ, appelés germes, dans l'espace de dessin. Cet espace est ensuite virtuellement découpé en une grille régulière, semblable à un écran composé de pixels. Pour chaque cellule de cette grille, l'algorithme calcule les distances pour déterminer quel est le germe le plus proche. Une fois cette proximité établie, on colorie simplement la cellule avec la couleur spécifique de ce point.


## 2. Installation et prérequis

Nous vous recommandons d'utiliser un environnement virtuel pour isoler les dépendances du projet et d'utiliser au moins **Python 3.9**.


**A. Cloner ou télécharger le projet, puis ouvrir un terminal à la racine.**

**B. Créer l'environnement virtuel :**

* Sur **Windows** :
  ```bash
  python -m venv venv
  ```
* Sur **Linux et macOS** :
  ```bash
  python3 -m venv venv
  ```
**C. Activer l'environnement virtuel :**
* Sur **Windows** :
  ```bash
  venv\Scripts\activate
  ```
* Sur **Linux et macOS** :
  ```bash
  source venv/bin/activate
  ```
**D. Installer les dépendances (Matplotlib, Pytest...) :**
* Sur **Windows, Linux et macOS** :
  ```bash 
  pip install -r requirements.txt
  ```


## 3. Utilisation
Tout d'abord, pour la phase 1, assurez vous d'avoir un fichier texte contenant vos points avec une coordonnée par ligne (x, y) dans le dossier data de préférence sinon à la racine. Le script cible le fichier **Points.txt** par défaut mais vous pouvez changer le chemin dans le fichier **Phase_1/main.py**.
* Ensuite lancez le script principal depuis le terminal avec le venv activé :
    ```bash
    python Phase_1/main.py
    ```
Enfin, l'application ouvrira une fenêtre, affichera le diagramme et l'exportera automatiquement au format png dans le dossier resultats.

## 4. Tests unitaires

Le projet contient une suite de tests unitaires pour garantir la fiabilité de la lecture des données et de l'algorithme de calcul (fichiers vides, données textuelles invalides, points superposés).

* Pour lancer la suite de tests, assurez-vous que l'environnement virtuel est activé et exécutez simplement :
    ```bash
    pytest Phase_1/tests/tests_voronoi.py
    ```