import tkinter
from ConceptionBriques import ConceptionBriques
from Controleur import ControleurInput

class Game:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("Blokus")
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f'{self.screen_width}x{self.screen_height}')
        self.root.resizable(True, True)
        self.canvas_width = self.screen_width * 0.95
        self.canvas_height = self.screen_height * 0.9
        self.playerTurn = 1 
        self.c = 0 
        self.current_figure = None
        self.old = [None, None]
        self.blocks = []
        self.colors = ['red', 'blue', 'green', 'yellow']
        self.canvas = tkinter.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, scrollregion=(0,0,self.canvas_width,self.canvas_height), bg='green')
        self.canvas.place(relx=0.5, rely=0.5, anchor='center')
        self.canvas.pack(expand=True)
        self.controleur = ControleurInput()
        self.controleur.initProperties(self.canvas, self.selectionner)
        self.controleur.input()
        self.gameFieldGenerator()

    def gameFieldGenerator(self):
        # Ваш код для создания окна генератора игрового поля
        self.gameFieldWindow = tkinter.Toplevel(self.root)
        self.gameFieldWindow.title("Game field generator")
        self.gameFieldWindow.geometry("300x200")

        # List of possible board sizes
        boardSizes = [str(i) for i in range(5, 21)]  # 5x5, 6x6, 7x7, ..., 20x20
        self.boardSize = tkinter.StringVar(self.gameFieldWindow)
        self.boardSize.set(boardSizes[0])  # Default value
        boardSizeLabel = tkinter.Label(self.gameFieldWindow, text="Board size:")
        boardSizeLabel.pack()
        boardSizeMenu = tkinter.OptionMenu(self.gameFieldWindow, self.boardSize, *boardSizes)
        boardSizeMenu.pack()

        # Spinbox creation
        numberOfPlayersLabel = tkinter.Label(self.gameFieldWindow, text="Number of players 2-4:")
        numberOfPlayersLabel.pack()
        self.numberOfPlayers = tkinter.Spinbox(self.gameFieldWindow, from_=2, to=4)
        self.numberOfPlayers.pack()

        startButton = tkinter.Button(self.gameFieldWindow, text="Start game", command=self.startGame)
        startButton.pack()
        self.gameFieldWindow.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.gameFieldWindow.attributes("-topmost", True)
        self.gameFieldWindow.mainloop()

    def createGameField(self, size):
        self.size = size
        self.padding = 10  # Add padding
        # Calculate the size of the cell depending on the size of the game field
        self.cell_size = (min(self.canvas_width, self.canvas_height) - 2 * self.padding) // (self.size * 1.5)

        for i in range(self.size):
            self.canvas.create_line(480,110+self.cell_size*i,980,110+self.cell_size*i)
            self.canvas.create_line(480+self.cell_size*i,110,480+self.cell_size*i,600)

        #Coordinates for determine the limits of the grid 
        #For x1 : 480 
        #For y1 : 110 
        #For x2 : 480 + cell_size * size 
        #For y2 : 110 + cell_size * size 
        self.canvas.create_rectangle(480,110,480+self.cell_size*self.size,110+self.cell_size*self.size,outline="blue")

        #Instanciation of blocks
        self.instance = ConceptionBriques(self.cell_size, self.canvas)
        self.blocks = self.instance.generate_blocks(self.playerTurn)
        self.block = []

        # Store the blocks in lists 
        self.gamePiecesPlayer = []

        #Placement of the figures 
        x_offset = 0  # Define x_offset variable
        for player in range(1,int(self.numberOfPlayers.get())):
            player_blocks = self.instance.generate_blocks(player)
            color = self.colors[player % len(self.colors)]  # выберите цвет
            for block in player_blocks:
                for item in block:
                    self.canvas.itemconfig(item, fill=color)  # установите цвет
                    self.canvas.move(item, x_offset, 0)
                self.blocks.append(block)  # Добавьте блок в список
                self.gamePiecesPlayer.append(player_blocks)

    def create_figure(self, cnv, x, y, figure, size=100, fill='red'):
        parts = []
        for dx, dy in figure:
            part = cnv.create_rectangle(x+dx*size, y+dy*size, x+(dx+1)*size, y+(dy+1)*size, fill=fill)
            parts.append(part)
        return parts

    def selectionner(self, event):
        # Ваш код для выбора фигуры
        self.c = (self.c + 1) % 2
        if self.c == 1:
            self.item = self.canvas.find_closest(event.x, event.y)
            self.current_figure = next((block for block in self.blocks if self.item[0] in block), None)  
            if self.current_figure is not None:
                x1, y1, x2, y2 = self.canvas.coords(self.current_figure[0])
                self.original_coords = (x1, y1)
                self.current_figure_pattern = [(x1-x, y1-y) for x, y in [(self.canvas.coords(item)[0], self.canvas.coords(item)[1]) for item in self.current_figure]]  # сохраняем шаблон текущей фигуры
            self.old[0] = event.x
            self.old[1] = event.y
            self.canvas.bind("<Motion>",self.glisser)
        else:
            self.old[0] = None
            self.old[1] = None
            self.canvas.unbind("<Motion>")
            self.deposer(event.x,event.y)

    def deposer(self, x, y):
        # Ваш код для размещения фигуры на игровом поле
        if self.current_figure is not None:
            for item in self.current_figure:
                x1, y1, x2, y2 = self.canvas.coords(item)
                # Выравниваем координаты по сетке
                x = round(x1 / self.cell_size) * self.cell_size
                y = round(y1 / self.cell_size) * self.cell_size
                if self.is_in_grid(x, y):
                    # Удаляем старую фигуру
                    self.canvas.delete(item)
                    # Создаем новую фигуру на игровом поле
                    self.current_figure = self.create_figure(self.canvas, x, y, self.current_figure_pattern, self.cell_size)
                else:
                    # Возвращаем фигуру на исходное место
                    x1, y1, x2, y2 = self.canvas.coords(self.current_figure[0])
                    for part in self.current_figure:
                        self.canvas.move(part, self.original_coords[0] - x1, self.original_coords[1] - y1)

    def glisser(self, event):
        # Ваш код для перемещения фигуры
        if self.current_figure is not None:
            for item in self.current_figure:
                self.canvas.move(item, event.x-self.old[0], event.y-self.old[1])
            self.old[0]=event.x
            self.old[1]=event.y

    def is_in_grid(self, x, y):
        return 480 <= x <= 480 + self.cell_size * self.size and 110 <= y <= 110 + self.cell_size * self.size

    def selectionner(self, event):
        # Ваш код для выбора фигуры
        self.c = (self.c + 1) % 2
        if self.c == 1:
            self.item = self.canvas.find_closest(event.x, event.y)
            self.current_figure = next((block for block in self.blocks if self.item[0] in block), None)  
            if self.current_figure is not None:
                x1, y1, x2, y2 = self.canvas.coords(self.current_figure[0])
                self.original_coords = (x1, y1)
                self.current_figure_pattern = [(x1-x, y1-y) for x, y in [(self.canvas.coords(item)[0], self.canvas.coords(item)[1]) for item in self.current_figure]]  # сохраняем шаблон текущей фигуры
            self.old[0] = event.x
            self.old[1] = event.y
            self.canvas.bind("<Motion>",self.glisser)
        else:
            self.old[0] = None
            self.old[1] = None
            self.canvas.unbind("<Motion>")
            self.deposer(event.x,event.y)

    def startGame(self):
        # Ваш код для начала игры
        # Getting the size of the game field and the number of players from the game field generator window
        self.size = int(self.boardSize.get())
        self.players = int(self.numberOfPlayers.get())
        
        # Close the game field generator window
        self.gameFieldWindow.withdraw()

        # Set the main window to the top level
        self.root.attributes('-topmost', True)

        # Create the game field
        self.createGameField(self.size)

    def run(self):
        self.root.mainloop()

