import pygame
import keyboard
from sys import exit
import tkinter as tk
from io import BytesIO
from time import sleep
from OpenGL.GL import *
from random import choice
from os.path import abspath
from itertools import cycle
from base64 import b64decode
from math import cos,sin,radians
from tkinter import filedialog as fd
from string import ascii_uppercase,digits
from pygame.locals import DOUBLEBUF,OPENGL

x,y = 400,400

root = tk.Tk()
root.title('Abstractor - Gavin McAfee | gavinjmcafee@gmail.com')
root.configure(bg="white")
root.tk_setPalette(background='white')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

frame = tk.Frame(root, bg='white')
frame.pack()

lenLabel = tk.Label(frame, text="Length (Default: 0.1):")
lenLabel.grid(row=0, column=0, padx=5, pady=5, sticky="w")

length = tk.Entry(frame)
length.grid(row=0,column=1,padx=5,pady=5)

depLabel = tk.Label(frame, text="Depth (Past 20,000 gets laggy | No commas | Default: 3000):")
depLabel.grid(row=1, column=0, padx=5, pady=5, sticky="w")

depth = tk.Entry(frame)
depth.grid(row=1,column=1,padx=5,pady=5)

angLabel = tk.Label(frame, text="Angles (Separate with commas):")
angLabel.grid(row=2, column=0, padx=5, pady=5, sticky="w")

angle = tk.Entry(frame)
angle.grid(row=2,column=1,padx=5,pady=5)

zoomLabel = tk.Label(frame, text="Zoom (Default: 1.0):")
zoomLabel.grid(row=3, column=0, padx=5, pady=5, sticky="w")

zoomie = tk.Entry(frame)
zoomie.grid(row=3,column=1,padx=5,pady=5)

def select_file():
    filetypes = (
        ('Snapshot files', '*.snap'),
        ('All files', '*.*')
    )

    fileName = fd.askopenfilename(title='Open a Snapshot', filetypes=filetypes)
    if fileName:
        filePath = abspath(fileName)
        with open(filePath, 'r') as f:
            global lengths,angles,scale,oDept,leng,val,origLeng,origDept,origVal,origScale,x,y
            b = f.read()
            q = b.split(':')
            lengV = q[0]
            deptV = q[1]
            angsV = q[2]
            zoomV = q[3]
            if lengV == 'def':
                leng = 0.1
            else:
                leng = float(lengV)
            if deptV == 'def':
                oDept = 3000
            else:
                oDept = int(deptV)
            if angsV == 'def':
                val ='1,10,2,9,3,8,4,7,5,6'
            else:
                val = angsV
            if zoomV == 'def':
                scale = 1.0
            else:
                scale = float(zoomV)
            if len(q) > 4:
                if q[4] == 'cen':
                    x = 400
                else:
                    x = float(q[4])
            else:
                x = 400
            if len(q) > 5:
                if q[5] == 'cen':
                    y = 400
                else:
                    y = float(q[5])
            else:
                y = 400
            for i in enumerate(q):
                print(i)
            origLeng = leng
            origDept = oDept
            origVal = val
            origScale = scale
            values = angsV.split(',')
            lengths = [leng+(0.1*i) for i in range(oDept)]
            angles = [float(value) * l for l, value in zip(range(oDept), cycle(values))]
            root.destroy()

snapshot = tk.Button(root, text="Open a Snapshot", command=select_file)
snapshot.pack(padx=5, pady=5)

def get_user_input():
    global scale,oDept,lengths,angles,leng,val,origLeng,origDept,origVal,origScale
    scale = zoomie.get()
    if scale == '':
        scale = 1.0
    else:
        scale = float(zoomie.get())
    oDept = depth.get()
    if oDept == '':
        oDept = 3000
    else:
        oDept = int(depth.get())
    leng = length.get()
    if leng == '':
        leng = 0.1
    else:
        leng = float(length.get())
    val = angle.get()
    if val == '':
        val = '1,10,2,9,3,8,4,7,5,6'
    origLeng = leng
    origDept = oDept
    origVal = val
    origScale = scale
    values = val.split(',')
    lengths = [leng+(0.1*i) for i in range(oDept)]
    angles = [float(value) * l for l, value in zip(range(oDept), cycle(values))]
    root.destroy()

