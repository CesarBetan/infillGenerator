

class ReadSlicedGcode():
    
    def __init__(self, fname):
        self.fname = fname
        self.parsed = []


    def readFile(self):
        stage = []
        layers = []
        stages = 4 * [True]
        with open(self.fname, 'r') as filehandle:
            for line in filehandle:
                # First case: Header
                if stages[0]:
                    if "; Ender 3 Custom Start G-code" not in str(line):
                        stage.append(str(line))
                    else:
                        stages[0] = False
                        self.parsed.append(stage)
                        stage = []
                        stage.append(str(line))
                # Second case: Ender 3 header
                elif stages[1]:
                    if ";LAYER:0" not in str(line):
                        stage.append(str(line))
                    else:
                        stages[1] = False
                        self.parsed.append(stage)
                        stage = []
                        stage.append(str(line))
                # Third case: Layers
                elif stages[2]:
                    if "G91 ;Relative positioning" not in str(line):
                        if "LAYER" not in str(line):
                            stage.append(str(line))
                        else:
                            layers.append(stage)
                            stage = []
                            stage.append(str(line))
                    else:
                        stages[2] = False
                        layers.append(stage)
                        self.parsed.append(layers)
                        stage = []
                        stage.append(str(line))
                # Third case: End of file
                elif stages[3]:
                    stage.append(str(line))
            self.parsed.append(stage)

    # Split from layers 4 through (n-4)
    def splitLayers(self):
        layers = self.parsed[2]
        numLayers = len(layers)
        res = []
        for i in range(4, numLayers - 4):
            print(i)      
