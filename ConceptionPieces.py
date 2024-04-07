class ConceptionPieces:
    def __init__(self, unite, canvas):
        #Figure creation variables
        self.unite = unite
        self.canvas = canvas
        self.blocks = []
        self.selected_block = None
        self.old_coords = None

    def createRectangle(self, x, y, color):
        #creates a rectangle whose length is determined by the size of the squares on the board 
        return self.canvas.create_rectangle(x*self.unite, y*self.unite, (x+1)*self.unite, (y+1)*self.unite, fill=color)
    
    def conception(self, coords, color):
        #call the rectangle creation function 
        self.blocks = [self.createRectangle(x, y, color) for x, y in coords]

    def generate_blocks(self, playerTurn, nbPlayers, size):
        #defines block colors from a list of available colors 
        colors = {0: "blue", 1: "red", 2: "green", 3: "yellow"}
        #defines the color to be applied to the figure, in relation to the color corresponding to the player whose figure is assigned 
        color = colors[(playerTurn - 1) % len(colors)] 
        
        #defines the shapes of the figures available for each board size 
        availableShapes = {
            1 : ["block"],
            2 : ["block"],
            3 : ["block","G"],
            4 : ["block","G"],
            4 : ["block","G","cross"],
            5 : ["block","G","cross"],
            6 : ["block","G","cross"],
            7 : ["block","G","cross","L"],
            8 : ["block","G","cross","L"],
            9 : ["block","G","cross","L","L2"],
            10 : ["block","G","cross","L","L2"],
            11 : ["block","G","cross","L","L2"],
            12 : ["block","G","cross","L","L2","square"],
            13 : ["block","G","cross","L","L2","square","stick"],
            14 : ["block","G","cross","L","L2","square","stick","T","I"],
            15 : ["block","G","cross","L","L2","square","stick","T","I","J"],
            16 : ["block","G","cross","L","L2","square","stick","T","I","J","Z"],
            17 : ["block","G","cross","L","L2","square","stick","T","I","J","Z","d","C"],
            18 : ["block","G","cross","L","L2","square","stick","T","I","J","Z","d","C","1","InvertedT"],
            19 : ["block","G","cross","L","L2","square","stick","T","I","J","Z","d","C","1","InvertedT","WideL","M"],
            20 : ["block","G","cross","L","L2","square","stick","T","I","J","Z","d","C","1","InvertedT","WideL","M","lightning","4","p","z"]
        }

        #reduces the number of figures per player according to the number of players 
        if int(nbPlayers.get()) > 2 and int(nbPlayers.get()) <= 4:
            availableShapesForSize = availableShapes.get(size - (int(nbPlayers.get()) // 2), [])
        else: 
            availableShapesForSize = availableShapes.get(size, [])

        #defines the shape of each part 
        shapes = {
            "block": [(0, 0)],
            "G": [(0, 0), (1, 0), (2, 0), (2, 1)],
            "cross": [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
            "L": [(0, 0), (0, 1), (0, 2), (1, 2)],
            "L2": [(1, 0), (1, 1), (1, 2), (0, 2)],
            "square": [(0, 0), (0, 1), (1, 0), (1, 1)],
            "stick": [(0, 0), (0, 1), (0, 2), (0, 3)],
            "T": [(0, 0), (1, 0), (2, 0), (1, 1)],
            "I": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
            "J": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3)],
            "Z": [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3)],
            "d": [(1, 0), (0, 1), (1, 1), (0, 2), (1, 2)],
            "C": [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)],
            "1": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1)],
            "InvertedT": [(0, 2), (1, 2), (2, 2), (1, 1), (1, 0)],
            "WideL": [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
            "M": [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)],
            "lightning": [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
            "4": [(0, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
            "p": [(0, 0), (0, 1), (1, 1), (0, 2)],
            "z": [(0, 0), (1, 0), (1, 1), (2, 1)],
        }
        
        #creates a list of figures
        blocks = [] 

        #FOR each figure that can be built 
        for shapeName in availableShapesForSize:
            #Get coordinates of figure shape 
            shapeCoords = shapes[shapeName]
            #create a block with the shape and color
            self.conception(shapeCoords, color)
            #add the block to the list of blocks
            blocks.append(self.blocks)
        #return the list of blocks
        return blocks