import pytest
from Phase_1.Diagramme.Calcul_germe import CalculerGerme
from Phase_1.Diagramme.ReadPoints import LirePoints

def test_should_return_list_of_tuples_given_valid_file(tmp_path):
    # Arrange
    tmp = tmp_path / "test_points.txt"
    with open(tmp, 'w') as f : 
        f.write("10.5, 20.0 \n 0, 0 \n -5.2, 3.14")
    lecteur = LirePoints(tmp)

    #Act
    resultats = lecteur.get_Points()

    #Assert
    assert len(resultats) == 3
    assert resultats[0] == (10.5, 20.0)
    assert resultats[1] == (0.0, 0.0)
    assert resultats[2] == (-5.2, 3.14)


def test_should_raise_value_error_given_invalid_file(tmp_path):
    # Arrange
    tmp = tmp_path / "test_phrases.txt"
    with open(tmp, 'w') as f: 
        f.write("points \n Ce n'est pas un nombre \n Test")
    
    lecteur = LirePoints(tmp)

    # Act / Assert
    with pytest.raises(ValueError):
        lecteur.get_Points()


def test_should_return_empty_list_given_empty_file(tmp_path):
    # Arrange
    tmp = tmp_path / "test_vide.txt"
    with open(tmp, 'w') as f: 
        pass 
    
    lecteur = LirePoints((tmp))

    # Act
    resultats = lecteur.get_Points()

    # Assert
    assert resultats == []


def test_should_return_exact_point_index_given_coordinates_matching_a_point():
    # Arrange
    points = [(0, 0), (10, 10), (20, 20)]
    calculateur = CalculerGerme(points)
    x_cible, y_cible = 10, 10
    
    # Act
    resultat = calculateur.plus_proche(x_cible, y_cible)
    
    # Assert
    assert resultat == 1


def test_should_return_closest_point_index_given_obvious_distance():
    # Arrange
    points = [(0, 0), (10, 10)]
    calculateur = CalculerGerme(points)
    x_cible, y_cible = 2, 2
    
    # Act
    resultat = calculateur.plus_proche(x_cible, y_cible)
    
    # Assert
    assert resultat == 0


def test_should_return_first_point_index_given_equidistant_target():
    # Arrange
    points = [(0, 0), (10, 0)]
    calculateur = CalculerGerme(points)
    x_cible, y_cible = 5, 0 
    
    # Act
    resultat = calculateur.plus_proche(x_cible, y_cible)
    
    # Assert
    assert resultat == 0

def test_should_return_correct_index_given_negative_coordinates():
    # Arrange
    points = [(-10, -10), (5, 5)]
    calculateur = CalculerGerme(points)
    x_cible, y_cible = -8, -8
    
    # Act
    resultat = calculateur.plus_proche(x_cible, y_cible)
    
    # Assert
    assert resultat == 0


def test_should_return_first_index_given_duplicate_points():
    # Arrange
    points = [(5, 5), (5, 5)]
    calculateur = CalculerGerme(points)
    x_cible, y_cible = 6, 6
    
    # Act
    resultat = calculateur.plus_proche(x_cible, y_cible)
    
    # Assert
    assert resultat == 0