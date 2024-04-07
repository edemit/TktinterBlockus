from ConceptionPieces import ConceptionPieces  

class Interface():
    def createGameField(self, size, canvas, canvasWidth, canvasHeight, nbPlayers, colors, screenWidth, screenHeight, blocks):
        self.size = size
        # Initialize the board with -1 (empty cells)
        self.board = [[-1 for _ in range(self.size)] for _ in range(self.size)]
        # Set the starting positions for each player to -2
        self.board[0][0] = self.board[0][self.size-1] = self.board[self.size-1][0] = self.board[self.size-1][self.size-1] = -2
        self.padding = 10  # Add padding
        # Calculate the size of the cell depending on the size of the game field
        self.cell_size = (min(canvasWidth, canvasHeight) - 2 * self.padding) // (self.size * 1.5)

        #calculate the corresponding coordinates for the game board 
        self.x_start = (canvasWidth - self.cell_size * self.size) / 2
        self.y_start = (canvasHeight - self.cell_size * self.size) / 2
        self.x_end = self.x_start + self.cell_size * self.size
        self.y_end = self.y_start + self.cell_size * self.size

        #draw the game board 
        for i in range(self.size+1):
            y_pos = self.y_start + self.cell_size * i
            canvas.create_line(self.x_start, y_pos, self.x_end, y_pos)

            x_pos = self.x_start + self.cell_size * i
            canvas.create_line(x_pos, self.y_start, x_pos, self.y_end)

        #creates an instance of the part design class 
        self.instance = ConceptionPieces(self.cell_size, canvas)

        #creates a list used to store figures for each player
        self.gamePiecesPlayer = []

        #figure position offsets 
        x_offset = 0
        y_offset = 0 
        placementLimit = 0 

        for player in range(1, int(nbPlayers.get()) + 1):
            #generate a figure for the player 
            player_blocks = self.instance.generate_blocks(player, nbPlayers, size)
            #Takes the color corresponding to the player's color 
            color = colors[(player - 1) % len(colors)] 

            #position delimitation corresponding to each player 
            player_offsets = [
                (0, 0, screenWidth/4),  # player 1
                (screenWidth/1.5, 0, screenWidth/1.2),  # player 2
                (0, screenHeight/2, screenWidth/4),  # player 3
                (screenWidth/1.5, screenHeight/2, screenWidth/1.2)  # player 4
                (0, 0, screenWidth/4),  #joueur 1
                (screenWidth/1.5, 0, screenWidth/1.2),  #joueur 2 
                (0, screenHeight/2, screenWidth/4), #joueur 3 
                (screenWidth/1.5, screenHeight/2, screenWidth/1.2) #joueur 4 
            ]

            #defines delimiter variables to those of the corresponding player 
            x_offset, y_offset, placementLimit = player_offsets[player-1]

            #for each block making up the figure
            for block in player_blocks:
                for item in block:
                    #colors each block making up the figure
                    canvas.itemconfig(item, fill=color) 
                    

                    #Management of piece position overruns, when there are only 2 players 
                    if int(nbPlayers.get()) == 2:
                        if player == 1 and x_offset > placementLimit:
                            x_offset = 0
                            y_offset += self.cell_size * 5
                        if player == 2 and x_offset > placementLimit:
                            x_offset = screenWidth/1.5
                            y_offset += self.cell_size * 5

                    #Management of piece position overruns, when there are between 3 and 4 players.  
                    if int(nbPlayers.get()) >= 3 and int(nbPlayers.get()) <= 5: 
                        if player == 1 or player == 3:
                            if x_offset > placementLimit:
                                x_offset = 0
                                y_offset += self.cell_size * 5
                        if player == 2 or player == 4:
                            if x_offset > placementLimit:
                                x_offset = screenWidth/1.5
                                y_offset += self.cell_size * 5 

                                
                    #depose the block 
                    canvas.move(item, x_offset, y_offset)
                #adds block to block management list 
                blocks.append(block)
                #add the part to the parts storage list 
                self.gamePiecesPlayer.append(player_blocks)
                self.gamePiecesPlayer.append(player_blocks) 
                #shifts position delimiter x 
                x_offset += self.cell_size * 3
            #player change, x and y position boundaries reset to 0 
            x_offset = 0
            y_offset = 0

    def create_figure(self, canvas, x, y, size, figure, colors, playerTurn, fill=None):
        if fill is None:
            #selects the color corresponding to that of the player whose turn it is to play 
            fill = colors[playerTurn % len(colors)]
        #list containing all the blocks making up the new part 
        parts = []
        #for each block making up the part 
        for dx, dy in figure: 
            #creates a rectangle (a block) with the corresponding coordinates 
            part = canvas.create_rectangle(x+dx*size, y+dy*size, x+(dx+1)*size, y+(dy+1)*size, fill=fill)
            #add this block to the parts list 
            parts.append(part)
        return parts
    
    def deposeFigure(self, figure, canvas, playerTurn):
        #deposit the part at the corresponding address 
        for item in figure: 
            x1, y1, x2, y2 = canvas.coords(item)
            x1 = round((x1 - self.x_start) / self.cell_size)
            y1 = round((y1 - self.y_start) / self.cell_size)
            #check that the figure is located within the enclosure of the game board 
            if not (0 <= y1 < len(self.board) and 0 <= x1 < len(self.board[0])):
                return False
            #check that the corresponding squares on the game board are empty 
            if self.board[y1][x1] != -1:
                return False
            self.board[y1][x1] = playerTurn 
            
    def displayScore(self, canvas, playersScoreLabels, playersScoreLabelsTexts, screenWidth, screenHeight, onlyUpdateDisplay):
        x = screenWidth/2.8
        y = screenHeight/1.25 
        #for each player 
        for i in range(0,len(playersScoreLabels)):
            if onlyUpdateDisplay == False: #only effective the first time the function is called, as it is not necessary to recreate the window each time the function is called. 
                #creates the window displaying the players corresponding to the scores 
                canvas.create_window(x,y,window=playersScoreLabels[i])
            #creates window displaying score values 
            x += screenWidth/14
            canvas.create_window(x,y,window=playersScoreLabelsTexts[i])
            x -= screenWidth/14 

            #according to the player, change the positions of the score labels 
            if i == 0 or i == 2:
                y += screenHeight/12.5
            elif i == 1 or i == 3:
                x += screenWidth/6 
                y = screenHeight/1.25  
