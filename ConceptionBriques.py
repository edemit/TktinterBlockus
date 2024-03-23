class ConceptionBriques:
    def __init__(self, unite, canvas):
        self.unite = unite
        self.canvas = canvas
        self.blocks = []
        self.selected_block = None
        self.old_coords = None
        self.canMovePiece = None 

    def createRectangle(self, x, y, color):
        return self.canvas.create_rectangle(x*self.unite, y*self.unite, (x+1)*self.unite, (y+1)*self.unite, fill=color)

    def conception(self, coords,color):
        self.blocks = [self.createRectangle(x, y, color) for x, y in coords]

    def generate_blocks(self, playerTurn):
        colors = {0: "blue", 1: "red", 2: "green", 3: "yellow"} # Define the colors of the blocks
        color = colors[(playerTurn - 1) % len(colors)]  # Define the color of the blocks

        # Define the shapes of the blocks
        shapes = {
            "G": [(0, 0), (1, 0), (2, 0), (2, 1)], 
            #"cross": [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
            #"L": [(0, 0), (0, 1), (0, 2), (1, 2)],
            #"L2": [(1, 0), (1, 1), (1, 2), (0, 2)],
            #"square": [(0, 0), (0, 1), (1, 0), (1, 1)],
            #"stick": [(0, 0), (0, 1), (0, 2), (0, 3)],
            #"T": [(0, 0), (1, 0), (2, 0), (1, 1)]
        }
        
        blocks = [] # Create a list of blocks
        for shape in shapes.values():  # for each shape
            self.conception(shape, color) # Create a block
            blocks.append(self.blocks) # Add the block to the list of blocks
        return blocks # Return the list of blocks
    
    def generateGameBoardPieces(self):
        block = []
        shape = {"GBP" : [(0, 0), (0, 1), (1, 0), (1, 1)]}
        for s in shape.values():
            self.conception(s, "white")
            block.append(self.blocks)
        return block 