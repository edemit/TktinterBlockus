# Blokus game is a strategy game for 2-4 players where you try to lay down as many of your tiles on the board as you can. When you play a tile, you must place it so it touches a corner on at least one of your other pieces. Once you play as many tiles as you can, count the tiles that you weren’t able to place to determine the winner.

import tkinter 

# Create the main window
root = tkinter.Tk()
root.title("Blokus")

# Получаем размеры экрана
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Устанавливаем размеры окна в зависимости от размеров экрана
root.geometry(f'{screen_width}x{screen_height}')

# Create the adaptive canvas
global canvas
canvas = tkinter.Canvas(root, width=screen_width, height=screen_height)
canvas.pack()

# Create the game field ganerator window in tkinter window before starting the game to change the size of the game field or number of players
def gameFieldGenerator():
    global boardSize
    global numberOfPlayers
    global gameFieldWindow
    gameFieldWindow = tkinter.Toplevel(root)
    gameFieldWindow.title("Game field generator")
    gameFieldWindow.geometry("300x200")

    # Создаем список возможных размеров доски
    boardSizes = [str(i) for i in range(5, 21)]  # Допустим, размеры доски могут быть от 5 до 20
    boardSize = tkinter.StringVar(gameFieldWindow)
    boardSize.set(boardSizes[0])  # Устанавливаем начальное значение
    boardSizeLabel = tkinter.Label(gameFieldWindow, text="Board size:")
    boardSizeLabel.pack()
    boardSizeMenu = tkinter.OptionMenu(gameFieldWindow, boardSize, *boardSizes)
    boardSizeMenu.pack()

    # Создаем Spinbox для выбора количества игроков
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
    # Рассчитываем размеры линий в зависимости от выбранного размера
    line_width = screen_width // size
    line_height = screen_height // size

    for i in range(size):
        canvas.create_line(i*line_width, 0, i*line_width, screen_height)
        canvas.create_line(0, i*line_height, screen_width, i*line_height)

def startGame():

    # Получаем выбранные пользователем параметры
    size = int(boardSize.get())
    players = int(numberOfPlayers.get())
    
    # Закрываем окно генератора игрового поля
    gameFieldWindow.destroy()

    # Здесь начинаем игру с выбранными параметрами
    # ...

gameFieldGenerator()

root.mainloop()