game = Game()
game.run()


# Path: ConceptionBriques.py
# class ConceptionBriques:
#     def __init__(self, unite, canvas):
#         self.unite = unite
#         self.canvas = canvas
#         self.blocks = []
#         self.selected_block = None
#         self.old_coords = None
#         self.canMovePiece = None 

#     def createRectangle(self, x, y, color):
#         return self.canvas.create_rectangle(x*self.unite, y*self.unite, (x+1)*self.unite, (y+1)*self.unite, fill=color)

#     def conception(self, coords,color):
#         self.blocks = [self.createRectangle(x, y, color) for x, y in coords]

#     def generate_blocks(self, playerTurn):
#         colors = {0: "blue", 1: "red", 2: "green", 3: "yellow"} # Define the colors of the blocks
#         color = colors[playerTurn] # Define the color of the blocks

#         # Define the shapes of the blocks
#         shapes = {
#             "G": [(0, 0), (1, 0), (2, 0), (2, 1)], 
#             #"cross": [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
#             #"L": [(0, 0), (0, 1), (0, 2), (1, 2)],
#             #"L2": [(1, 0), (1, 1), (1, 2), (0, 2)],
#             #"square": [(0, 0), (0, 1), (1, 0), (1, 1)],
#             #"stick": [(0, 0), (0, 1), (0, 2), (0, 3)],
#             #"T": [(0, 0), (1, 0), (2, 0), (1, 1)]
#         }
        
#         blocks = [] # Create a list of blocks
#         for shape in shapes.values():  # for each shape
#             self.conception(shape, color) # Create a block
#             blocks.append(self.blocks) # Add the block to the list of blocks
#         return blocks # Return the list of blocks
    
#     def generateGameBoardPieces(self):
#         block = []
#         shape = {"GBP" : [(0, 0), (0, 1), (1, 0), (1, 1)]}
#         for s in shape.values():
#             self.conception(s, "white")
#             block.append(self.blocks)
#         return block 


# Path: Controleur.py
# class ControleurInput():
#     def __init__(self):
#         self.canvas = None
#         self.selectionFigure = None 

#     def initProperties(self, canvas, fonctionSelection):
#         self.canvas = canvas
#         self.selectionFigure = fonctionSelection 
        
#     def input(self):
#         if self.canvas:
#             self.canvas.bind("<Button-1>", self.selectionFigure)