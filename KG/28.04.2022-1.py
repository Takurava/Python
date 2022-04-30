from tkinter import Canvas, Tk, Frame, BOTH
import math
from random import randrange

pi = math.pi


def polar(point1, point2, alfa=0):
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


class RandomShell(Frame):
  def __init__(self, canvas, left=(0, 0), right=(400, 400), count_of_points=20, dash=None, r=2):
    super().__init__()
    self.pack(fill=BOTH, expand=1)

    points = [(randrange(left[0], right[0]), randrange(left[1], right[1])) for i in range(count_of_points)]

    for point in points:
      canvas.create_oval((point[0] - r, point[1] - r, point[0] + r, point[1] + r), fill='red')

    min_point = min(points, key=lambda p: p[1])
    points.sort(key=lambda p: polar(min_point, p))

    steck = []
    steck.append(points[0])
    steck.append(points[1])

    for i in range(2, count_of_points):
      p1 = steck[-2]
      p2 = steck[-1]
      p3 = points[i]

      while (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0]) <= 0:
        steck.pop()
        p1 = steck[-2]
        p2 = steck[-1]
      else:
        steck.append(points[i])

    for i in range(len(steck)):
      canvas.create_line((steck[i - 1][0], steck[i - 1][1], steck[i][0], steck[i][1]), dash=dash)

    canvas.pack(fill=BOTH, expand=1)


root = Tk()
c = Canvas(root, width=600, height=600, bg='white')
ex1 = RandomShell(c)

root.geometry('600x600+300+300')
root.mainloop()
