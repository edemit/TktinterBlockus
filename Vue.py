import tkinter
from ConceptionBriques import ConceptionBriques 

class Interface():
    def createGameField(self, size, canvas, canvasWidth, canvasHeight, nbPlayers, colors, screenWidth, screenHeight, blocks):
        self.size = size
        self.board = [[-1 for _ in range(size)] for _ in range(size)]  # Create a game field
        self.padding = 10  # Add padding
        # Calculate the size of the cell depending on the size of the game field
        self.cell_size = (min(canvasWidth, canvasHeight) - 2 * self.padding) // (self.size * 1.5)

        # Calculate relative coordinates for the game field
        self.x_start = (canvasWidth - self.cell_size * self.size) / 2
        self.y_start = (canvasHeight - self.cell_size * self.size) / 2
        self.x_end = self.x_start + self.cell_size * self.size
        self.y_end = self.y_start + self.cell_size * self.size

        for i in range(self.size+1):
            y_pos = self.y_start + self.cell_size * i
            canvas.create_line(self.x_start, y_pos, self.x_end, y_pos)

            x_pos = self.x_start + self.cell_size * i
            canvas.create_line(x_pos, self.y_start, x_pos, self.y_end)

        #Instanciation of blocks
        self.instance = ConceptionBriques(self.cell_size, canvas)

        # Store the blocks in lists 
        self.gamePiecesPlayer = []
        
        #Placement of the figures 
        x_offset = 0  # Define x_offset variable
        y_offset = 0 #Define y_offset variable 
        placementLimit = 0 #Define the border for each zone
        for player in range(1, int(nbPlayers.get()) + 1):
            player_blocks = self.instance.generate_blocks(player, nbPlayers, size)
            color = colors[(player - 1) % len(colors)] 

            player_offsets = [
                (0, 0, screenWidth/4),  # player 1
                (screenWidth/1.5, 0, screenWidth/1.2),  # player 2
                (0, screenHeight/2, screenWidth/4),  # player 3
                (screenWidth/1.5, screenHeight/2, screenWidth/1.2)  # player 4
            ]

            x_offset, y_offset, placementLimit = player_offsets[player-1]

            for block in player_blocks:
                for item in block:
                    canvas.itemconfig(item, fill=color)  # установите цвет
                    
                    if int(nbPlayers.get()) == 2:
                        if player == 1 and x_offset > placementLimit:
                            x_offset = 0
                            y_offset += self.cell_size * 5
                        if player == 2 and x_offset > placementLimit:
                            x_offset = screenWidth/1.5
                            y_offset += self.cell_size * 5

                    if int(nbPlayers.get()) >= 3 and int(nbPlayers.get()) <= 5: 
                        if player == 1 or player == 3:
                            if x_offset > placementLimit:
                                x_offset = 0
                                y_offset += self.cell_size * 5
                        if player == 2 or player == 4:
                            if x_offset > placementLimit:
                                x_offset = screenWidth/1.5
                                y_offset += self.cell_size * 5 

                    canvas.move(item, x_offset, y_offset)
                blocks.append(block)  # Добавьте блок в список
                self.gamePiecesPlayer.append(player_blocks)
                self.gamePiecesPlayer.append(player_blocks) 
                x_offset += self.cell_size * 3
            x_offset = 0
            y_offset = 0

    def create_figure(self, canvas, x, y, size, figure, colors, playerTurn, fill=None):
        if fill is None:
            fill = colors[playerTurn % len(colors)]
        parts = []
        for dx, dy in figure:
            part = canvas.create_rectangle(x+dx*size, y+dy*size, x+(dx+1)*size, y+(dy+1)*size, fill=fill)
            parts.append(part)
        return parts
    
    def deposeFigure(self, figure, canvas, playerTurn):
        # Fill the board with the current player's number
        for item in figure: 
            x1, y1, x2, y2 = canvas.coords(item)
            x1 = round((x1 - self.x_start) / self.cell_size)
            y1 = round((y1 - self.y_start) / self.cell_size)
            self.board[y1][x1] = playerTurn 
            
    def displayScore(self, canvas, playersScoreLabels, screenWidth, screenHeight):
        x = screenWidth/2.8
        y = screenHeight/1.25 
        for i in range(0,len(playersScoreLabels)):
            canvas.create_window(x,y,window=playersScoreLabels[i])
            if i == 0 or i == 2:
                y += screenHeight/12.5
            elif i == 1 or i == 3:
                y = screenHeight/1.25 
                x += screenWidth/6 
            print("here")
