class ConceptionBriques: 
    def __init__(self, unite, canvas):
        self.unite = unite 
        self.canvas = canvas 

    def conception(self,numero):
        #Création des figures
        if numero == 1:
            self.rectangle = self.canvas.create_rectangle(self.unite,self.unite,self.unite*2,self.unite*2,fill="red") #1 par 1 
        elif numero == 2:
            self.rectangle = self.canvas.create_rectangle(self.unite,self.unite,self.unite*4,self.unite*4,fill="red") #1 par 2 
        elif numero == 3:
            self.rectangle = self.canvas.create_rectangle(self.unite*2,self.unite*2,self.unite*4,self.unite*4,fill="red") #2 par 2 