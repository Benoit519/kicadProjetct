# -*- coding: utf-8 -*-
import pcbnew

board = pcbnew.GetBoard()

# Parametres de placement
start_x = 300.0  # Position X de depart
start_y = 125.0  # Position Y de depart
spacing = 19.05  # Espacement entre boutons (0.75 pouces = 19.05 mm)

# Configuration de la grille 3x6 (3 colonnes, 6 rangees verticales)
# Ordre exact de la photo (de gauche a droite, de haut en bas)

# Colonne de gauche (de haut en bas)
col1 = ['B6_23', 'A6_23', 'B5_23', 'A5_23', 'B4_23', 'A4_23']

# Colonne du milieu (de haut en bas)
col2 = ['B3_23', 'A3_23', 'B2_23', 'A2_23', 'B1_23', 'A1_23']

# Colonne de droite (de haut en bas)
col3 = ['B0_23', 'A0_23', 'B7_22', 'A7_22', 'B6_22', 'A6_22']

# Liste de toutes les colonnes
columns = [col1, col2, col3]

# Orientation des boutons (en degres)
button_rotation = 0

def place_button(button_name, x, y, rotation):
    """Fonction pour placer un bouton"""
    footprint = board.FindFootprintByReference(button_name)
    if footprint:
        footprint.SetPosition(pcbnew.VECTOR2I(
            int(x * 1e6),
            int(y * 1e6)
        ))
        footprint.SetOrientationDegrees(rotation)
        print("[OK] {} place a ({:.2f}, {:.2f})".format(button_name, x, y))
        return True
    else:
        print("[ERREUR] {} non trouve".format(button_name))
        return False

# Placer tous les boutons
print("========================================")
print("=== Placement des boutons ===")
print("========================================")

for col_index, column in enumerate(columns):
    print("\n=== Colonne {} ===".format(col_index + 1))
    
    for row_index, button_name in enumerate(column):
        # Calculer la position
        pos_x = start_x + (col_index * spacing)
        pos_y = start_y + (row_index * spacing)
        
        # Placer le bouton
        place_button(button_name, pos_x, pos_y, button_rotation)

pcbnew.Refresh()
print("\n========================================")
print("--- Placement termine ---")
print("========================================")