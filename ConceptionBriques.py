class ConceptionBriques:
    def __init__(self, unite, canvas):
        self.unite = unite
        self.canvas = canvas
        self.blocks = []
        self.selected_block = None
        self.old_coords = None

    def createRectangle(self, x, y, color):
        return self.canvas.create_rectangle(x*self.unite, y*self.unite, (x+1)*self.unite, (y+1)*self.unite, fill=color)
    
    def conception(self, coords, color):
        self.blocks = [self.createRectangle(x, y, color) for x, y in coords]

    def generate_blocks(self, playerTurn, size):
        colors = {0: "blue", 1: "red", 2: "green", 3: "yellow"} # Define the colors of the blocks
        color = colors[(playerTurn - 1) % len(colors)]  # Define the color of the blocks

        # Define the shapes of the blocks available for different grid sizes
        available_shapes = {
            5: ["square","stick"],
            12 : ["square","stick","L","cross","T", "block"],
            20 : ["square","stick","L","cross","T", "block"]
            # Add more grid sizes and corresponding available shapes as needed
        }

        # Get the available shapes based on the size of the grid
        available_shapes_for_size = available_shapes.get(size, [])

        # Define the shapes of the blocks
        shapes = {
            "block": [(0, 0)],
            "G": [(0, 0), (1, 0), (2, 0), (2, 1)],
            "cross": [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
            "L": [(0, 0), (0, 1), (0, 2), (1, 2)],
            "L2": [(1, 0), (1, 1), (1, 2), (0, 2)],
            "square": [(0, 0), (0, 1), (1, 0), (1, 1)],
            "stick": [(0, 0), (0, 1), (0, 2), (0, 3)],
            "T": [(0, 0), (1, 0), (2, 0), (1, 1)]
        }

        blocks = []  # Create a list of blocks
        for shape_name in available_shapes_for_size:  # Iterate over available shapes for the grid size
            shape_coords = shapes[shape_name]  # Get the coordinates for the shape
            self.conception(shape_coords, color)  # Create a block
            blocks.append(self.blocks)  # Add the block to the list of blocks
        return blocks  # Return the list of blocks