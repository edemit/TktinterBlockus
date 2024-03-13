from tkinter import Tk, Canvas

def create_figure(cnv, x, y, figure, size=100, fill='red'):
    # Создаем части фигуры в соответствии с переданным шаблоном
    parts = []
    for dx, dy in figure:
        part = cnv.create_rectangle(x+dx*size, y+dy*size, x+(dx+1)*size, y+(dy+1)*size, fill=fill)
        parts.append(part)
    # Возвращаем части фигуры как список
    return parts

def clic(event):
    global c
    c = (c+1)%2
    if ( c == 1):
        cnv.bind("<Motion>",glisser)
        old[0]=event.x
        old[1]=event.y
    else:
        cnv.unbind("<Motion>")
        deposer(event.x,event.y)

def glisser(event):
    for part in current_figure:
        x1, y1, x2, y2 = cnv.coords(part)
        if (old[0] >= x1 and old[0] <= x2 and old[1] >= y1 and old[1] <= y2):
            cnv.move(part, event.x-old[0], event.y-old[1])
    old[0]=event.x
    old[1]=event.y

def deposer(x,y):
    # Получаем координаты первой части фигуры
    x1, y1, x2, y2 = cnv.coords(current_figure[0])
    # Вычисляем смещение
    dx = x - x1
    dy = y - y1
    # Перемещаем все части фигуры
    for part in current_figure:
        cnv.move(part, dx, dy)
    # Создаем новую фигуру после размещения старой
    current_figure = create_figure(cnv, 620, 30, current_figure_pattern)

# pgm principal

old=[None, None]
global c
c = 0
root = Tk()
cnv = Canvas(root, width=800, height=650)
cnv.pack()

tetris_g_figure = [(0, 0), (0, 1), (1, 1), (2, 1)]  # Фигура "Г"
tetris_i_figure = [(0, 0), (0, 1), (0, 2), (0, 3)]  # Фигура "I"

current_figure_pattern = tetris_g_figure
current_figure = create_figure(cnv, 620, 30, current_figure_pattern)

for i in range(7):
    cnv.create_line(5,5+100*i,605,5+100*i)
    cnv.create_line(5+100*i,5,5+100*i,605)

cnv.bind("<Button-1>",clic)

root.mainloop()