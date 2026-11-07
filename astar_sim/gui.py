import tkinter as tk
from turtle import RawTurtle
from tkinter import filedialog
from tkinter import messagebox
from math import sqrt
from astar import getPath

map = None
n = None    # map height
m = None    # and width in squares
square = 25 # map square size

def promptError():
    tk.messagebox.showinfo(title="Error!", message="Please select a file.")

def drawEmpty():
    turtle.up()
    turtle.lt(45)
    turtle.fd(sqrt(square)*2)
    turtle.rt(45)
    turtle.down()
    for i in range (4):
        turtle.fd(square/2)
        turtle.lt(90)
    turtle.up()
    turtle.lt(45)
    turtle.bk(sqrt(square)*2)
    turtle.rt(45)
    turtle.down()
def drawFilled():
    turtle.begin_fill()
    for i in range (4):
        turtle.fd(square)
        turtle.lt(90)
    turtle.end_fill()
def drawStart():
    turtle.fillcolor("red")
    drawFilled()
    turtle.fillcolor("black")
def drawGoal():
    turtle.fillcolor("green")
    drawFilled()
    turtle.fillcolor("black")

def drawMap():
    if map == None:
        promptError()
        return

    turtle.up()
    turtle.clear()
    turtle.home()
    turtle.setpos(-square*n/2, square*m/2)
    turtle.down()
    turtle.rt(90)

    #tk.messagebox.showinfo(title="Map:", message='\n'.join(map))

    turtle.ht()
    turtle.speed(10)
    for j in range(m):
        for i in range (n):
            if (map[i][j] == '0'):
                drawEmpty()
            if (map[i][j] == '1'):
                drawFilled()
            if(map[i][j] == 'S'):
                drawStart()
            if(map[i][j] == 'G'):
                drawGoal()
            turtle.up()
            turtle.fd(square)
            turtle.down()
        turtle.up()
        turtle.bk(square*n)
        turtle.lt(90)
        turtle.fd(square)
        turtle.rt(90)
        turtle.down()
    for i in range (4):
        turtle.fd(n*square)
        turtle.rt(90)
    turtle.st()
    turtle.screen.update()

def browseImage():
    global filename
    filename = filedialog.askopenfilename(initialdir = ".",
        title = "Select a file",
        filetypes = (("Text files ", "*txt*"),
                    ("All files", "*.*")) )
    fileName.configure(text=filename)
    with open(filename, "r") as f:
        global map, n, m
        map = [line.strip() for line in f if line.strip()]
        n = len(map)
        if n == 0:
            promptError()
            return
        m = len(map[0])
        for i in range (0, n, 1):
            if (len(map[i]) != m):
                promptError()
                return

def turtleGoTo(i, j):
    turtle.setpos(-square*n/2 + j*square + square/2, 
                square*m/2 - i*square - square/2)

def calculatePath():
    # todo: fetch path from astar.py and draw it using turtleGoTo
    path = getPath(filename)
    print(path)
    turtle.width(5)
    turtle.color("blue")
    turtle.up()
    for node in path:
        turtleGoTo(node[0], node[1])
        turtle.screen.update()
        turtle.down()
    turtle.width(1)
    turtle.color("black")

def main():
    root = tk.Tk()
    root.title("A* path finder simulation")

    global fileName, turtle, canvas
    fileName = tk.Label(root, text="- Choose a map -")
    fileName.pack()
    tk.Button(root, text="Browse image", width=25, command=browseImage).pack()
    tk.Button(root, text="Draw map", width=25, command=drawMap).pack()
    tk.Button(root, text="Calculate path", width=25, command=calculatePath).pack()

    canvas = tk.Canvas(root, width = 1000, height = 500)
    canvas.pack()

    turtle = RawTurtle(canvas)
    turtle.screen.tracer(0)

    root.mainloop()

if __name__ == "__main__":
    main()