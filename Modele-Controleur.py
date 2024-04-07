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