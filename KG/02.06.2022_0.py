import math
import numpy as np
class point():
    def __init__(self, arr):
        self.x = arr[0]
        self.y = arr[1]
        self.z = arr[2]

def turning_y(point, alpha):
    tmatrix = np.zeros([3, 3])
    cosa = math.cos(alpha)
    sina = math.sin(alpha)
    tmatrix[0, 0] = cosa
    tmatrix[0, 1] = -sina
    tmatrix[1, 0] = sina
    tmatrix[1, 1] = cosa
    tmatrix[2, 2] = 1
    return np.dot(tmatrix, np.array([point.x, point.y, point.z]))
def turning_x(point, alpha):
    tmatrix = np.zeros([3, 3])
    cosa = math.cos(alpha)
    sina = math.sin(alpha)
    tmatrix[0, 0] = cosa
    tmatrix[0, 2] = sina
    tmatrix[1, 1] = 1
    tmatrix[2, 0] = -sina
    tmatrix[2, 2] = cosa
    return np.dot(tmatrix, np.array([point.x, point.y, point.z]))

from tkinter import *
root = Tk()
canv = Canvas(root, width = 1000, height = 1000, bg = "white")
canv.focus_set()
canv.pack()
a = 100
p1 = point([-a/2, a/2, a/2])
p2 = point([-a/2, -a/2, a/2])
p3 = point([-a/2, -a/2, -a/2])
p4 = point([-a/2, a/2, -a/2])
p5 = point([a/2, a/2, a/2])
p6 = point([a/2, a/2, -a/2])
p7 = point([a/2, -a/2, -a/2])
p8 = point([a/2, -a/2, a/2])
points = [p1, p2, p3, p4, p5, p6, p7, p8]
for i in range(8):
    points[i] = point(list(turning_y(points[i], math.pi/3)))
    points[i] = point(list(turning_x(points[i], math.pi/3)))

cube = [[points[0], points[4], points[5], points[3]], [points[1], points[7], points[4], points[0]], [points[7], points[6], points[5], points[4]], [points[6], points[2], points[3], points[5]], [points[2], points[1], points[0], points[3]], [points[6], points[7], points[1], points[2]]]


func = lambda x: [x.x + a, x.y + a]
func(p1)

def s(grane):
    x0, x1, x2, x3 = grane[0].x, grane[1].x, grane[2].x, grane[3].x
    y0, y1, y2, y3 = grane[0].y, grane[1].y, grane[2].y, grane[3].y
    S = (x0 - x1) *(y0 + y1) + (x1 - x2) *(y1 + y2) + (x2 - x3) *(y2 +y3) + (x3 -x0 ) *(y3 +y0)
    return S < 0

def polina(points):
    return min(points, key=lambda x: x.z)

def ocp(p, me=point([0, 0, 1000]), surface_z=800):

    x = (surface_z - p.z) * (me.x - p.x) / (me.z - p.z) + p.x
    y = (surface_z - p.z) * (me.y - p.y) / (me.z - p.z) + p.y
    z = 0

    return point([x, y, z])

def normale(p, cube):
    x, y, z = 0, 0, 0
    for c in cube:
        if p in c:
            x1, y1, z1 = p.x, p.y, p.z
            i = c.index(p)
            x2, y2, z2 = c[(i+1)%4].x, c[(i+1)%4].y, c[(i+1)%4].z
            x3, y3, z3 = c[(i+2)%4].x, c[(i+2)%4].y, c[(i+2)%4].z
            x += (z2-z1)*(y3-y1) - (y2-y1)*(z3-z1)
            y += (x2-x1)*(z3-z1) - (z2-z1)*(x3-x1)
            z += (y2-y1)*(x3-x1) - (x2-x1)*(y3-y1)
    length = (x**2 + y**2 + z**2) ** 0.5
    x, y, z = x/length, y/length, z/length
    return([x, y, z])

def fromLtoP(l, p):
    xl = l[0]-p.x
    yl = l[1]-p.y
    zl = l[2]-p.z
    length = (xl**2 + yl**2 + zl**2)**0.5
    return([xl/length, yl/length, zl/length])

def cosalph(l, n):
    xl, yl, zl = l[0], l[1], l[2]
    xn, yn, zn = n[0], n[1], n[2]
    return xl*xn + yl*yn + zl*zn

def distance(p, l):
    return ((p.x-l[0])**2 + (p.y-l[1])**2 + (p.z - l[2])**2)**0.5

def intensity(ambient, amp, K, cosa, d):
    return ambient + amp*cosa/(d+K)

a = 200
light = [-a, -a, -a]
ambient = 0.6
amp = 0.4
K = 0
distances = []
for p in points:
    distances.append(distance(p, light))
max(distances)

intensities = [[], [], [], [], [], []]
for p in points:
    n = normale(p, cube)
    l = fromLtoP(light, p)
    cosa = cosalph(l, n)
    d = distance(p, light)/max(distances)
    for i in range(6):
        if p in cube[i]:
            intensities[i].append(intensity(ambient, amp, K, cosa, d))
intensities = [sum(i)/len(i) for i in intensities]
intensities

