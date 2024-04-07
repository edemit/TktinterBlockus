class ConceptionPieces:
    def __init__(self, unite, canvas):
        #variable de création des pièces 
        self.unite = unite
        self.canvas = canvas
        self.blocks = []
        self.selected_block = None
        self.old_coords = None

    def createRectangle(self, x, y, color):
        #crée un rectangle de longueur déterminée par la taille des cases du plateau de jeu 
        return self.canvas.create_rectangle(x*self.unite, y*self.unite, (x+1)*self.unite, (y+1)*self.unite, fill=color)
    
    def conception(self, coords, color):
        #appelle la fonction de creation de rectangle 
        self.blocks = [self.createRectangle(x, y, color) for x, y in coords]

    def generate_blocks(self, playerTurn, nbPlayers, size):
        #définit les couleurs des blocs parmi une liste des couleurs disponible 
        colors = {0: "blue", 1: "red", 2: "green", 3: "yellow"}
        #définit la couleur a appliquer à la pièce, par rapport à la couleur correspondante au joueur dont la pièce est attribuée 
        color = colors[(playerTurn - 1) % len(colors)] 
        
        #définit les formes des pièces disponibles pour chaque taille du plateau de jeu 
        availableShapes = {
            5: ["square","stick"],
            6: ["square","stick"],
            7: ["square","stick","L"],
            8: ["square","stick","L"],
            9: ["square","stick","L","cross"],
            10: ["square","stick","L","cross"],
            11: ["square","stick","L","cross","T"],
            12 : ["block","square","stick","L","cross","T"],
            13 : ["square","stick","L","cross","T","block"],
            14 : ["square","stick","L","cross","T","block"],
            15 : ["square","stick","L","cross","T","block","G"],
            16 : ["square","stick","L","cross","T","block","G"],
            17 : ["square","stick","L","cross","T","block","G","L2"],
            18 : ["square","stick","L","cross","T","block","G","L2"],
            19 : ["square","stick","L","cross","T","block","G","L2"],
            20 : ["square","stick","L","cross","T", "block","G","L2"]
        }

        #réduit le nombre de pièces par joueur en fonction du nombre de joueurs 
        if int(nbPlayers.get()) > 2 and int(nbPlayers.get()) <= 4:
            availableShapesForSize = availableShapes.get(size - (int(nbPlayers.get())-2), [])
            print(int(nbPlayers.get())-2)
        else: 
            availableShapesForSize = availableShapes.get(size, [])

        #définit la forme de chaque pièce 
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
        
        #crée une liste servant a contenir les pièces 
        blocks = [] 

        #pour chaque pièce pouvant être construite 
        for shapeName in availableShapesForSize:
            #récupérer les coordonnées de la forme de la pièce 
            shapeCoords = shapes[shapeName]
            #crée un bloc
            self.conception(shapeCoords, color)
            #ajouter ce bloc a la liste blocks 
            blocks.append(self.blocks)
        #retourne la liste des pièces 
        return blocks