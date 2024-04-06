import tkinter
from tkinter import *  
from Vue import Interface

class ControleurInput():
    def __init__(self):
        #Main 
        self.root = tkinter.Tk()
        self.root.title("Blokus")
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f'{self.screen_width}x{self.screen_height}')
        self.root.resizable(True, True)
        self.playerTurn = 0
        self.points = [0,0,0,0]
        self.c = 0 
        self.current_figure = None
        self.old = [None, None]
        self.blocks = []
        self.available_coords = None  # Initialize available coordinates
        #Vue 
        self.vueScript = Interface()
        self.canvas_width = self.screen_width * 0.95
        self.canvas_height = self.screen_height * 0.9 
        self.colors = ['red', 'blue', 'green', 'yellow']
        self.canvas = tkinter.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, scrollregion=(0,0,self.canvas_width,self.canvas_height), bg='white')
        self.canvas.place(relx=0.5, rely=0.5, anchor='center')
        self.canvas.pack(expand=True)
        self.player1ScoreLabel = tkinter.Label(self.root, text="Score joueur 1 : ", font=("Arial", 15))
        self.player2ScoreLabel = tkinter.Label(self.root, text="Score joueur 2 : ", font=("Arial", 15))
        self.player3ScoreLabel = tkinter.Label(self.root, text="Score joueur 3 : ", font=("Arial", 15))
        self.player4ScoreLabel = tkinter.Label(self.root, text="Score joueur 4 : ", font=("Arial", 15))
        self.playersScoreLabels = [self.player1ScoreLabel, self.player2ScoreLabel, self.player3ScoreLabel, self.player4ScoreLabel]
        self.player1ScoreText = tkinter.StringVar(self.root, self.points[0])
        self.player2ScoreText = tkinter.StringVar(self.root, self.points[1])
        self.player3ScoreText = tkinter.StringVar(self.root, self.points[2])
        self.player4ScoreText = tkinter.StringVar(self.root, self.points[3])
        self.playerScoreText = [self.player1ScoreText, self.player2ScoreText, self.player3ScoreText, self.player4ScoreText]
        self.player1ScoreLabelText = tkinter.Label(self.root, textvariable=self.player1ScoreText, font=("Arial", 15))
        self.player2ScoreLabelText = tkinter.Label(self.root, textvariable=self.player2ScoreText, font=("Arial", 15))
        self.player3ScoreLabelText = tkinter.Label(self.root, textvariable=self.player3ScoreText, font=("Arial", 15))
        self.player4ScoreLabelText = tkinter.Label(self.root, textvariable=self.player4ScoreText, font=("Arial", 15))
        self.playersScoreLabelsTexts = [self.player1ScoreLabelText, self.player2ScoreLabelText, self.player3ScoreLabelText, self.player4ScoreLabelText]

        #Controleur 
        self.input() 
        self.gameFieldGenerator()

    def input(self):
        if self.canvas:
            self.canvas.bind("<Button-1>", self.selectionner)
            
    def selectionner(self, event):
        self.c = (self.c + 1) % 2
        if self.c == 1:
            item = self.canvas.find_closest(event.x, event.y)
            currentColor =self.colors[self.playerTurn % len(self.colors)]
            print(currentColor, end=" ")
            itemColor = self.canvas.itemcget(item, "fill")
            print(itemColor)
            if itemColor == currentColor:
                self.current_figure = next((block for block in self.blocks if item[0] in block), None)  
                if self.current_figure is not None:
                    x1, y1, x2, y2 = self.canvas.coords(self.current_figure[0])
                    self.original_coords = (x1, y1)
                    self.current_figure_pattern = [(x1-x, y1-y) for x, y in [(self.canvas.coords(item)[0], self.canvas.coords(item)[1]) for item in self.current_figure]]
                self.old[0] = event.x
                self.old[1] = event.y
                self.canvas.bind("<Motion>",self.glisser)
            else:
                print("This is not your turn")
                self.c = 0
        else: 
            self.old[0] = None
            self.old[1] = None
            self.canvas.unbind("<Motion>")
            self.deposer(event.x,event.y)

    def deposer(self, x, y):
        if self.current_figure is not None:
            # Calculate the new coordinates of the figure based on the grid
            new_figure = []
            for item in self.current_figure:
                x1, y1, x2, y2 = self.canvas.coords(item)
                x = (round((x1 - self.vueScript.x_start) / self.vueScript.cell_size) * self.vueScript.cell_size) + self.vueScript.x_start
                y = (round((y1 - self.vueScript.y_start) / self.vueScript.cell_size) * self.vueScript.cell_size) + self.vueScript.y_start
                new_figure.append((x, y))
            # Check if the figure can be placed on the board
            if all(self.is_in_grid(x, y) for x, y in new_figure) and (x, y) in self.available_coords[self.playerTurn]:
                for item in self.current_figure:
                    #Update score 
                    self.points[self.playerTurn] += 1 
                    self.playerScoreText[self.playerTurn].set(self.points[self.playerTurn])
                    
                    #Delete the figure from the list of blocks
                    self.canvas.delete(item)
                # Create a new figure
                self.current_figure = [self.vueScript.create_figure(self.canvas, x, y, self.vueScript.cell_size, self.current_figure_pattern, self.colors, self.playerTurn, fill=None) for x, y in new_figure]
                for figure in self.current_figure:
                    self.vueScript.deposeFigure(figure, self.canvas, self.playerTurn)
                #  Change the player's turn
                self.playerTurn = (self.playerTurn + 1) % int(self.numberOfPlayers.get())
                self.update_available_coords()
            else:
                # Move the figure back to its original position
                x1, y1, x2, y2 = self.canvas.coords(self.current_figure[0])
                for part in self.current_figure:
                    self.canvas.move(part, self.original_coords[0] - x1, self.original_coords[1] - y1)
                self.vueScript.displayScore(self.canvas, self.playersScoreLabels[:self.players], self.playersScoreLabelsTexts[:self.players], self.screen_width, self.screen_height, True) 
            self.check_end_game()

    def glisser(self, event):
        if self.current_figure is not None:
            for item in self.current_figure:
                self.canvas.move(item, event.x-self.old[0], event.y-self.old[1])
            self.old[0]=event.x
            self.old[1]=event.y

    def is_in_grid(self, x, y):
        for item in self.current_figure:
            x1, y1, x2, y2 = self.canvas.coords(item)
            x1 = round((x1 - self.vueScript.x_start) / self.vueScript.cell_size)
            y1 = round((y1 - self.vueScript.y_start) / self.vueScript.cell_size)
            # check if the figure is in the grid
            if not (0 <= y1 < len(self.vueScript.board) and 0 <= x1 < len(self.vueScript.board[0])):
                return False
            # check if the cell is empty
            if self.vueScript.board[y1][x1] != -1:
                return False
        return True
    
    def update_available_coords(self):
        # Remove used coordinates
        for i, coords in enumerate(self.available_coords[self.playerTurn]):
            if self.vueScript.board[coords[1]][coords[0]] != -1:
                del self.available_coords[self.playerTurn][i]
        
         # Add new available coordinates
        for item in self.current_figure:
            x1, y1, x2, y2 = self.canvas.coords(item)
            x1 = round((x1 - self.vueScript.x_start) / self.vueScript.cell_size)
            y1 = round((y1 - self.vueScript.y_start) / self.vueScript.cell_size)
            new_coords = [(x1-1, y1-1), (x1+1, y1-1), (x1-1, y1+1), (x1+1, y1+1)]
            self.available_coords[self.playerTurn].extend(new_coords)

    def check_end_game(self):
        if not any(self.available_coords):
            self.end_game()

    def end_game(self):
        end_game_window = tkinter.Toplevel(self.root)
        end_game_window.title("Game Over")
        end_game_window.geometry("200x100")
        tkinter.Label(end_game_window, text="Game Over!").pack()
        tkinter.Button(end_game_window, text="Relaunch", command=self.relaunchGame).pack()
        tkinter.Button(end_game_window, text="OK", command=end_game_window.destroy).pack()
    
    # Relaunch the game
    def relaunchGame(self):
        self.playerTurn = 0 
        self.points = [0,0,0,0]
        self.gameFieldGenerator()

    def gameFieldGenerator(self):
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

    def startGame(self):
        # Getting the size of the game field and the number of players from the game field generator window
        self.size = int(self.boardSize.get())
        self.players = int(self.numberOfPlayers.get())

        # Initialize available coordinates after size is defined
        self.available_coords = [[(0, 0), (0, self.size-1), (self.size-1, 0), (self.size-1, self.size-1)] for _ in range(4)]

        # Close the game field generator window
        self.gameFieldWindow.withdraw()

        # Set the main window to the top level
        self.root.attributes('-topmost', True)

        #Create the game field 
        self.vueScript.createGameField(self.size,self.canvas,self.canvas_width,self.canvas_height,self.numberOfPlayers,self.colors,self.screen_width,self.screen_height,self.blocks)

        self.vueScript.displayScore(self.canvas, self.playersScoreLabels[:self.players], self.playersScoreLabelsTexts[:self.players], self.screen_width, self.screen_height, False) 

    def run(self):
        self.root.mainloop()

