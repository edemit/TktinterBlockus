# Blokus game is a strategy game for 2-4 players where you try to lay down as many of your tiles on the board as you can. When you play a tile, you must place it so it touches a corner on at least one of your other pieces. Once you play as many tiles as you can, count the tiles that you weren’t able to place to determine the winner.

import tkinter 
import ConceptionBriques
from ConceptionBriques import ConceptionBriques 
import Controleur
from Controleur import ControleurInput 

# Global variables

boardSize = 0 
numberOfPlayers = 0
gameFieldWindow = 0
playerTurn = 0 #int 
gamePiecesPlayer = []  # Declare gamePiecesPlayer as a global variable

# Create the main window
root = tkinter.Tk()
root.title("Blokus")

# Get screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size depending on screen size
root.geometry(f'{screen_width}x{screen_height}')

# Resizable window
root.resizable(True, True)

# Create the adaptive canvas
global canvas
canvas_width = screen_width * 0.95  # Define the width of the canvas depending on the screen size
canvas_height = screen_height * 0.9  # Define the height of the canvas depending on the screen size
canvas = tkinter.Canvas(root, width=canvas_width, height=canvas_height, scrollregion=(0,0,canvas_width,canvas_height), bg='green')

# Canvas in the center of the window
canvas.place(relx=0.5, rely=0.5, anchor='center')
canvas.pack(expand=True)

controleur = ControleurInput() 

# Create the game field ganerator window in tkinter window before starting the game to change the size of the game field or number of players
def gameFieldGenerator():
    global boardSize
    global numberOfPlayers
    global gameFieldWindow
    gameFieldWindow = tkinter.Toplevel(root)
    gameFieldWindow.title("Game field generator")
    gameFieldWindow.geometry("300x200")

    # List of possible board sizes
    boardSizes = [str(i) for i in range(5, 21)]  # 5x5, 6x6, 7x7, ..., 20x20
    boardSize = tkinter.StringVar(gameFieldWindow)
    boardSize.set(boardSizes[0])  # Default value
    boardSizeLabel = tkinter.Label(gameFieldWindow, text="Board size:")
    boardSizeLabel.pack()
    boardSizeMenu = tkinter.OptionMenu(gameFieldWindow, boardSize, *boardSizes)
    boardSizeMenu.pack()

    # Spinbox creation
    numberOfPlayersLabel = tkinter.Label(gameFieldWindow, text="Number of players 2-4:")
    numberOfPlayersLabel.pack()
    numberOfPlayers = tkinter.Spinbox(gameFieldWindow, from_=2, to=4)
    numberOfPlayers.pack()

    startButton = tkinter.Button(gameFieldWindow, text="Start game", command=lambda: [createGameField(int(boardSize.get())), startGame()])
    startButton.pack()
    gameFieldWindow.protocol("WM_DELETE_WINDOW", root.destroy)
    gameFieldWindow.attributes("-topmost", True)
    gameFieldWindow.mainloop()

# Create the game field
# Create the game field
def createGameField(size):
    global gamePiecesPlayer  # Declare gamePiecesPlayer as global at the start of the function

    padding = 10  # Add padding
    # Calculate the size of the cell depending on the size of the game field
    global cell_size 
    cell_size = (min(canvas_width, canvas_height) - 2 * padding) // (size * 1.5)

    for i in range(size):
        canvas.create_line(480,110+cell_size*i,980,110+cell_size*i)
        canvas.create_line(480+cell_size*i,110,480+cell_size*i,600)

    #Coordinates for determine the limits of the grid 
    #For x1 : 480 
    #For y1 : 110 
    #For x2 : 480 + cell_size * size 
    #For y2 : 110 + cell_size * size 
    canvas.create_rectangle(480,110,480+cell_size*size,110+cell_size*size,outline="blue")

    #Instanciation of blocks
    instance = ConceptionBriques(cell_size, canvas)
    blocks = instance.generate_blocks(playerTurn)
    global block 

    # Store the blocks in lists 
    gamePiecesPlayer = []

    #Placement of the figures 
    for player in range(1,int(numberOfPlayers.get())):
        player_blocks = instance.generate_blocks(player)
        if player%2 == 0:
            x_offset = canvas_width/4
        else: 
            x_offset = canvas_width - (len(player_blocks[0]) * cell_size + 50) 
        for block in player_blocks:
            for item in block:
                canvas.move(item, x_offset, 0)
            gamePiecesPlayer.append(player_blocks)

def selectionner(event):
    global c, item, itemType 
    c = (c + 1) % 2
    if c == 1:
        item = canvas.find_closest(event.x, event.y)
        old[0] = event.x
        old[1] = event.y
        canvas.bind("<Motion>",glisser)
    else:
        old[0] = None
        old[1] = None
        canvas.unbind("<Motion>")
        deposer(event.x,event.y)
        
def glisser(event):
    global item  
    x1, y1, x2, y2 = canvas.coords(item)
    if (old[0] >= x1 and old[0] <= x2 and old[1] >= y1 and old[1] <= y2):
        canvas.move(item, event.x-old[0], event.y-old[1])
        old[0]=event.x
        old[1]=event.y

def deposer(x,y):
    global item
    x1, y1, x2, y2 = canvas.coords(item)

old = [None,None]
c = 0 

controleur.initProperties(canvas,selectionner)
controleur.input() 

def startGame():
    # Getting the size of the game field and the number of players from the game field generator window
    size = int(boardSize.get())
    players = int(numberOfPlayers.get())
    
    # Close the game field generator window
    gameFieldWindow.withdraw()

    # Set the main window to the top level
    root.attributes('-topmost', True)

gameFieldGenerator()

root.mainloop()