create = tk.Button(root, text='Create', command=get_user_input)
create.pack(padx=5,pady=5)
create.focus_set()

def on_closing():
    exit()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

def draw_line_with_angles(x, y, lengths, angles, scale):
    x1, y1 = x, y
    for length, angle in zip(lengths, angles):
        x2 = x1 + length * 10 * scale * cos(radians(float(angle)))
        y2 = y1 + length * 10 * scale * sin(radians(float(angle)))
        glBegin(GL_LINES)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glEnd()
        x1, y1 = x2, y2
moveNum = 25
nein = 0
def on_key_event(event):
    global scale,x,y,leng,origLeng,origDept,origVal,origScale,x,y,nein
    if event.event_type == keyboard.KEY_DOWN:
        global moveNum
        if event.name == "right":
            x -= moveNum / scale
        elif event.name == "left":
            x += moveNum / scale
        elif event.name == "up":
            y -= moveNum / scale
        elif event.name == "down":
            y += moveNum / scale
        elif event.name == "0":
            scale = 1.0
            x, y = 400, 400
        elif event.name == "c":
            x, y = 400, 400
        elif event.name == "=":
            scale = scale * 1.05
        elif event.name == "-":
            scale = scale / 1.05
        elif event.name == "u":
            moveNum = int(moveNum * 1.5)
        elif event.name == "d":
            moveNum = int(moveNum / 1.5)
        elif event.name == "r":
            moveNum = 25
        elif event.name == "o":
            scale = 1.0
        elif event.name == "s":
            if nein == 1:
                pass
            else:
                try:
                    nein = 1
                    files = [("Snapshot file","*.snap")]
                    tName = ''.join([''.join(choice(ascii_uppercase + digits)) for i in range(20)][0:-1])
                    folder = fd.asksaveasfile(filetypes=files,defaultextension=files,initialfile=tName)
                    with open(folder, "w") as fo:
                        if origLeng == 0.1:
                            origLeng = 'def'
                        if origDept == 3000:
                            origDept = 'def'
                        if origVal == '1,10,2,9,3,8,4,7,5,6':
                            origVal = 'def'
                        if scale == 1.0:
                            origScale = 'def'
                        else:
                            origScale = scale
                        if x == 400:
                            xV = 'cen'
                        else:
                            xV = x
                        if y == 400:
                            yV = 'cen'
                        else:
                            yV = y
                        fo.write(str(origLeng)+':'+str(origDept)+':'+str(origVal)+':'+str(origScale)+':'+str(xV)+':'+str(yV))
                    sleep(1)
                    nein = 0
                except:
                    nein = 0

keyboard.hook(on_key_event)

