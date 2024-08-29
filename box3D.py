import pygame
import sys
import math
import numpy as np
from image import *
from box import *


class Poligon:
    def __init__(self, point, poligon=[0, 0, 0, 0, 0]):
        self.poligon = poligon
        self.point_old = np.matrix(point).reshape((3, 1))
        self.point = self.point_old
        self.point2D = np.dot([[1, 0, 0], [0, 1, 0]], self.point)

    def getPoligon(self):
        return self.poligon

    def dot(self, matrixs):
        self.point = self.point_old
        for matrix in matrixs:
            self.point = np.dot(matrix, self.point)
        self.dot2D()

    def dot2D(self):
        self.point2D = np.dot([[1, 0, 0], [0, 1, 0]], self.point)

    def get(self):
        return (int(self.point2D[0][0]), int(self.point2D[1][0]))


class Box3D:
    def __init__(self, screen, color=(255, 255, 255), pos=""):
        self.color = color
        self.screen = screen
        self.width = screen.get_rect()[2]
        self.height = screen.get_rect()[3]
        self.pos = (self.width / 2 - 50, self.height / 2 - 50) if pos == "" else pos

        self.scale = 100
        self.points = []
        self.angle = 0
        p = 1
        self.points.append(Poligon([-p, -p, p]))
        self.points.append(Poligon([p, -p, p]))
        self.points.append(Poligon([p, p, p]))
        self.points.append(Poligon([-p, p, p]))
        self.points.append(Poligon([-p, -p, -p]))
        self.points.append(Poligon([p, -p, -p]))
        self.points.append(Poligon([p, p, -p]))
        self.points.append(Poligon([-p, p, -p]))

        self.points.append(Poligon([p * 2, 0, 0]))
        self.points.append(Poligon([0, p * 2, 0]))
        self.points.append(Poligon([0, 0, p * 2]))
        self.points.append(Poligon([-p * 2, 0, 0]))
        self.points.append(Poligon([0, -p * 2, 0]))
        self.points.append(Poligon([0, 0, -p * 2]))

        self.points.append(Poligon([p, 0, 0], [8, 2, 1, 5, 6]))
        self.points.append(Poligon([0, p, 0], [9, 3, 2, 6, 7]))
        self.points.append(Poligon([0, 0, p], [10, 0, 1, 2, 3]))
        self.points.append(Poligon([-p, 0, 0], [11, 3, 0, 4, 7]))
        self.points.append(Poligon([0, -p, 0], [12, 0, 1, 5, 4]))
        self.points.append(Poligon([0, 0, -p], [13, 4, 5, 6, 7]))

        self.points_l = []
        self.points_l.append(np.matrix([0, 0, -2]))
        self.points_l.append(np.matrix([0, 0, 3]))

    def x_matrix(self):
        return np.matrix(
            [
                [1, 0, 0],
                [0, math.cos(self.angle), -math.sin(self.angle)],
                [0, math.sin(self.angle), math.cos(self.angle)],
            ]
        )

    def y_matrix(self):
        return np.matrix(
            [
                [math.cos(self.angle), 0, math.sin(self.angle)],
                [0, 1, 0],
                [-math.sin(self.angle), 0, math.cos(self.angle)],
            ]
        )

    def z_matrix(self):
        return np.matrix(
            [
                [math.cos(self.angle), -math.sin(self.angle), 0],
                [math.sin(self.angle), math.cos(self.angle), 0],
                [0, 0, 1],
            ]
        )

    def theta(self, points_l, i):
        thetas = []
        for point_l in points_l:
            A = (self.points[i + 6].get(), self.points[i].get())
            B = (self.points[i + 6].get(), point_l)
            a = (A[1][0] - A[0][0], A[1][1] - A[0][1])
            b = (B[1][0] - B[0][0], B[1][1] - B[0][1])
            magnitude_a = math.sqrt(a[0] ** 2 + a[1] ** 2)
            magnitude_b = math.sqrt(b[0] ** 2 + b[1] ** 2)
            dot_product = a[0] * b[0] + a[1] * b[1]
            theta = 0
            if magnitude_a != 0 and magnitude_b != 0:
                cos_theta = dot_product / (magnitude_a * magnitude_b)
                theta = math.acos(cos_theta)
            thetas.append(theta)
        return thetas

    def rgbs(self, r, g, b, thetas):
        for theta in thetas:
            r -= theta * 100
            g -= theta * 100
            b -= theta * 100
        return (
            int(r if r > 0 else 0),
            int(g if g > 0 else 0),
            int(b if b > 0 else 0),
        )

    def blit(self):
        self.angle += 0.01
        for i in self.points:
            i.dot([self.x_matrix(), self.y_matrix(), self.z_matrix()])
            i.point2D[0][0] = (int(i.point2D[0][0] * self.scale) + self.pos[0],)
            i.point2D[1][0] = (int(i.point2D[1][0] * self.scale) + self.pos[1],)
            # pygame.draw.circle(
            #     self.screen,
            #     (0, 0, 0),
            #     i.get(),
            #     5,
            # )
        # pygame.draw.circle(
        #     self.screen,
        #     (255, 255, 255),
        #     (self.width - 200, 200),
        #     100,
        # )

        points_l = []
        for i in range(len(self.points_l)):
            rotated2d = self.points_l[i].reshape((3, 1))
            projected2d = np.dot(
                [
                    [1, 0, 0],
                    [0, 1, 0],
                ],
                rotated2d,
            )
        points_l.append(
            (
                int(projected2d[0][0]) + self.width - 200,
                int(projected2d[1][0]) + 200,
            )
        )
        # points_l.append(
        #     (
        #         int(projected2d[0][0]) + self.width - 1500,
        #         int(projected2d[1][0]) + 600,
        #     )
        # )
        # pygame.draw.circle(
        #     self.screen,
        #     (255, 255, 0),
        #     points_l[0],
        #     20,
        # )
        # pygame.draw.circle(
        #     self.screen,
        #     (255, 255, 0),
        #     points_l[1],
        #     20,
        # )

        # pygame.draw.circle(
        #     self.screen,
        #     (255, 255, 255),
        #     (self.width - 200, 200),
        #     100,
        # )

        # for i in range(8, 14):
        #     pygame.draw.line(
        #         self.screen,
        #         (255, 255, 0),
        #         self.points[i + 6].get(),
        #         points_l[-1],
        #         2,
        #     )
        #     pygame.draw.line(
        #         self.screen,
        #         (255, 255, 0),
        #         self.points[i].get(),
        #         self.points[i + 6].get(),
        #         2,
        #     )

        arr = self.points
        arr_sorted = sorted(arr, key=lambda x: float(x.point[2][0]))

        for i in arr_sorted:
            poligon = i.getPoligon()
            pygame.draw.polygon(
                self.screen,
                self.rgbs(*self.color, self.theta(points_l, poligon[0])),
                [
                    self.points[poligon[1]].get(),
                    self.points[poligon[2]].get(),
                    self.points[poligon[3]].get(),
                    self.points[poligon[4]].get(),
                ],
            )

        i = 11
        # pygame.draw.line(
        #     self.screen,
        #     (0, 0, 255),
        #     self.points[i].get(),
        #     self.points[i + 6].get(),
        #     3,
        # )

        # # pygame.draw.circle(
        # #     self.screen,
        # #     (0, 0, 255),
        # #     point[-1],
        # #     5,
        # # )

        # pygame.display.flip()
        # self.clock.tick(60)  # limits FPS to 60
