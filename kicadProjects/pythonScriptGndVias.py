import pcbnew

board = pcbnew.GetBoard()

GND_NET = "GND"

via_diameter = pcbnew.FromMM(0.6)
drill = pcbnew.FromMM(0.3)

spacing = pcbnew.FromMM(10)

net = board.FindNet(GND_NET)


def is_clear(pos):

    for track in board.GetTracks():
        if track.HitTest(pos):
            return False

    for pad in board.GetPads():
        if pad.HitTest(pos):
            return False

    return True


def place_via(pos):

    via = pcbnew.PCB_VIA(board)

    via.SetPosition(pos)
    via.SetWidth(via_diameter)
    via.SetDrill(drill)

    via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
    via.SetNet(net)

    board.Add(via)


bbox = board.ComputeBoundingBox()

xmin = bbox.GetLeft()
xmax = bbox.GetRight()
ymin = bbox.GetTop()
ymax = bbox.GetBottom()

x = xmin

while x < xmax:

    y = ymin

    while y < ymax:

        pos = pcbnew.VECTOR2I(x, y)

        if is_clear(pos):
            place_via(pos)

        y += spacing

    x += spacing


pcbnew.Refresh()

print("Vias GND places")