window_size = (800,800)
pygame.init()
icon = BytesIO(b64decode('AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAADz8/P/8/Pz//Pz8//z8/P/8/Pz//Pz8//z8/P/8/Pz//Pz8//z8/P/8/Pz//Pz8//z8/P/8/Pz//Pz8//z8/P/8/Pz//Pz8//z8/P/8/Pz//Pz8//z8/P/8/Pz//Pz8//z8/P/8/Pz//Pz8//z8/P/8/Pz//Pz8//z8/P/8/Pz/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5+fn/+bm5v/l5eX/5OTk/+Pj4//k5OT/5ubm/+fn5//n5+f/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+Xl5f/h4eH/2tra/9XV1f/Q0ND/0NDQ/8/Pz//Ozs7/1tbW/+Li4v/n5+f/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/j4+P/29vb/9fX1//U1NT/1NTU/9LS0v/S0tL/0NDQ/8vLy//Gxsb/xMTE/9PT0//l5eX/5+fn/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/4eHh/9nZ2f/X19f/2NjY/9jY2P/Y2Nj/19fX/9XV1f/U1NT/1NTU/9HR0f/Ly8v/wMDA/8bGxv/h4eH/5+fn/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+Li4v/Z2dn/2NjY/9jY2P/Y2Nj/2dnZ/9nZ2f/Y2Nj/2NjY/9fX1//W1tb/1dXV/9PT0//Q0ND/v7+//76+vv/i4uL/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/l5eX/29vb/9jY2P/Y2Nj/19fX/9jY2P/Y2Nj/2NjY/9jY2P/Z2dn/2NjY/9fX1//X19f/1NTU/9TU1P/R0dH/uLi4/8DAwP/l5eX/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+Hh4f/Y2Nj/2tra/9XV1f/Ly8v/vLy8/7Kysv+wsLD/uLi4/8XFxf/U1NT/2dnZ/9fX1//V1dX/1dXV/9XV1f/Ly8v/qqqq/9DQ0P/n5+f/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/3d3d/9jY2P/Hx8f/qKio/5ubm/+YmJj/mZmZ/5mZmf+Wlpb/lZWV/52dnf+9vb3/1tbW/9bW1v/V1dX/1dXV/9PT0/+3t7f/srKy/+Pj4//m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/Y2Nj/tra2/5ycnP+hoaH/qqqq/62trf+rq6v/pqam/6Ghof+enp7/lJSU/4yMjP+vr6//1NTU/9XV1f/T09P/0NDQ/7+/v/+np6f/0tLS/+fn5//m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/4uLi/7Kysv+bm5v/qqqq/7CwsP+urq7/rKys/6enp/+ioqL/np6e/5ycnP+Xl5f/lZWV/4yMjP+zs7P/y8vL/8XFxf/ExMT/tra2/6Ojo/+7u7v/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/BwcH/n5+f/6urq/+ysrL/sLCw/6ysrP+lpaX/nJyc/5KSkv+NjY3/ioqK/4yMjP+Wlpb/kpKS/4ODg/+ysrL/wcHB/7y8vP+ysrL/qKio/6enp//c3Nz/5eXl/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/n5+f/09PT/6enp/+ysrL/vb29/8HBwf+/v7//sbGx/5aWlv95eXn/a2tr/3V1df+Ghob/fn5+/4CAgP+SkpL/d3d3/5ubm/+4uLj/sLCw/7CwsP+oqKj/oaGh/9PT0//e3t7/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+Tk5P+1tbX/tbW1/8vLy//IyMj/xcXF/8LCwv+ysrL/cnJy/2ZmZv90dHT/bGxs/3d3d/+fn5//gICA/4CAgP9wcHD/fn5+/6Wlpf+pqan/ra2t/6enp/+goKD/1NTU/9ra2v/i4uL/5ubm/+bm5v/m5ub/5ubm/+bm5v/n5+f/1NTU/6+vr//Nzc3/0tLS/9DQ0P/FxcX/u7u7/4aGhv9sbGz/g4OD/3Nzc/9/f3//eHh4/4WFhf+ioqL/dXV1/21tbf9zc3P/np6e/6ioqP+qqqr/oqKi/6Kiov/W1tb/29vb/93d3f/l5eX/5ubm/+bm5v/m5ub/5ubm/+fn5//ExMT/vb29/9PT0//U1NT/1tbW/9XV1f+tra3/fHx8/4mJif95eXn/jIyM/66urv+dnZ3/m5ub/5ubm/9paWn/Z2dn/3t7e/+goKD/p6en/6enp/+dnZ3/r6+v/9ra2v/Z2dn/2dnZ/+Pj4//m5ub/5ubm/+bm5v/m5ub/5OTk/7+/v//Hx8f/09PT/9bW1v/X19f/09PT/5qamv+MjIz/j4+P/3x8fP+goKD/c3Nz/5qamv+MjIz/ampq/3BwcP97e3v/hYWF/56env+ioqL/oaGh/5eXl//CwsL/29vb/9jY2P/X19f/4ODg/+bm5v/m5ub/5ubm/+bm5v/h4eH/u7u7/83Nzf/V1dX/19fX/9fX1//Nzc3/lJSU/5eXl/+Tk5P/fX19/4+Pj/9oaGj/l5eX/6ioqP+YmJj/kpKS/39/f/+RkZH/n5+f/6Ojo/+bm5v/oqKi/9bW1v/a2tr/19fX/9XV1f/g4OD/5ubm/+bm5v/m5ub/5ubm/+Dg4P/AwMD/z8/P/9bW1v/X19f/19fX/8jIyP+VlZX/np6e/5eXl/+CgoL/fX19/3Jycv9ubm7/goKC/4SEhP94eHj/i4uL/5ycnP+ioqL/nZ2d/5WVlf/ExMT/2dnZ/9nZ2f/X19f/1NTU/9/f3//m5ub/5ubm/+bm5v/m5ub/4uLi/8XFxf/Q0ND/19fX/9jY2P/X19f/y8vL/5iYmP+jo6P/n5+f/5CQkP93d3f/ZmZm/3V1df+AgID/hISE/5GRkf+dnZ3/oqKi/5iYmP+RkZH/uLi4/9nZ2f/X19f/19fX/9bW1v/T09P/4ODg/+bm5v/m5ub/5ubm/+bm5v/k5OT/zMzM/8/Pz//W1tb/19fX/9bW1v/R0dH/nZ2d/5+fn/+mpqb/oaGh/5SUlP98fHz/ZWVl/2hoaP97e3v/kJCQ/5OTk/+QkJD/lpaW/7y8vP/X19f/2NjY/9fX1//Y2Nj/1NTU/9TU1P/j4+P/5ubm/+bm5v/m5ub/5ubm/+bm5v/V1dX/zs7O/9bW1v/X19f/1tbW/9XV1f+urq7/lpaW/6mpqf+rq6v/pKSk/6Ghof+enp7/mJiY/42Njf+Xl5f/pqam/7e3t//MzMz/1tbW/9bW1v/W1tb/19fX/9XV1f/R0dH/2dnZ/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/9/f3//Q0ND/1dXV/9bW1v/W1tb/1tbW/8vLy/+bm5v/o6Oj/6urq/+qqqr/qamp/7Gxsf+/v7//vb29/8bGxv/U1NT/1dXV/9XV1f/W1tb/1dXV/9bW1v/W1tb/0tLS/9LS0v/i4uL/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5eXl/9jY2P/U1NT/19fX/9fX1//X19f/19fX/7y8vP+Xl5f/pKSk/6mpqf+rq6v/sbGx/8HBwf/Dw8P/y8vL/9XV1f/W1tb/1dXV/9bW1v/W1tb/1dXV/9PT0//Pz8//3Nzc/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/4+Pj/9fX1//W1tb/19fX/9fX1//X19f/1tbW/7a2tv+YmJj/oqKi/6mpqf+tra3/vLy8/8bGxv/R0dH/1tbW/9fX1//W1tb/1dXV/9XV1f/R0dH/zMzM/9jY2P/l5eX/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/4uLi/9fX1//W1tb/19fX/9jY2P/Y2Nj/2NjY/8DAwP+ioqL/m5ub/6Kiov+tra3/v7+//9DQ0P/T09P/09PT/9LS0v/Nzc3/xsbG/8jIyP/Z2dn/5eXl/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/4uLi/9vb2//X19f/2NjY/9fX1//Y2Nj/2tra/9HR0f+3t7f/paWl/6Kiov+qqqr/rq6u/7Kysv+2trb/urq6/76+vv/Pz8//4eHh/+fn5//m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5eXl/+Hh4f/d3d3/3d3d/9nZ2f/Z2dn/3Nzc/9/f3//e3t7/2NjY/9DQ0P/Jycn/ycnJ/9HR0f/b29v/4+Pj/+fn5//m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/l5eX/5OTk/+Tk5P/l5eX/5ubm/+bm5v/n5+f/5+fn/+fn5//n5+f/5+fn/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/5ubm/+bm5v/m5ub/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='))
iconScr = pygame.image.load(icon)
pygame.display.set_icon(iconScr)
window = pygame.display.set_mode(window_size, DOUBLEBUF | OPENGL)
pygame.display.set_caption("Abstractor - Gavin McAfee | gavinjmcafee@gmail.com")

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, window_size[0], 0, window_size[1], -1, 1)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glClearColor(0.9, 0.9, 0.9, 1)

glColor(0, 0, 0)
glLineWidth(1)

firstTime = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            keyboard.unhook_all()
            exit()

    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-window_size[0], window_size[0], -window_size[1], window_size[1], -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glScalef(scale, scale, 0)

    if firstTime:
        glTranslatef(-window_size[0] / 2, -window_size[1] / 2, 0)

    draw_line_with_angles(x,y,lengths,angles,1)

    pygame.display.flip()