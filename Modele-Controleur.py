import tkinter
from tkinter import *  
from Vue import Interface

class ModeleControleur():
    def __init__(self):
        #Main 
        #variables de création de la fenêtre 
        self.root = tkinter.Tk()
        self.root.title("Blokus")
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f'{self.screen_width}x{self.screen_height}')
        self.root.resizable(True, True)
        #variables de gestion des données 
        self.playerTurn = 0
        self.points = [0,0,0,0]
        self.c = 0 
        self.current_figure = None
        self.old = [None, None]
        self.blocks = []
        self.available_coords = None
        #Vue 
        self.available_coords = None 
        #variables du canvas 
        self.vueScript = Interface()
        self.canvas_width = self.screen_width * 0.95
        self.canvas_height = self.screen_height * 0.9 
        self.colors = ['red', 'blue', 'green', 'yellow']
        self.canvas = tkinter.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, scrollregion=(0,0,self.canvas_width,self.canvas_height), bg='white')
        self.canvas.place(relx=0.5, rely=0.5, anchor='center')
        self.canvas.pack(expand=True)
        #variables de l'affichage du score
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
        #mets en place la gestion de l'input de selection
        self.input() 

        #crée la fenêtre de menu 
        self.gameFieldGenerator()

    def input(self):
        if self.canvas:
            #lorsque le bouton gauche de la souris et cliqué, la fonction "selectionner" est appelée 
            self.canvas.bind("<Button-1>", self.selectionner)
            
    def selectionner(self, event):
        self.c = (self.c + 1) % 2
        #si le clic du bouton gauche de la souris est bien détecté (pas sur, a revoir)
        if self.c == 1:
            #récupére la pièce la plus proche de la souris 
            item = self.canvas.find_closest(event.x, event.y)
            #récupère et vérifie que la couleur de la pièce corresponde à la couleur correspondante au joueur 
            #afin de vérifier que le joueur actuel est bien celui qui doit jouer a ce moment la (si c'est bien son tour de jeu)
            currentColor =self.colors[self.playerTurn % len(self.colors)]
            print(currentColor, end=" ")
            itemColor = self.canvas.itemcget(item, "fill")
            print(itemColor)
            if itemColor == currentColor:
                #récupére chaque bloc composant la pièce
                self.current_figure = next((block for block in self.blocks if item[0] in block), None)  
                #Ilia faudra que t'explique la 
                if self.current_figure is not None:
                    x1, y1, x2, y2 = self.canvas.coords(self.current_figure[0])
                    self.original_coords = (x1, y1)
                    self.current_figure_pattern = [(x1-x, y1-y) for x, y in [(self.canvas.coords(item)[0], self.canvas.coords(item)[1]) for item in self.current_figure]]
                self.old[0] = event.x
                self.old[1] = event.y
                self.canvas.bind("<Motion>",self.glisser)
            #indique au joueur que ca n'est pas son tour de jeu, et empeche la pièce d'être déplacé 
            else:
                print("This is not your turn")
                self.c = 0
        #si le joueur reclique sur le bouton gauche de la souris alors qu'il a selectionné la pièce, il la dépose (pas sur, a revoir)
        else: 
            self.old[0] = None
            self.old[1] = None
            self.canvas.unbind("<Motion>")
            self.deposer(event.x,event.y)

    def deposer(self, x, y):
        if self.current_figure is not None:
            #calcule les nouveaux coordonnées de la pièce sur la base du plateau de jeu
            new_figure = []
            for item in self.current_figure:
                x1, y1, x2, y2 = self.canvas.coords(item)
                x = (round((x1 - self.vueScript.x_start) / self.vueScript.cell_size) * self.vueScript.cell_size) + self.vueScript.x_start
                y = (round((y1 - self.vueScript.y_start) / self.vueScript.cell_size) * self.vueScript.cell_size) + self.vueScript.y_start
                new_figure.append((x, y))
            #vérifie que la pièce puisse être placé sur le plateau de jeu
            if all(self.is_in_grid(x, y) for x, y in new_figure) and (x, y) in self.available_coords[self.playerTurn]:
                for item in self.current_figure:
                    #mets a jour le score 
                    self.points[self.playerTurn] += 1 
                    self.playerScoreText[self.playerTurn].set(self.points[self.playerTurn])

                    #supprime la pièce de la liste de pièces présente sur la canvas 
                    self.canvas.delete(item)
                #cree une nouvelle pièce, ayant la même géométrie que la pièce venant d'être suppprimé 
                self.current_figure = [self.vueScript.create_figure(self.canvas, x, y, self.vueScript.cell_size, self.current_figure_pattern, self.colors, self.playerTurn, fill=None) for x, y in new_figure]
                #déposer la pièce sur le plateau de jeu, bloc après bloc (les blocs sont les carrés composant la pièce)
                for figure in self.current_figure:
                    self.vueScript.deposeFigure(figure, self.canvas, self.playerTurn)
                #change le tour de jeu (passe au joueur suivant)
                self.playerTurn = (self.playerTurn + 1) % int(self.numberOfPlayers.get())
                #mets a jour la matrice gérant les coordonées du plateau de jeu ou des pièces peuvent être posées
                self.update_available_coords()
            else:
                #fais revenir la pièce a sa position initiale 
                x1, y1, x2, y2 = self.canvas.coords(self.current_figure[0])
                for part in self.current_figure:
                    self.canvas.move(part, self.original_coords[0] - x1, self.original_coords[1] - y1)
                self.vueScript.displayScore(self.canvas, self.playersScoreLabels[:self.players], self.playersScoreLabelsTexts[:self.players], self.screen_width, self.screen_height, True) 
            #mets a jour l'affichage du score 
            self.vueScript.displayScore(self.canvas, self.playersScoreLabels[:self.players], self.playersScoreLabelsTexts[:self.players], self.screen_width, self.screen_height, True)
            #vérifie les conditions de fin de partie 
            self.check_end_game()

    def glisser(self, event):
        #modifie les coordonnées de la pièce en fonction du mouvement de la souris, afin de déplacer la pièce 
        if self.current_figure is not None:
            for item in self.current_figure:
                self.canvas.move(item, event.x-self.old[0], event.y-self.old[1])
            self.old[0]=event.x
            self.old[1]=event.y

    def is_in_grid(self, x, y):
        #vérifie que la pièce se situe bien dans l'enceinte du plateau de jeu 
        for item in self.current_figure:
            x1, y1, x2, y2 = self.canvas.coords(item)
            x1 = round((x1 - self.vueScript.x_start) / self.vueScript.cell_size)
            y1 = round((y1 - self.vueScript.y_start) / self.vueScript.cell_size)
            if not (0 <= y1 < len(self.vueScript.board) and 0 <= x1 < len(self.vueScript.board[0])):
                return False
            #vérifie que les cases du plateau de jeu ou se situe la pièce sont vides 
            if self.vueScript.board[y1][x1] != -1:
                return False
        return True
    
    def update_available_coords(self):
        #supprime les coordonnées utilisés 
        for i, coords in enumerate(self.available_coords[self.playerTurn]):
            if self.vueScript.board[coords[1]][coords[0]] != -1:
                del self.available_coords[self.playerTurn][i]
        
         # Add new available coordinates

         #re initialise la matrice avec les nouveaux coordonnées disponibles (donc la liste des cases du plateau de jeu vides)
        for item in self.current_figure:
            x1, y1, x2, y2 = self.canvas.coords(item)
            x1 = round((x1 - self.vueScript.x_start) / self.vueScript.cell_size)
            y1 = round((y1 - self.vueScript.y_start) / self.vueScript.cell_size)
            new_coords = [(x1-1, y1-1), (x1+1, y1-1), (x1-1, y1+1), (x1+1, y1+1)]
            self.available_coords[self.playerTurn].extend(new_coords)

    def check_end_game(self):
        #si tous les coordonnées de la matrice sont pris, arrete la partie 
        if not any(self.available_coords):
            self.end_game()

    def end_game(self):
        #affiche une fenetre de fin de partie 
        end_game_window = tkinter.Toplevel(self.root)
        end_game_window.title("Game Over")
        end_game_window.geometry("200x100")
        tkinter.Label(end_game_window, text="Game Over!").pack()
        #affiche un bouton de relance de partie
        tkinter.Button(end_game_window, text="Relaunch", command=self.relaunchGame).pack()
        #affiche un bouton indiquant qu'une partie à été relancé 
        tkinter.Button(end_game_window, text="OK", command=end_game_window.destroy).pack()
    
    # Relaunch the game
    def relaunchGame(self):
        self.playerTurn = 0 
        #réinitialisation des variables servant à gérer les données de gameplay 
        self.playerTurn = 0
        self.points = [0,0,0,0]
        self.c = 0 
        self.current_figure = None
        self.old = [None, None]
        self.blocks = []
        self.available_coords = None 
        #crée la fenêtre de menu 
        self.gameFieldGenerator()

    def gameFieldGenerator(self):
        #crée la fenetre de menu 
        self.gameFieldWindow = tkinter.Toplevel(self.root)
        self.gameFieldWindow.title("Game field generator")
        self.gameFieldWindow.geometry("300x200")

        #liste des tailles possibles du plateau de jeu (allant de 5x5 a 20x20)
        boardSizes = [str(i) for i in range(5, 21)]
        self.boardSize = tkinter.StringVar(self.gameFieldWindow)
        self.boardSize.set(boardSizes[0])  # Default value
        self.boardSize.set(boardSizes[0])
        boardSizeLabel = tkinter.Label(self.gameFieldWindow, text="Board size:")
        boardSizeLabel.pack()
        #crée le menu d'option permettant de choisir la taille du plateau de jeu 
        boardSizeMenu = tkinter.OptionMenu(self.gameFieldWindow, self.boardSize, *boardSizes)
        boardSizeMenu.pack()

        #crée la spinbox permettant de choisir combien de joueurs jouent (allant de 2 à 4)
        numberOfPlayersLabel = tkinter.Label(self.gameFieldWindow, text="Number of players 2-4:")
        numberOfPlayersLabel.pack()
        self.numberOfPlayers = tkinter.Spinbox(self.gameFieldWindow, from_=2, to=4)
        self.numberOfPlayers.pack()

        #crée le bouton pour lancer une partie 
        startButton = tkinter.Button(self.gameFieldWindow, text="Start game", command=self.startGame)
        startButton.pack()
        self.gameFieldWindow.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.gameFieldWindow.attributes("-topmost", True)
        self.gameFieldWindow.mainloop()

    def startGame(self):
        #récupère la taille du plateau de jeu et le nombre de joueurs, sélectionnés dans le fenêtre de menu 
        self.size = int(self.boardSize.get())
        self.players = int(self.numberOfPlayers.get())

        #initialise les coordonnées disponibles après que la taille du plateau du jeu est été defini
        self.available_coords = [[(0, 0), (0, self.size-1), (self.size-1, 0), (self.size-1, self.size-1)] for _ in range(4)]

        #ferme la fenêtre de menu 
        self.gameFieldWindow.withdraw()

        #place la fenêtre principale au premier plan 
        self.root.attributes('-topmost', True)

        #crée l'espace de jeu, comprenant le plateau de jeu et le pièces de chaque joueur 
        self.vueScript.createGameField(self.size,self.canvas,self.canvas_width,self.canvas_height,self.numberOfPlayers,self.colors,self.screen_width,self.screen_height,self.blocks)

        #affiche le score 
        self.vueScript.displayScore(self.canvas, self.playersScoreLabels[:self.players], self.playersScoreLabelsTexts[:self.players], self.screen_width, self.screen_height, False) 

    #lance la fenêtre Tkinter 
    def run(self):
        self.root.mainloop()

#crée une instance de la classe Controleur
controleur = ModeleControleur()

#appelle la fonction permettant de lancer la fenêtre Tkinter 
controleur.run()   