controleur = ControleurInput()
controleur.run()   


# Path: Vue.py
# import tkinter
# from ConceptionBriques import ConceptionBriques 

# class Interface():
#     def createGameField(self, size, canvas, canvasWidth, canvasHeight, nbPlayers, colors, screenWidth, screenHeight, blocks):
#         self.size = size
#         self.board = [[-1 for _ in range(size)] for _ in range(size)]  # Create a game field
#         self.padding = 10  # Add padding
#         # Calculate the size of the cell depending on the size of the game field
#         self.cell_size = (min(canvasWidth, canvasHeight) - 2 * self.padding) // (self.size * 1.5)

#         # Calculate relative coordinates for the game field
#         self.x_start = (canvasWidth - self.cell_size * self.size) / 2
#         self.y_start = (canvasHeight - self.cell_size * self.size) / 2
#         self.x_end = self.x_start + self.cell_size * self.size
#         self.y_end = self.y_start + self.cell_size * self.size

#         for i in range(self.size+1):
#             y_pos = self.y_start + self.cell_size * i
#             canvas.create_line(self.x_start, y_pos, self.x_end, y_pos)

#             x_pos = self.x_start + self.cell_size * i
#             canvas.create_line(x_pos, self.y_start, x_pos, self.y_end)

#         #Instanciation of blocks
#         self.instance = ConceptionBriques(self.cell_size, canvas)

