import tkinter
from ConceptionPieces import ConceptionPieces  

class Interface():
    def createGameField(self, size, canvas, canvasWidth, canvasHeight, nbPlayers, colors, screenWidth, screenHeight, blocks):
        self.size = size
        self.board = [[-1 for _ in range(size)] for _ in range(size)]  # Create a game field
        self.padding = 10  # Add padding
        self.size = size #récupère la taille du plateau de jeu 
        self.board = [[-1 for _ in range(size)] for _ in range(size)] #crée le plateau de jeu 
        self.padding = 10  #ajoute du padding 
        # Calculate the size of the cell depending on the size of the game field
        self.cell_size = (min(canvasWidth, canvasHeight) - 2 * self.padding) // (self.size * 1.5)

        # Calculate relative coordinates for the game field
        #calcul les coordonnées correspondants pour le plateau de jeu 
        self.x_start = (canvasWidth - self.cell_size * self.size) / 2
        self.y_start = (canvasHeight - self.cell_size * self.size) / 2
        self.x_end = self.x_start + self.cell_size * self.size
        self.y_end = self.y_start + self.cell_size * self.size

        #dessine le plateau de jeu 
        for i in range(self.size+1):
            y_pos = self.y_start + self.cell_size * i
            canvas.create_line(self.x_start, y_pos, self.x_end, y_pos)

            x_pos = self.x_start + self.cell_size * i
            canvas.create_line(x_pos, self.y_start, x_pos, self.y_end)

        #crée une instance de la classe de conception des pièces 
        self.instance = ConceptionPieces(self.cell_size, canvas)

        #crée une liste servant a stocker les pièces 
        self.gamePiecesPlayer = []

        #variables de délimitation (offsets) de position des pièces 
        x_offset = 0
        y_offset = 0 
        placementLimit = 0 

        for player in range(1, int(nbPlayers.get()) + 1):
            #génére une pièce 
            player_blocks = self.instance.generate_blocks(player, nbPlayers, size)
            #récupère la couleur correspondante a celle du joueur 
            color = colors[(player - 1) % len(colors)] 

            #délimitation de position correspondants a chaque joueur 
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

            #définit les variables de délimition sur celles du joueur correspondant 
            x_offset, y_offset, placementLimit = player_offsets[player-1]

            #pour chaque bloc composant la pièce 
            for block in player_blocks:
                for item in block:
                    #colorit chaque bloc composant la pièce 
                    canvas.itemconfig(item, fill=color) 
                    

                    #gestion des dépassements des délimitations de position des pièces, dans le cas ou il n'y a que 2 joueurs 
                    if int(nbPlayers.get()) == 2:
                        if player == 1 and x_offset > placementLimit:
                            x_offset = 0
                            y_offset += self.cell_size * 5
                        if player == 2 and x_offset > placementLimit:
                            x_offset = screenWidth/1.5
                            y_offset += self.cell_size * 5

                    #gestion des dépassements des délimitations de position des pièces, dans le cas ou il y a entre 3 et 4 joueurs  
                    if int(nbPlayers.get()) >= 3 and int(nbPlayers.get()) <= 5: 
                        if player == 1 or player == 3:
                            if x_offset > placementLimit:
                                x_offset = 0
                                y_offset += self.cell_size * 5
                        if player == 2 or player == 4:
                            if x_offset > placementLimit:
                                x_offset = screenWidth/1.5
                                y_offset += self.cell_size * 5 

                                
                    #dépose le bloc 
                    canvas.move(item, x_offset, y_offset)
                #ajoute le bloc a la liste de gestion des blocs 
                blocks.append(block)
                #ajoute la pièce à la liste servant a stocker les pièces 
                self.gamePiecesPlayer.append(player_blocks)
                self.gamePiecesPlayer.append(player_blocks) 
                #décale la délimitation de position x 
                x_offset += self.cell_size * 3
            #changement de joueur, on remet les délimitations de position x et y a 0 
            x_offset = 0
            y_offset = 0

    def create_figure(self, canvas, x, y, size, figure, colors, playerTurn, fill=None):
        if fill is None:
            #sélectionne la couleur correspondante a celle du joueur dont c'est le tour de jeu 
            fill = colors[playerTurn % len(colors)]
        #liste contenant tous les blocs composant la nouvelle pièce 
        parts = []
        #pour chaque bloc composant la pièce 
        for dx, dy in figure: 
            #crée un rectangle (un bloc) avec les coordonnées correspondants 
            part = canvas.create_rectangle(x+dx*size, y+dy*size, x+(dx+1)*size, y+(dy+1)*size, fill=fill)
            #ajoute ce bloc a la liste parts 
            parts.append(part)
        return parts
    
    def deposeFigure(self, figure, canvas, playerTurn):
        #dépose la pièce aux coordonnées correspondantes 
        for item in figure: 
            x1, y1, x2, y2 = canvas.coords(item)
            x1 = round((x1 - self.x_start) / self.cell_size)
            y1 = round((y1 - self.y_start) / self.cell_size)
            #vérifie que la figure se situe dans l'enceine du plateau de jeu 
            if not (0 <= y1 < len(self.board) and 0 <= x1 < len(self.board[0])):
                return False
            #vérifie que les cases du plateau de jeu correspondantes sont vides 
            if self.board[y1][x1] != -1:
                return False
            self.board[y1][x1] = playerTurn 
            
    def displayScore(self, canvas, playersScoreLabels, playersScoreLabelsTexts, screenWidth, screenHeight, onlyUpdateDisplay):
        x = screenWidth/2.8
        y = screenHeight/1.25 
        #pour chaque joueur 
        for i in range(0,len(playersScoreLabels)):
            if onlyUpdateDisplay == False: #effectif seulement lors du premier appel de la fonction, car il n'est pas nécéssaire de récréer la fenêtre a chaque nouvel appel de la fonction 
                #crée la fenêtre affichant les joueurs correspondant aux scores 
                canvas.create_window(x,y,window=playersScoreLabels[i])
            #crée la fenêtre affichant les valeurs de score 
            x += screenWidth/14
            canvas.create_window(x,y,window=playersScoreLabelsTexts[i])
            x -= screenWidth/14 

            #en fonction de joueur, modifier les positions des labels de score 
            if i == 0 or i == 2:
                y += screenHeight/12.5
            elif i == 1 or i == 3:
                x += screenWidth/6 
                y = screenHeight/1.25  