def rgb_hack(rgb):
    r = max(min(255, rgb[0]), 0)
    g = max(min(255, rgb[1]), 0)
    b = max(min(255, rgb[2]), 0)
    return "#%02x%02x%02x" % (r, g, b)

root = Tk()
canv = Canvas(root, width = 1000, height = 1000, bg = "white")
canv.focus_set()
canv.pack()
for i, c in zip(intensities, cube):
    if polina(points) in c:
        canv.create_polygon(list(np.concatenate(list(map(func, c)))), fill=rgb_hack((255, int(255 - 255*i), 255)), outline='black')
root.mainloop()

class pointI:
    def __init__(self, x=0, y=0, z=0, I=0):
        self.x = x
        self.y = y
        self.z = z
        self.I = I


colors = ['red', 'green', 'black', 'blue', 'yellow', 'pink']
points1 = points.copy()

root = Tk()
canv = Canvas(root, width=1000, height=1000, bg="white")
canv.focus_set()
canv.pack()
for i, c in zip(intensities, cube):
    if polina(points) in c:
        canv.create_polygon(list(np.concatenate(list(map(func, c)))), fill=rgb_hack((255, int(255 - 255 * i), 255)),
                            outline='black')


def control(event):
    cube1 = cube.copy()
    if event.keysym == 'Left':
        canv.delete('all')
        for i in range(8):
            points1[i] = point(list(turning_x(points1[i], math.pi / 12)))
        cube1 = [[points1[0], points1[4], points1[5], points1[3]], [points1[1], points1[7], points1[4], points1[0]],
                 [points1[7], points1[6], points1[5], points1[4]], [points1[6], points1[2], points1[3], points1[5]],
                 [points1[2], points1[1], points1[0], points1[3]], [points1[6], points1[7], points1[1], points1[2]]]
        intensities = [[], [], [], [], [], []]
        pIntens = []
        for p in points1:
            n = normale(p, cube1)
            l = fromLtoP(light, p)
            cosa = cosalph(l, n)
            d = distance(p, light) / max(distances)
            pIntens.append((p, intensity(ambient, amp, K, cosa, d)))
            for i in range(6):
                if p in cube1[i]:
                    intensities[i].append(intensity(ambient, amp, K, cosa, d))
        intensities = [sum(i) / len(i) for i in intensities]
        for c, i in zip(cube1, intensities):
            # if s(c):
            if polina(points1) in c:
                # newc = list(map(ocp, c))
                point_grane_arr = []

                cI = []
                for p in c:
                    for pI in pIntens:
                        if p == pI[0]:
                            cI.append(pI[1])

                dx12 = (c[1].x - c[0].x) / a
                dy12 = (c[1].y - c[0].y) / a
                dI12 = (cI[1] - cI[0]) / a
                dx43 = (c[2].x - c[3].x) / a
                dy43 = (c[2].y - c[3].y) / a
                dI43 = (cI[2] - cI[3]) / a

                for i in range(0, a + 1):
                    x12 = c[0].x + dx12 * i
                    y12 = c[0].y + dy12 * i
                    I12 = cI[0] + dI12 * i
                    x43 = c[3].x + dx43 * i
                    y43 = c[3].y + dy43 * i
                    I43 = cI[3] + dI43 * i
                    point_grane_arr.append((pointI(x12, y12, 0, I12), pointI(x43, y43, 0, I43)))

                all_pointI = []
                for p1, p2 in point_grane_arr:
                    dx = (p2.x - p1.x) / a
                    dy = (p2.y - p1.y) / a
                    dI = (p2.I - p1.I) / a
                    for i in range(0, a + 1):
                        all_pointI.append(pointI(p1.x + dx * i, p1.y + dy * i, 0, p1.I + dI * i))
                        canv.create_oval(
                            (p1.x + dx * i + a, p1.y + dy * i + a, p1.x + dx * i + 1 + a, p1.y + dy * i + 1 + a),
                            fill=rgb_hack((255, int(255 - 255 * (p1.I + dI * i)), 255)))

                canv.create_polygon(list(np.concatenate(list(map(func, c)))), fill=rgb_hack((255, int(255 - 255*i), 255)), outline='black')
    if event.keysym == 'Right':
        canv.delete('all')
        for i in range(8):
            points1[i] = point(list(turning_x(points1[i], -math.pi / 12)))
        cube1 = [[points1[0], points1[4], points1[5], points1[3]], [points1[1], points1[7], points1[4], points1[0]],
                 [points1[7], points1[6], points1[5], points1[4]], [points1[6], points1[2], points1[3], points1[5]],
                 [points1[2], points1[1], points1[0], points1[3]], [points1[6], points1[7], points1[1], points1[2]]]
        intensities = [[], [], [], [], [], []]
        pIntens = []
        for p in points1:
            n = normale(p, cube1)
            l = fromLtoP(light, p)
            cosa = cosalph(l, n)
            d = distance(p, light) / max(distances)
            pIntens.append((p, intensity(ambient, amp, K, cosa, d)))
            for i in range(6):
                if p in cube1[i]:
                    intensities[i].append(intensity(ambient, amp, K, cosa, d))
        intensities = [sum(i) / len(i) for i in intensities]
        for c, i in zip(cube1, intensities):
            # if s(c):
            if polina(points1) not in c:
                # newc = list(map(ocp, c))
                i1 = 0
                for k, p in enumerate(c):
                    if p.y > c[i1].y or (p.y == c[i1].y and p.x < c[i1].x):
                        i1 = k

                cI = []
                for p in c:
                    for pI in pIntens:
                        if p == pI[0]:
                            cI.append(pI[1])

                p_versh = [pointI(c[ii % 4].x, c[ii % 4].y, 0, cI[ii % 4]) for ii in range(i1, i1 - 4, -1)]

                if p_versh[0].y == p_versh[1].y:
                    # Интерполяция от грани до грани
                    for yi in range(round(p_versh[0].y), round(p_versh[3].y)):
                        x1 = (yi - p_versh[0].y) * (p_versh[3].x - p_versh[0].x) / (p_versh[3].y - p_versh[0].y) + p_versh[0].x
                        x2 = (yi - p_versh[1].y) * (p_versh[2].x - p_versh[1].x) / (p_versh[2].y - p_versh[1].y) + p_versh[2].x
                        # Тут надо переделывать
                        t1 = ((x1 - p_versh[0].x) ** 2 + (yi - p_versh[0].y) ** 2) ** 0.5 / (
                                (p_versh[3].x - p_versh[0].x) ** 2 + (p_versh[3].y - p_versh[0].y) ** 2) ** 0.5
                        I1 = (1 - t1) * p_versh[0].I + t1 * p_versh[3].I
                        t2 = ((x2 - p_versh[1].x) ** 2 + (yi - p_versh[1].y) ** 2) ** 0.5 / (
                                (p_versh[2].x - p_versh[1].x) ** 2 + (p_versh[2].y - p_versh[1].y) ** 2) ** 0.5
                        I2 = (1 - t2) * p_versh[1].I + t2 * p_versh[2].I
                        # Переделывать до сюда
                        for xi in range(round(x1), round(x2)):
                            t = ((xi - x1) ** 2 + (yi - yi) ** 2) ** 0.5 / ((x2 - x1) ** 2 + (yi - yi) ** 2) ** 0.5
                            I = (1 - t) * I1 + t * I2
                            #print(I)
                            canv.create_oval(xi + a, yi + a, xi + a, yi + a,
                                             fill=rgb_hack((255, int(255 - 255 * (I)), 255)),
                                             outline=rgb_hack((255, int(255 - 255 * (I)), 255)))

                else:
                    for yi in range(round(p_versh[0].y), round(p_versh[2].y), -1):
                        x1 = max((yi - p_versh[0].y) * (p_versh[3].x - p_versh[0].x) / (p_versh[3].y - p_versh[0].y) +
                                 p_versh[0].x,
                                 (yi - p_versh[2].y) * (p_versh[3].x - p_versh[2].x) / (p_versh[3].y - p_versh[2].y) +
                                 p_versh[2].x)
                        x2 = min((yi - p_versh[1].y) * (p_versh[2].x - p_versh[1].x) / (p_versh[2].y - p_versh[1].y) +
                                 p_versh[2].x,
                                 (yi - p_versh[1].y) * (p_versh[0].x - p_versh[1].x) / (p_versh[0].y - p_versh[1].y) +
                                 p_versh[0].x)
                        # Тут надо переделывать
                        t1 = ((x1 - p_versh[0].x) ** 2 + (yi - p_versh[0].y) ** 2) ** 0.5 / (
                                    (p_versh[3].x - p_versh[0].x) ** 2 + (p_versh[3].y - p_versh[0].y) ** 2) ** 0.5
                        I1 = (1 - t1) * p_versh[0].I + t1 * p_versh[3].I
                        t2 = ((x2 - p_versh[1].x) ** 2 + (yi - p_versh[1].y) ** 2) ** 0.5 / (
                                    (p_versh[2].x - p_versh[1].x) ** 2 + (p_versh[2].y - p_versh[1].y) ** 2) ** 0.5
                        I2 = (1 - t2) * p_versh[1].I + t2 * p_versh[2].I
                        # Переделывать до сюда
                        for xi in range(round(x1), round(x2)):
                            t = ((xi - x1) ** 2 + (yi - yi) ** 2) ** 0.5 / ((x2 - x1) ** 2 + (yi - yi) ** 2) ** 0.5
                            I = (1 - t) * I1 + t * I2
                            #print(I)
                            canv.create_oval(xi + a, yi + a, xi + a, yi + a,
                                             fill=rgb_hack((255, int(255 - 255 * (I)), 255)),
                                             outline=rgb_hack((255, int(255 - 255 * (I)), 255)))

                # canv.create_polygon(list(np.concatenate(list(map(func, c)))), fill=rgb_hack((255, int(255 - 255*i), 255)), outline='black')


canv.bind("<Key>", control)  # второй аргумент - имя функции по нажатию любой клавиши клавиатуры
root.mainloop()