#         # Store the blocks in lists 
#         self.gamePiecesPlayer = []
        
#         #Placement of the figures 
#         x_offset = 0  # Define x_offset variable
#         y_offset = 0 #Define y_offset variable 
#         placementLimit = 0 #Define the border for each zone
#         for player in range(1, int(nbPlayers.get()) + 1):
#             player_blocks = self.instance.generate_blocks(player, nbPlayers, size)
#             color = colors[(player - 1) % len(colors)] 

#             player_offsets = [
#                 (0, 0, screenWidth/4),  # player 1
#                 (screenWidth/1.5, 0, screenWidth/1.2),  # player 2
#                 (0, screenHeight/2, screenWidth/4),  # player 3
#                 (screenWidth/1.5, screenHeight/2, screenWidth/1.2)  # player 4
#             ]

#             x_offset, y_offset, placementLimit = player_offsets[player-1]

#             for block in player_blocks:
#                 for item in block:
#                     canvas.itemconfig(item, fill=color) 
                    
#                     if int(nbPlayers.get()) == 2:
#                         if player == 1 and x_offset > placementLimit:
#                             x_offset = 0
#                             y_offset += self.cell_size * 5
#                         if player == 2 and x_offset > placementLimit:
#                             x_offset = screenWidth/1.5
#                             y_offset += self.cell_size * 5

#                     if int(nbPlayers.get()) >= 3 and int(nbPlayers.get()) <= 5: 
#                         if player == 1 or player == 3:
#                             if x_offset > placementLimit:
#                                 x_offset = 0
#                                 y_offset += self.cell_size * 5
#                         if player == 2 or player == 4:
#                             if x_offset > placementLimit:
#                                 x_offset = screenWidth/1.5
#                                 y_offset += self.cell_size * 5 

#                     canvas.move(item, x_offset, y_offset)
#                 blocks.append(block)
#                 self.gamePiecesPlayer.append(player_blocks)
#                 self.gamePiecesPlayer.append(player_blocks) 
#                 x_offset += self.cell_size * 3
#             x_offset = 0
#             y_offset = 0

#     def create_figure(self, canvas, x, y, size, figure, colors, playerTurn, fill=None):
#         if fill is None:
#             fill = colors[playerTurn % len(colors)]
#         parts = []
#         for dx, dy in figure:
#             part = canvas.create_rectangle(x+dx*size, y+dy*size, x+(dx+1)*size, y+(dy+1)*size, fill=fill)
#             parts.append(part)
#         return parts
    
