from tkinter import Tk, Canvas

def create_figure(cnv, x, y, figure, size=100, fill='red'):
    parts = []
    for dx, dy in figure:
        part = cnv.create_rectangle(x+dx*size, y+dy*size, x+(dx+1)*size, y+(dy+1)*size, fill=fill)
        parts.append(part)
    return parts

def is_in_grid(x, y):
    return 5 <= x <= 605 and 5 <= y <= 605

def clic(event):
    global c, original_coords, current_figure
    c = (c+1)%2
    if ( c == 1):
        cnv.bind("<Motion>",glisser)
        old[0]=event.x
        old[1]=event.y
        original_coords = cnv.coords(current_figure[0])
    else:
        cnv.unbind("<Motion>")
        deposer(event.x,event.y)

def glisser(event):
    dx = event.x - old[0]
    dy = event.y - old[1]
    for part in current_figure:
        cnv.move(part, dx, dy)
    old[0] = event.x
    old[1] = event.y

def deposer(x,y):
    global current_figure
    size = 100  # размер клетки
    # Выравниваем координаты по сетке
    x = round(x / size) * size
    y = round(y / size) * size
    if is_in_grid(x, y):
        # Удаляем старую фигуру
        for part in current_figure:
            cnv.delete(part)
        # Создаем новую фигуру на игровом поле
        current_figure = create_figure(cnv, x, y, current_figure_pattern)
    else:
        # Возвращаем фигуру на исходное место
        x1, y1, x2, y2 = cnv.coords(current_figure[0])
        for part in current_figure:
            cnv.move(part, original_coords[0] - x1, original_coords[1] - y1)

old=[None, None]
original_coords = [None, None]
global c
c = 0
root = Tk()
cnv = Canvas(root, width=800, height=650)
cnv.pack()

tetris_g_figure = [(0, 0), (0, 1), (1, 1), (2, 1)]
tetris_i_figure = [(0, 0), (0, 1), (0, 2), (0, 3)]

current_figure_pattern = tetris_g_figure
current_figure = create_figure(cnv, 620, 30, current_figure_pattern)

for i in range(7):
    cnv.create_line(5,5+100*i,605,5+100*i)
    cnv.create_line(5+100*i,5,5+100*i,605)

cnv.bind("<Button-1>",clic)

root.mainloop()