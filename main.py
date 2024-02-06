# Blokus game is a strategy game for 2-4 players where you try to lay down as many of your tiles on the board as you can. When you play a tile, you must place it so it touches a corner on at least one of your other pieces. Once you play as many tiles as you can, count the tiles that you weren’t able to place to determine the winner.

import tkinter 
from tkinter import Scrollbar

# Create the main window
root = tkinter.Tk()
root.title("Blokus")

# Получаем размеры экрана
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Устанавливаем размеры окна в зависимости от размеров экрана
root.geometry(f'{screen_width}x{screen_height}')

# Делаем окно масштабируемым
root.resizable(True, True)

# Create the adaptive canvas
global canvas
canvas_width = screen_width * 0.8  # Устанавливаем ширину холста равной 80% ширины экрана
canvas_height = screen_height * 0.8  # Устанавливаем высоту холста равной 80% высоты экрана
canvas = tkinter.Canvas(root, width=canvas_width, height=canvas_height, scrollregion=(0,0,canvas_width,canvas_height))

# Размещаем холст в центре окна
canvas.pack(expand=True)

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
    # Рассчитываем размеры клетки в зависимости от выбранного размера и размера холста
    cell_size = min(canvas_width, canvas_height) // size

    for i in range(size):
        for j in range(size):
            x1 = i * cell_size
            y1 = j * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            canvas.create_rectangle(x1, y1, x2, y2)

def startGame():

    # Получаем выбранные пользователем параметры
    size = int(boardSize.get())
    players = int(numberOfPlayers.get())
    
    # Скрываем окно генератора игрового поля
    gameFieldWindow.withdraw()

    # Устанавливаем окно с полем поверх всех остальных окон
    root.attributes('-topmost', True)

    # Здесь начинаем игру с выбранными параметрами
    # ...

gameFieldGenerator()

root.mainloop()