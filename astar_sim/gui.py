import tkinter as tk
from turtle import RawTurtle
from tkinter import filedialog
from tkinter import messagebox
from math import sqrt
from astar import getPath
from build_map import buildMap

map = None
n = None    # map height
m = None    # and width in squares
goal = (-1, -1)
start = (0, 0)
waiting_for_click = False
canvas_width = 1000
canvas_height = 500

def promptError():
    tk.messagebox.showinfo(title="Error!", message="Please select a file.")

def drawEmpty():
    turtle.up()
    turtle.fd(1)
    turtle.down()
    return
def drawFilled():
    turtle.fd(1)
    return
def drawStart():
    turtle.fillcolor("red")
    draw_centered_circle(5)
    turtle.fillcolor("black")
def drawGoal():
    turtle.fillcolor("green")
    draw_centered_circle(5)
    turtle.fillcolor("black")
def draw_centered_circle(radius):
    turtle.up()
    turtle.bk(radius)
    turtle.down()
    turtle.rt(90)

    turtle.begin_fill()
    turtle.circle(radius)
    turtle.end_fill()

    turtle.lt(90)
    turtle.up()
    turtle.fd(radius)
    turtle.down()

def drawMap():
    if map is None:
        promptError()
        return

    turtle.up()
    turtle.clear()
    turtle.home()
    turtle.setpos(-m/2, n/2)
    turtle.down()
    turtle.rt(90)

    #turtle.ht()
    turtle.speed(10)
    for j in range(m):
        for i in range (n):
            if (map[i][j] == '0'):
                drawEmpty()
            if (map[i][j] == '1'):
                drawFilled()
            if(map[i][j] == 'S'):
                global start
                start = (i, j)
                drawStart()
            if(map[i][j] == 'G'):
                global goal
                goal = (i, j)
                drawGoal()
            # turtle.up()
            # turtle.fd(1)
            # turtle.down()
        turtle.up()
        turtle.bk(n)
        turtle.lt(90)
        turtle.fd(1)
        turtle.rt(90)
        turtle.down()
    for i in range (2):
        turtle.fd(n)
        turtle.rt(90)
        turtle.fd(m)
        turtle.rt(90)
    #turtle.st()
    turtle.screen.update()

def browseImage():
    global mapFileName
    mapFileName = 'map_big.txt'
    # mapFileName = filedialog.askopenfilename(initialdir = ".",
    #     title = "Select a file",
    #     filetypes = (("Text files ", "*txt*"),
    #                 ("All files", "*.*")) )
    fileName.configure(text=mapFileName)
    with open(mapFileName, "r") as f:
        global map, n, m, goal
        map = [list ( line.strip() ) for line in f if line.strip()]
        n = len(map)
        if n == 0:
            promptError()
            return
        m = len(map[0])
        goal = (n-1, m-1)
        for i in range (0, n, 1):
            if (len(map[i]) != m):
                promptError()
                return

def turtleGoTo(i, j, penup=False):
    if penup:
        turtle.up()
    turtle.setpos(-m/2 + j, 
                n/2 - i)
    turtle.down()

#draws the path from start to goal on the canvas
def calculatePath():
    print("Drawing the path...")
    path = getPath(mapFileName)
    turtle.width(5)
    turtle.color("blue")
    turtle.up()
    for node in path:
        turtleGoTo(node[0], node[1])
        turtle.screen.update()
        turtle.down()
    turtle.width(1)
    turtle.color("black")
    print("Path drawing finished!")

# initiates the new goal pick
def pickGoal():
    global waiting_for_click
    waiting_for_click = 1
    print("Pick the new goal!")
    canvas.config(cursor="hand1")

#initiates the new start pick
def pickStart():
    global waiting_for_click
    waiting_for_click = 2
    print("Pick the new start!")
    canvas.config(cursor="hand1")

# ends the new goal/start pick
def on_canvas_click(event):
    global waiting_for_click

    # pick goal
    if waiting_for_click > 0:
        print("waiting_for_click is True")
        if map is None:
            promptError()
            return

        global canvas_width, canvas_height

        top_left_y = (canvas_width / 2) - (m/2)
        top_left_x = (canvas_height / 2) - (n/2)

        i = int(event.y - top_left_x)
        j = int(event.x - top_left_y)

        if waiting_for_click == 1:
            global goal
            map[goal[0]][goal[1]] = '0'
            goal = (i, j)
            map[goal[0]][goal[1]] = 'G'
            print(f"New start picked: {goal}")
            turtleGoTo(i, j, penup=True)
            drawGoal()
        elif waiting_for_click == 2:
            global start
            map[start[0]][start[1]] = '0'
            start = (i, j)
            map[start[0]][start[1]] = 'S'
            print(f"New goal picked: {start}")
            turtleGoTo(i, j, penup=True)
            drawStart()

        waiting_for_click = False
        canvas.config(cursor="")
        buildMap(start=start, goal=goal)

def main():
    global root, canvas, turtle, canvas_width, canvas_height
    root = tk.Tk()
    root.title("A* path finder simulation")
    buildMap()

    global fileName, turtle, canvas
    fileName = tk.Label(root, text="- Choose a map -", width=100, borderwidth=1, relief="sunken")
    fileName.grid(row=0, column=0, columnspan=3)
    tk.Button(root, text="Browse image", width=25, command=browseImage).grid(row=1, column=0)
    tk.Button(root, text="Draw map", width=25, command=drawMap).grid(row=2, column=0)
    tk.Button(root, text="Calculate path", width=25, command=calculatePath).grid(row=3, column=0)
    canvas = tk.Canvas(root, width = canvas_width, height = canvas_height)
    canvas.grid(row=4, column=0, columnspan=3)
    tk.Button(root, text="Pick new goal", width=25, command=pickGoal).grid(row=1, column=2)
    tk.Button(root, text="Pick new start", width=25, command=pickStart).grid(row=2, column=2)

    turtle = RawTurtle(canvas)
    turtle.screen.tracer(0)
    
    canvas.bind("<Button-1>", on_canvas_click)

    root.mainloop()

if __name__ == "__main__":
    main()