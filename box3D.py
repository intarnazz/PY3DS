import pygame
import sys
import math
import numpy as np
from image import *
from box import *


class Poligon:
    def __init__(self, point):
        self.point = np.matrix(point).reshape((3, 1))
        self.point2D = ((0), (0))

    def dot(self, matrix):
        self.point = np.dot(matrix, self.point)

    def dot2D(self):
        self.point2D = np.dot([[1, 0, 0], [0, 1, 0]], self.point)


class Box3D:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_rect()[2]
        self.height = screen.get_rect()[3]
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

        self.points.append(Poligon([p, 0, 0]))
        self.points.append(Poligon([0, p, 0]))
        self.points.append(Poligon([0, 0, p]))
        self.points.append(Poligon([-p, 0, 0]))
        self.points.append(Poligon([0, -p, 0]))
        self.points.append(Poligon([0, 0, -p]))

        self.points_l = []
        self.points_l.append(np.matrix([0, 0, -1]))

        self.x_matrix = np.matrix(
            [
                [1, 0, 0],
                [0, math.cos(self.angle), -math.sin(self.angle)],
                [0, math.sin(self.angle), math.cos(self.angle)],
            ]
        )
        self.y_matrix = np.matrix(
            [
                [math.cos(self.angle), 0, math.sin(self.angle)],
                [0, 1, 0],
                [-math.sin(self.angle), 0, math.cos(self.angle)],
            ]
        )
        self.z_matrix = np.matrix(
            [
                [math.cos(self.angle), -math.sin(self.angle), 0],
                [math.sin(self.angle), math.cos(self.angle), 0],
                [0, 0, 1],
            ]
        )

    def blit(self):
        for i in self.points:
            i.dot(self.x_matrix)
            i.dot(self.y_matrix)
            i.dot(self.z_matrix)
            projected2d = i.dot2D()
            i.point2D = (int(i.point2D[0][0] * self.scale) + self.width / 2 - 50,)
            i.point2D = (int(i.point2D[1][0] * self.scale) + self.height / 2 - 50,)

            pygame.draw.circle(
                self.screen,
                (0, 0, 0),
                i.point2D,
                5,
            )

        pygame.draw.circle(
            self.screen,
            (255, 255, 255),
            (self.width - 200, 200),
            100,
        )

        points_l = []
        for i in self.points_l:
            rotated2d = i.reshape((3, 1))
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
            pygame.draw.circle(
                self.screen,
                (255, 255, 0),
                points_l[-1],
                20,
            )

        pygame.draw.circle(
            self.screen,
            (255, 255, 255),
            (self.width - 200, 200),
            100,
        )

        for i in range(8, 14):
            pygame.draw.line(
                self.screen,
                (255, 255, 0),
                point[i + 6],
                points_l[-1],
                2,
            )
            pygame.draw.line(
                self.screen,
                (255, 255, 0),
                point[i],
                point[i + 6],
                2,
            )
        self.screen_A.fill((0, 0, 0, 0))

        pygame.draw.polygon(
            self.screen,
            (255 - self.theta(point, points_l, 8) * 60, 0, 0),
            [point[4], point[5], point[6], point[7]],
        )

        pygame.draw.polygon(
            self.screen,
            (255 - self.theta(point, points_l, 10) * 60, 0, 0),
            [point[0], point[1], point[2], point[3]],
        )

        pygame.draw.polygon(
            self.screen_A,
            (255, 0, 0, 0),
            [point[3], point[2], point[6], point[7]],
        )
        self.screen.blit(self.screen_A, (0, 0))

        pygame.draw.polygon(
            self.screen_A,
            (255, 0, 0, 0),
            [point[0], point[1], point[5], point[4]],
        )
        self.screen.blit(self.screen_A, (0, 0))

        pygame.draw.polygon(
            self.screen_A,
            (255, 0, 0, 0),
            [point[3], point[0], point[4], point[7]],
        )
        self.screen.blit(self.screen_A, (0, 0))

        pygame.draw.polygon(
            self.screen_A,
            (255, 0, 0, 0),
            [point[2], point[1], point[5], point[6]],
        )
        self.screen.blit(self.screen_A, (0, 0))

        # pygame.draw.circle(
        #     self.screen,
        #     (0, 0, 255),
        #     point[-1],
        #     5,
        # )

        pygame.display.flip()
        self.clock.tick(60)  # limits FPS to 60
