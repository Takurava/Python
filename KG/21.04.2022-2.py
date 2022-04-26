from tkinter import Canvas, Tk, Frame, BOTH
import math
from random import randrange

pi = math.pi


class Triangle(Frame):
  def __init__(self, canvas, x=0, y=0, a=100, dash=None):
    super().__init__()
    cos30 = math.cos(pi/6)
    self.pack(fill=BOTH, expand=1)
    canvas.create_line((x, y, x + a, y), dash=dash)
    canvas.create_line((x, y, x + a/2, y + cos30 * a), dash=dash)
    canvas.create_line((x + a/2, y + cos30 * a, x + a, y), dash=dash)
    canvas.pack(fill=BOTH, expand=1)


class Ellipse(Frame):
  def __init__(self, canvas, x=0, y=0, r=100):
    super().__init__()
    cos30 = math.cos(pi/6)
    self.pack(fill=BOTH, expand=1)
    canvas.create_oval((x-r, y-r, x+r, y+r), fill='red')
    canvas.pack(fill=BOTH, expand=1)


def get_color():
  while True:
    color = f'#{randrange(100000, 999999)}'
    yield color


class PiChart(Frame):
  def __init__(self, canvas, x=0, y=0, r=100, *args):
    super().__init__()
    alfa = [a*360/sum(args) for a in args]
    start_a = 0
    for a in alfa:
      self.pack(fill=BOTH, expand=1)
      canvas.create_arc((x-r, y-r, x+r, y+r), start=start_a, extent=a, fill=next(get_color()))
      start_a = start_a + a
    canvas.pack(fill=BOTH, expand=1)

'''root = Tk()
x, y, a, r = 50, 50, 200, 40
c = Canvas(root, width=1000, height=1000, bg='white')
ex1 = Triangle(c, x, y, a, dash=(6, 6))
cos30 = math.cos(pi / 6)
ex2 = Ellipse(c, x+a/2, y+cos30*a/3, r)

ex3 = PiChart(c, 400, 400, 100, 123, 456, 234, 967)
root.geometry('600x600+300+300')
root.mainloop()'''

from tkinter import *
from tkinter import ttk

#Create an instance of Tkinter frame or window
win = Tk()

#Set the geometry of tkinter frame
win.geometry("750x250")
def callback():
   Label(win, text="Hello World!", font=('Georgia 20 bold')).pack(pady=4)

#Create a Label and a Button widget
btn = ttk.Button(win, text="Press Enter to Show a Message", command= callback)
btn.pack(ipadx=10)

win.bind('<Return>',lambda event:callback())

win.mainloop()

