class ControleurInput():
    def __init__(self):
        self.canvas = None
        self.selectionFigure = None 

    def initProperties(self, canvas, fonctionSelection):
        self.canvas = canvas
        self.selectionFigure = fonctionSelection 
        
    def input(self):
        if self.canvas:
            self.canvas.bind("<Button-1>", self.selectionFigure)