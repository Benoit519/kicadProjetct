# -*- coding: utf-8 -*-
import pcbnew

board = pcbnew.GetBoard()

# Plan de masse uniquement sur couche inferieure (Back)
print("========================================")
print("=== Ajout plan de masse (couche Back) ===")
print("========================================")

# Parametres
layer_back = pcbnew.B_Cu
clearance = 0.3  # 0.3mm de clearance
min_thickness = 0.25  # 0.25mm epaisseur minimale

# Trouver le net GND
gnd_net = board.GetNetInfo().GetNetItem("GND")

if gnd_net:
    # Creer la zone (methode correcte pour KiCad 9.0)
    zone = pcbnew.ZONE(board)
    board.Add(zone)
    
    # Configurer la zone
    zone.SetNet(gnd_net)
    zone.SetLayer(layer_back)
    zone.SetLocalClearance(int(clearance * 1e6))
    zone.SetMinThickness(int(min_thickness * 1e6))
    zone.SetIsFilled(False)
    zone.SetZoneName("GND_Plane")
    
    # Obtenir les dimensions du PCB
    outline = board.GetBoardEdgesBoundingBox()
    margin = 0.5  # 0.5mm de marge par rapport au bord
    
    x_min = (outline.GetX() / 1e6) + margin
    y_min = (outline.GetY() / 1e6) + margin
    x_max = ((outline.GetX() + outline.GetWidth()) / 1e6) - margin
    y_max = ((outline.GetY() + outline.GetHeight()) / 1e6) - margin
    
    # Definir le contour rectangulaire
    outline_poly = zone.Outline()
    outline_poly.NewOutline()
    outline_poly.Append(int(x_min * 1e6), int(y_min * 1e6))
    outline_poly.Append(int(x_max * 1e6), int(y_min * 1e6))
    outline_poly.Append(int(x_max * 1e6), int(y_max * 1e6))
    outline_poly.Append(int(x_min * 1e6), int(y_max * 1e6))
    
    print("[OK] Zone GND creee sur couche Back")
    print("    - Clearance: {} mm".format(clearance))
    print("    - Epaisseur min: {} mm".format(min_thickness))
    print("    - Dimensions: {:.1f} x {:.1f} mm".format(x_max - x_min, y_max - y_min))
    
    # Remplir la zone
    filler = pcbnew.ZONE_FILLER(board)
    zones = board.Zones()
    filler.Fill(zones)
    
    pcbnew.Refresh()
    print("[OK] Plan de masse rempli")
    print("\nAppuyez sur F8 dans KiCad pour re-remplir si necessaire")
else:
    print("[ERREUR] Net GND non trouve!")
    print("Verifiez que le net 'GND' existe dans votre schema")

print("========================================")