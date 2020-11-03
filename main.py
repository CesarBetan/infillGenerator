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
    print(top)
    print(len(top))

if __name__ == "__main__":
    main()



    