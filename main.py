# Blokus game is a strategy game for 2-4 players where you try to lay down as many of your tiles on the board as you can. When you play a tile, you must place it so it touches a corner on at least one of your other pieces. Once you play as many tiles as you can, count the tiles that you weren’t able to place to determine the winner.

import tkinter 
from tkinter import Scrollbar
import ConceptionBriques
from ConceptionBriques import ConceptionBriques

# Global variables

boardSize = 0 
numberOfPlayers = 0
gameFieldWindow = 0
playerTurn = 0 #int 

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

    startButton = tkinter.Button(gameFieldWindow, text="Start game", command=lambda: [startGame(), createGameField(int(boardSize.get()))])
    startButton.pack()
    gameFieldWindow.protocol("WM_DELETE_WINDOW", root.destroy)
    gameFieldWindow.attributes("-topmost", True)
    gameFieldWindow.mainloop()

# Create the game field
def createGameField(size):
    padding = 10  # Add padding
    # Calculate the size of the cell depending on the size of the game field
    cell_size = (min(canvas_width, canvas_height) - 2 * padding) // (size * 1.5)

    # Create the game field
    global game_canvas 
    game_canvas = tkinter.Canvas(canvas, width=cell_size*size + 2 * padding, height=cell_size*size + 2 * padding, bg='white')

    for i in range(size):
        for j in range(size):
            x1 = i * cell_size + padding
            y1 = j * cell_size + padding
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            game_canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

    #Instanciation of blocks
    instance = ConceptionBriques(cell_size, canvas)

    # Center-north the game field in the main window
    game_canvas.place(relx=0.5, rely=0.35, anchor = 'center')
    
    global gamePiecesPlayer 
    gamePiecesPlayer = []
    block = []

    for player in range(int(numberOfPlayers.get())):
        block = instance.generate_blocks(player)
        print(block) 
        for i, block in enumerate(block):
            for rect in block:
                x1, y1, x2, y2 = game_canvas.coords(rect)
                gamePiecesPlayer.append(game_canvas.create_rectangle(x1, y1, x2, y2, fill = "blue")) 

    game_canvas.bind("<Button-1>",gamePiecesPlayer1Movement) 

def startGame():
    # Getting the size of the game field and the number of players from the game field generator window
    size = int(boardSize.get())
    players = int(numberOfPlayers.get())
    
    # Close the game field generator window
    gameFieldWindow.withdraw()

    # Set the main window to the top level
    root.attributes('-topmost', True)

    # Here we start game with chosen parameters
    # ...

def gamePiecesPlayer1Movement(event):
    global canMovePiece 
    canMovePiece = (canMovePiece + 1)%2  
    if (canMovePiece == 1):
        game_canvas.bind("<Motion>",glisser)
        old[0]=event.x
        old[1]=event.y
    else:
        game_canvas.unbind("<Motion>")
        
def glisser(event):
    x1, y1, x2, y2 = game_canvas.coords(gamePiecesPlayer[0])
    print(gamePiecesPlayer[0], x1, y1, x2, y2)
    if (old[0] >= x1 and old[0] <= x2 and old[1] >= y1 and old[1] <= y2):
        game_canvas.move(gamePiecesPlayer[0], event.x-old[0], event.y-old[1])
        old[0]=event.x
        old[1]=event.y
        
old = [None, None]
canMovePiece = 0 

gameFieldGenerator()

root.mainloop()