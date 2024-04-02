import tkinter 
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
        #Vue 
        self.vueScript = Interface()
        self.canvas_width = self.screen_width * 0.95
        self.canvas_height = self.screen_height * 0.9 
        self.colors = ['red', 'blue', 'green', 'yellow']
        self.canvas = tkinter.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, scrollregion=(0,0,self.canvas_width,self.canvas_height), bg='green')
        self.canvas.place(relx=0.5, rely=0.5, anchor='center')
        self.canvas.pack(expand=True)
        #Controleur 
        self.input()
        self.gameFieldGenerator()  

    def input(self):
        if self.canvas:
            self.canvas.bind("<Button-1>", self.selectionner)
            
    def selectionner(self, event):
        # Ваш код для выбора фигуры
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
                    self.current_figure_pattern = [(x1-x, y1-y) for x, y in [(self.canvas.coords(item)[0], self.canvas.coords(item)[1]) for item in self.current_figure]]  # сохраняем шаблон текущей фигуры
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
        # Ваш код для размещения фигуры на игровом поле
        if self.current_figure is not None:
            for item in self.current_figure:
                x1, y1, x2, y2 = self.canvas.coords(item)
                # Выравниваем координаты по сетке
                x = round((x1 - self.vueScript.x_start) / self.vueScript.cell_size) * self.vueScript.cell_size + self.vueScript.x_start
                y = round((y1 - self.vueScript.y_start) / self.vueScript.cell_size) * self.vueScript.cell_size + self.vueScript.y_start
                if self.is_in_grid(x, y):
                    self.points[self.playerTurn] += 1
                    print(self.playerTurn, " : ", self.points[self.playerTurn])
                    # Delete the figure from the list of blocks
                    self.canvas.delete(item)
                    # Create a new figure
                    self.current_figure = self.vueScript.create_figure(self.canvas, x, y, self.size, self.current_figure_pattern, self.colors, self.playerTurn, fill=None)
                    self.vueScript.deposeFigure(self.current_figure, self.canvas, self.playerTurn)
                print(self.vueScript.board)
        else:
            # Возвращаем фигуру на исходное место
            x1, y1, x2, y2 = self.canvas.coords(self.current_figure[0])
            for part in self.current_figure:
                self.canvas.move(part, self.original_coords[0] - x1, self.original_coords[1] - y1)
        # Переходим к следующему игроку
        self.playerTurn = (self.playerTurn + 1) % int(self.numberOfPlayers.get())

    def glisser(self, event):
        # Ваш код для перемещения фигуры
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
            if 0 <= y1 < len(self.vueScript.board) and 0 <= x1 < len(self.vueScript.board[0]) and self.vueScript.board[y1][x1] != -1:
                return False
        return True  
    
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

    def startGame(self):
        # Ваш код для начала игры
        # Getting the size of the game field and the number of players from the game field generator window
        self.size = int(self.boardSize.get())
        self.players = int(self.numberOfPlayers.get())

        # Close the game field generator window
        self.gameFieldWindow.withdraw()

        # Set the main window to the top level
        self.root.attributes('-topmost', True)

        #Create the game field 
        self.vueScript.createGameField(self.size,self.canvas,self.canvas_width,self.canvas_height,self.numberOfPlayers,self.colors,self.screen_width,self.screen_height,self.blocks)

    def run(self):
        self.root.mainloop()
        
controleur = ControleurInput()
controleur.run()   