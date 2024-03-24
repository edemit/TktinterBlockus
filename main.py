from tkinter import Tk, Canvas

def create_figure(cnv, x, y, figure, size=100, fill='red'):
    # Создаем части фигуры в соответствии с переданным шаблоном
    parts = []
    for dx, dy in figure:
        part = cnv.create_rectangle(x+dx*size, y+dy*size, x+(dx+1)*size, y+(dy+1)*size, fill=fill)
        parts.append(part)
    # Возвращаем части фигуры как список
    return parts

def clic(event):
    global c
    c = (c+1)%2
    if ( c == 1):
        cnv.bind("<Motion>",glisser)
        old[0]=event.x
        old[1]=event.y
    else:
        cnv.unbind("<Motion>")
        deposer(event.x,event.y)

def glisser(event):
    for part in current_figure:
        x1, y1, x2, y2 = cnv.coords(part)
        if (old[0] >= x1 and old[0] <= x2 and old[1] >= y1 and old[1] <= y2):
            cnv.move(part, event.x-old[0], event.y-old[1])
    old[0]=event.x
    old[1]=event.y

def deposer(x,y):
    # Получаем координаты первой части фигуры
    x1, y1, x2, y2 = cnv.coords(current_figure[0])
    # Вычисляем смещение
    dx = x - x1
    dy = y - y1
    # Перемещаем все части фигуры
    for part in current_figure:
        cnv.move(part, dx, dy)
    # Создаем новую фигуру после размещения старой
    current_figure = create_figure(cnv, 620, 30, current_figure_pattern)

# pgm principal

old=[None, None]
global c
c = 0
root = Tk()
cnv = Canvas(root, width=800, height=650)
cnv.pack()

tetris_g_figure = [(0, 0), (0, 1), (1, 1), (2, 1)]  # Фигура "Г"
tetris_i_figure = [(0, 0), (0, 1), (0, 2), (0, 3)]  # Фигура "I"

current_figure_pattern = tetris_g_figure
current_figure = create_figure(cnv, 620, 30, current_figure_pattern)

for i in range(7):
    cnv.create_line(5,5+100*i,605,5+100*i)
    cnv.create_line(5+100*i,5,5+100*i,605)

cnv.bind("<Button-1>",clic)

<<<<<<< Updated upstream
root.mainloop()
=======
        # Store the blocks in lists 
        self.gamePiecesPlayer = []

        #Placement of the figures 
        x_offset = 0  # Define x_offset variable
        y_offset = 0 #Define y_offset variable
        for player in range(1,int(self.numberOfPlayers.get())):
            player_blocks = self.instance.generate_blocks(player,size)
            color = self.colors[player % len(self.colors)]  # выберите цвет

            if player == 0:
                x_offset = 0
                y_offset = 0
            if player == 1:
                x_offset = self.screen_width/1.5
                y_offset = 0
            if player == 2:
                x_offset = 0
                y_offset = self.screen_height/2
            if player == 3:
                x_offset = self.screen_width/1.5
                y_offset = self.screen_height/2

            placementLimit0And2 = self.screen_width/4.5
            placementLimit1And3 = self.screen_width/1.2

            for block in player_blocks:
                for item in block:
                    self.canvas.itemconfig(item, fill=color)  # установите цвет
                    
                    if int(self.numberOfPlayers.get()) <= 2:
                        if player == 0 and x_offset > placementLimit0And2:
                            x_offset = 0
                            y_offset += item + self.cell_size * 3
                        if player == 1 and x_offset > placementLimit1And3:
                            x_offset = self.screen_width/1.5
                            y_offset += item + self.cell_size * 3 

                    if int(self.numberOfPlayers.get()) > 2 and int(self.numberOfPlayers.get()) <= 4: 
                        if player == 0 or player == 2:
                            if x_offset > placementLimit0And2:
                                x_offset = 0
                                y_offset += item + self.cell_size * 3
                        if player == 1 or player == 3:
                            if x_offset > placementLimit1And3:
                                x_offset = self.screen_width/1.5
                                y_offset += item + self.cell_size * 3

                    self.canvas.move(item, x_offset, y_offset)
                self.blocks.append(block)  # Добавьте блок в список
                self.gamePiecesPlayer.append(player_blocks)
                x_offset += self.cell_size * 3
            x_offset = 0

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
                x = round((x1 - self.x_start) / self.cell_size) * self.cell_size + self.x_start
                y = round((y1 - self.y_start) / self.cell_size) * self.cell_size + self.y_start
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
>>>>>>> Stashed changes