#     def deposeFigure(self, figure, canvas, playerTurn):
#         # Fill the board with the current player's number
#         for item in figure: 
#             x1, y1, x2, y2 = canvas.coords(item)
#             x1 = round((x1 - self.x_start) / self.cell_size)
#             y1 = round((y1 - self.y_start) / self.cell_size)
#             # check if the figure is in the grid
#             if not (0 <= y1 < len(self.board) and 0 <= x1 < len(self.board[0])):
#                 return False
#             # check if the cell is empty
#             if self.board[y1][x1] != -1:
#                 return False
#             self.board[y1][x1] = playerTurn 
            
#     def displayScore(self, canvas, playersScoreLabels, playersScoreLabelsTexts, screenWidth, screenHeight, onlyUpdateDisplay):
#         x = screenWidth/2.8
#         y = screenHeight/1.25 
#         for i in range(0,len(playersScoreLabels)):
#             if onlyUpdateDisplay == False:
#                 canvas.create_window(x,y,window=playersScoreLabels[i])
#             x += screenWidth/14
#             canvas.create_window(x,y,window=playersScoreLabelsTexts[i])
#             x -= screenWidth/14 

#             if i == 0 or i == 2:
#                 y += screenHeight/12.5
#             elif i == 1 or i == 3:
#                 x += screenWidth/6 
#                 y = screenHeight/1.25  


# Path: ConceptionBriques.py
# class ConceptionBriques:
#     def __init__(self, unite, canvas):
#         self.unite = unite
#         self.canvas = canvas
#         self.blocks = []
#         self.selected_block = None
#         self.old_coords = None

#     def createRectangle(self, x, y, color):
#         return self.canvas.create_rectangle(x*self.unite, y*self.unite, (x+1)*self.unite, (y+1)*self.unite, fill=color)
    
#     def conception(self, coords, color):
#         self.blocks = [self.createRectangle(x, y, color) for x, y in coords]

#     def generate_blocks(self, playerTurn, nbPlayers, size):
#         colors = {0: "blue", 1: "red", 2: "green", 3: "yellow"} # Define the colors of the blocks
#         color = colors[(playerTurn - 1) % len(colors)]  # Define the color of the blocks

#         # Define the shapes of the blocks available for different grid sizes
#         availableShapes = {
#             5: ["square","stick"],
#             6: ["square","stick"],
#             7: ["square","stick","L"],
#             8: ["square","stick","L"],
#             9: ["square","stick","L","cross"],
#             10: ["square","stick","L","cross"],
#             11: ["square","stick","L","cross","T"],
#             12 : ["square","stick","L","cross","T"],
#             13 : ["square","stick","L","cross","T","block"],
#             14 : ["square","stick","L","cross","T","block"],
#             15 : ["square","stick","L","cross","T","block","G"],
#             16 : ["square","stick","L","cross","T","block","G"],
#             17 : ["square","stick","L","cross","T","block","G","L2"],
#             18 : ["square","stick","L","cross","T","block","G","L2"],
#             19 : ["square","stick","L","cross","T","block","G","L2"],
#             20 : ["square","stick","L","cross","T", "block","G","L2"]
#             # Add more grid sizes and corresponding available shapes as needed
#         }

#         # Get the available shapes based on the size of the grid
#         if int(nbPlayers.get()) > 2 and int(nbPlayers.get()) <= 4:
#             availableShapesForSize = availableShapes.get(size - (int(nbPlayers.get())-2), [])
#             print(int(nbPlayers.get())-2)
#         else: 
#             availableShapesForSize = availableShapes.get(size, [])

#         # Define the shapes of the blocks
#         shapes = {
#             "block": [(0, 0)],
#             "G": [(0, 0), (1, 0), (2, 0), (2, 1)],
#             "cross": [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
#             "L": [(0, 0), (0, 1), (0, 2), (1, 2)],
#             "L2": [(1, 0), (1, 1), (1, 2), (0, 2)],
#             "square": [(0, 0), (0, 1), (1, 0), (1, 1)],
#             "stick": [(0, 0), (0, 1), (0, 2), (0, 3)],
#             "T": [(0, 0), (1, 0), (2, 0), (1, 1)]
#         }

#         blocks = []  # Create a list of blocks
#         for shapeName in availableShapesForSize:  # Iterate over available shapes for the grid size
#             shapeCoords = shapes[shapeName]  # Get the coordinates for the shape
#             self.conception(shapeCoords, color)  # Create a block
#             blocks.append(self.blocks)  # Add the block to the list of blocks
#         return blocks  # Return the list of blocks