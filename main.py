import numpy as np

import readSlicedGcode as rsg 

# Split from layers 4 through (n-4)
def splitLayers(layers, numLayers):
    bottom = []
    # Bottom part of the object (4 layers)
    for i in range(4):
        bottom.append(layers[i])

    top = []
    # Top part of the object (4 layers)
    for i in range(numLayers - 4, numLayers):
        top.append(layers[i])

    res1 = []
    res2 = []
    # Layers for the infill
    for i in range(4, numLayers - 4):
        l = layers[i]
        aux = []
        first = True
        for layer in l:
            if first:
                if ";MESH:NONMESH" not in layer:
                    aux.append(layer)
                else:
                    res1.append(aux)
                    aux = []
                    aux.append(layer)
                    first = False
            else:
                if "LAYER" not in layer:
                    aux.append(layer)
                else:
                    res2.append(aux)
                    aux = []
                    aux.append(layer)
                    first = True
        res2.append(aux)
    return bottom, res1, res2, top

# Get a lists of lists containing the [minX, minY, maxX, maxY]
def getPrintingSpace(layers):
    sizeLayers = len(layers)
    spaces = np.empty((sizeLayers, 0)).tolist()
    minimax = []
    for i in range(sizeLayers):
        l = layers[i]
        aux = []
        inner = True
        # Get G commands for the inner layer
        for layer in l:
            if inner:
                if ";TYPE:WALL-OUTER" not in layer:
                    aux.append(layer)
                else:
                    layers[i] = aux
                    inner = False
            else: continue
        # Get values for x and y for the layer
        matching = [s for s in layers[i] if "X" in s]
        x_ = []
        y_ = []
        for match in matching:
            m = match.split( )
            aux_x = [s for s in m if "X" in s]
            aux_y = [s for s in m if "Y" in s]
            x_.append(aux_x[0])
            y_.append(aux_y[0])
        # Get the [minX, minY, maxX, maxY] for each layer
        for i in range(len(x_)):
            x_[i] = float(x_[i].split('X')[1])
            y_[i] = float(y_[i].split('Y')[1])
        res = [min(x_), min(y_), max(x_), max(y_)]
        minimax.append(res)
    return minimax
        


def main():
    filename = "./inGcode/cube_20mm.gcode"
    r = rsg.ReadSlicedGcode(filename)
    r.readFile()
    # print(r.parsed[0])
    header = r.parsed[0]
    headerEnder  = r.parsed[1]
    layers = r.parsed[2]
    numLayers = len(layers)
    eof = r.parsed[3]
    # It returns two list of lists containing the code printed before the infill and after the infill
    bottom, sLayer1, sLayer2, top = splitLayers(layers, numLayers)
    # Get the min and max printing space for each layer
    printSpace = getPrintingSpace(sLayer1)
    print(printSpace)

if __name__ == "__main__":
    main()



    