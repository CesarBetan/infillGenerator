import readSlicedGcode as rsg 

def main():
    filename = "./inGcode/cube_20mm.gcode"
    r = rsg.ReadSlicedGcode(filename)
    r.readFile()
    # print(r.parsed[0])
    r.splitLayers()

if __name__ == "__main__":
    main()



    