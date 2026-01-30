# -*- coding: utf-8 -*-
import pcbnew

board = pcbnew.GetBoard()

print("========================================")
print("=== Ajout vias GND ===")
print("========================================")

# Parametres des vias
via_size = 0.8  # Diametre du via en mm
via_drill = 0.4  # Diametre du trou en mm
offset = 2.0  # Distance du via par rapport au composant en mm

# Trouver le net GND
gnd_net = board.GetNetInfo().GetNetItem("GND")

if not gnd_net:
    print("[ERREUR] Net GND non trouve!")
else:
    via_count = 0
    
    # Liste des composants pour lesquels ajouter des vias
    # MCP23017 (U1, U2, U3, U4...)
    mcp_refs = ['U{}'.format(i) for i in range(1, 10)]
    
    # Condensateurs de decouplage (A0_21_C1, A1_21_C1, etc.)
    cap_refs = []
    for prefix in ['A', 'B']:
        for i in range(8):
            for suffix in ['20', '21', '22', '23']:
                cap_refs.append('{}{}_{}_C1'.format(prefix, i, suffix))
    
    all_refs = mcp_refs + cap_refs
    
    for ref in all_refs:
        footprint = board.FindFootprintByReference(ref)
        
        if footprint:
            # Chercher un pad qui DEVRAIT etre GND (meme s'il n'est pas encore route)
            gnd_pad = None
            
            # Pour les condensateurs, chercher le pad "-" ou "2"
            if '_C1' in ref:
                for pad in footprint.Pads():
                    pad_num = pad.GetNumber()
                    # Les condensateurs ont souvent le pad 2 ou "-" comme GND
                    if pad_num in ['2', '-', 'GND']:
                        gnd_pad = pad
                        break
                # Si pas trouve, prendre le deuxieme pad
                if not gnd_pad and len(list(footprint.Pads())) >= 2:
                    gnd_pad = list(footprint.Pads())[1]
            
            # Pour les MCP23017, chercher les pads VSS
            elif ref.startswith('U'):
                for pad in footprint.Pads():
                    pad_num = pad.GetNumber()
                    # Les MCP23017 ont VSS sur pins 1 et 18 (selon datasheet)
                    if pad_num in ['1', '18', 'VSS', 'GND']:
                        gnd_pad = pad
                        break
            
            # Si on a trouve un pad GND (ou candidat)
            if gnd_pad:
                pos = gnd_pad.GetPosition()
                x = pos.x
                y = pos.y
                
                # Ajouter un via a cote du pad
                via = pcbnew.PCB_VIA(board)
                via.SetPosition(pcbnew.VECTOR2I(x + int(offset * 1e6), y))
                via.SetNet(gnd_net)
                via.SetWidth(int(via_size * 1e6))
                via.SetDrill(int(via_drill * 1e6))
                via.SetViaType(pcbnew.VIATYPE_THROUGH)
                
                board.Add(via)
                via_count += 1
                
                print("[OK] Via GND ajoute pres de {} (pad {})".format(ref, gnd_pad.GetNumber()))
            else:
                # Si aucun pad specifique trouve, ajouter via au centre du composant
                pos = footprint.GetPosition()
                via = pcbnew.PCB_VIA(board)
                via.SetPosition(pcbnew.VECTOR2I(pos.x + int(offset * 1e6), pos.y))
                via.SetNet(gnd_net)
                via.SetWidth(int(via_size * 1e6))
                via.SetDrill(int(via_drill * 1e6))
                via.SetViaType(pcbnew.VIATYPE_THROUGH)
                
                board.Add(via)
                via_count += 1
                
                print("[OK] Via GND ajoute pres de {} (position centrale)".format(ref))
        else:
            print("[INFO] Composant {} non trouve sur le PCB".format(ref))
    
    pcbnew.Refresh()
    print("\n========================================")
    print("Total: {} vias GND ajoutes".format(via_count))
    print("========================================")
    
    if via_count > 0:
        print("\nEtapes suivantes:")
        print("1. Verifiez les vias ajoutes")
        print("2. Routez les connexions GND vers les vias")
        print("3. Appuyez sur F8 pour remplir le plan de masse")