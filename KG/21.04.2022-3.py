from tkinter import Canvas, Tk, Frame, BOTH
import math
from random import randrange

pi = math.pi


def polar(point1, point2):
  x = float(point2[0] - point1[0])
  y = float(point2[1] - point1[1])
  if x == 0:
    if y == 0:
       return 0
    if y > 0:
      return pi / 2.0
    else:
      return 3 * pi / 2.0

  if x < 0:
    return math.atan(y / x) + pi

  if x > 0:
    angle = math.atan(y / x)
    if y >= 0:
      return angle
    else:
      return angle + 2.0 * pi

  return -1


class RandomPolygon(Frame):
  def __init__(self, canvas, left=(0, 0), right=(400, 400), count_of_points = 20, dash=None):
    super().__init__()
    self.pack(fill=BOTH, expand=1)
    points = [(randrange(left[0], right[0]), randrange(left[1], right[1])) for i in range(count_of_points)]
    min_point = min(points, key=lambda p: p[1])
    print(points, min_point)
    for i in range(len(points)):
      point = points[i]
      points[i] = (point[0], point[1], polar(min_point, points[i]))
    points.sort(key=lambda p: p[2]+pi)
    print(points)
    for i in range(len(points)):
      canvas.create_line((points[i-1][0], points[i-1][1], points[i][0], points[i][1]), dash=dash)
    canvas.pack(fill=BOTH, expand=1)



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
    self.frame = canvas.create_oval((x-r, y-r, x+r, y+r), fill='red')
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

root = Tk()
c = Canvas(root, width=1000, height=1000, bg='white')
ex1 = RandomPolygon(c)

root.geometry('600x600+300+300')
root.mainloop()
