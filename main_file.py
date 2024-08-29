import pygame
import sys
import math
import numpy as np
from image import *
from box import *


class ProgectLavel:
    def __init__(self):
        pygame.init()

        self.bgcolor = (50, 50, 50)
        self.clock = pygame.time.Clock()
        info = pygame.display.Info()

        self.width = info.current_w
        self.height = info.current_h

        self.screen = pygame.display.set_mode((self.width, self.height))  # РАСШИРЕНИЕ
        self.screen.fill((50, 50, 50))
        self.screen_A = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        self.screen_rect = self.screen.get_rect()
        pygame.mouse.set_visible(False)

        self.boxes = {
            "bg": [
                # BG(self.screen),
            ],
            # "hero": Hero(self.screen),
            # "enemy": Enemy(self.screen),
            # "focus": [Focus(self.screen)],
            "cart": [
                # Cart(self.screen),
            ],
            "moveBox": [
                #'MoveBox': MoveBox(self.screen, 20),
            ],
            "hpBar": [],
            "hpBarBorder": [],
            "box": [],
        }

        # self.boxes["hpBarBorder"].append(HpBarBorder(self.screen, self.boxes["hero"]))
        # self.boxes["hpBarBorder"].append(HpBarBorder(self.screen, self.boxes["enemy"]))

        # for border in self.boxes["hpBarBorder"]:
        #     self.boxes["hpBar"].append(border.hpBar())

        # info = pygame.display.Info()

        # for i in range(4):
        #     self.add_cart()

        # self.points = [(150, 150), (350, 100), (400, 300), (200, 350)]
        # self.angle = 0
        # self.z = 1

        self.scale = 100

        self.points = []
        self.angle = 0

        p = 1
        self.points.append(np.matrix([-p, -p, p]))
        self.points.append(np.matrix([p, -p, p]))
        self.points.append(np.matrix([p, p, p]))
        self.points.append(np.matrix([-p, p, p]))
        self.points.append(np.matrix([-p, -p, -p]))
        self.points.append(np.matrix([p, -p, -p]))
        self.points.append(np.matrix([p, p, -p]))
        self.points.append(np.matrix([-p, p, -p]))

        self.points.append(np.matrix([p * 2, 0, 0]))
        self.points.append(np.matrix([0, p * 2, 0]))
        self.points.append(np.matrix([0, 0, p * 2]))
        self.points.append(np.matrix([-p * 2, 0, 0]))
        self.points.append(np.matrix([0, -p * 2, 0]))
        self.points.append(np.matrix([0, 0, -p * 2]))

        self.points.append(np.matrix([p, 0, 0]))
        self.points.append(np.matrix([0, p, 0]))
        self.points.append(np.matrix([0, 0, p]))
        self.points.append(np.matrix([-p, 0, 0]))
        self.points.append(np.matrix([0, -p, 0]))
        self.points.append(np.matrix([0, 0, -p]))

        self.points_l = []
        self.points_l.append(np.matrix([0, 0, -1]))

    def run_game(self):
        """ОСНОВНОЙ ЦИКЛ"""
        while True:
            self._check_events()
            for box in self.boxes["moveBox"]:
                box.move_box()
            self._update_screen()

    def add_cart(self):
        for cart in self.boxes["cart"]:
            cart.rect.x += 200
        self.boxes["cart"].append(Cart(self.screen))

    # /////////////////////////////////////////////////////////////// ДАЛЕЕ МОДУЛИ "RUN_GAME" //////////////////////////////////////////
    # ================= ИВЕНТЫ КНОПКИ ============================
    def _check_events(self):
        """Проверка ивентов"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

                # if event.key == pygame.K_SPACE:
                #     for cart in self.boxes["cart"]:
                #         cart.rect.x += 200
                #     self.boxes["cart"].append(Cart(self.screen))
                # # if event.key == pygame.K_BACKSPACE:
                #     if len(self.boxes["cart"]) > 0:
                #         self.boxes["cart"].pop(0)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    for box in self.boxes["moveBox"]:
                        box.box_up = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    for box in self.boxes["moveBox"]:
                        box.box_down = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    for box in self.boxes["moveBox"]:
                        box.box_right = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    for box in self.boxes["moveBox"]:
                        box.box_left = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    for box in self.boxes["moveBox"]:
                        box.box_up = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    for box in self.boxes["moveBox"]:
                        box.box_down = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    for box in self.boxes["moveBox"]:
                        box.box_right = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    for box in self.boxes["moveBox"]:
                        box.box_left = False

    # ================= //НАЖАТИЕ КНОПКИ// ============================
    # /////////////////////////////////////////////////////////////// КОНЕЦ "RUN_GAME" //////////////////////////////////////////

    def theta(self, point, points_l, i):
        A = (point[i + 6], point[i])
        B = (point[i + 6], points_l[-1])
        a = (A[1][0] - A[0][0], A[1][1] - A[0][1])
        b = (B[1][0] - B[0][0], B[1][1] - B[0][1])
        magnitude_a = math.sqrt(a[0] ** 2 + a[1] ** 2)
        magnitude_b = math.sqrt(b[0] ** 2 + b[1] ** 2)
        dot_product = a[0] * b[0] + a[1] * b[1]
        theta = 0
        if magnitude_a != 0 and magnitude_b != 0:
            cos_theta = dot_product / (magnitude_a * magnitude_b)
            theta = math.acos(cos_theta)
        return theta

    def _update_screen(self):
        """ОТРИСОВКА ЭКРАНА"""
        self.screen.fill(self.bgcolor)

        for boxes in self.boxes.values():
            if type(boxes) == type([]):
                for box in boxes:
                    box.blit()
            else:
                boxes.blit()

        # center_x = sum([p[0] for p in self.points]) / len(self.points)
        # center_y = sum([p[1] for p in self.points]) / len(self.points)

        # self.angle = 0.01
        # # self.z += 0.0001

        # for i in range(len(self.points)):
        #     qx = (
        #         center_x
        #         + math.cos(self.angle) * (self.points[i][0] - center_x)
        #         - math.sin(self.angle) * (self.points[i][1] - center_y)
        #     )
        #     qy = (
        #         center_y
        #         + math.sin(self.angle) * (self.points[i][0] - center_x)
        #         + math.cos(self.angle) * (self.points[i][1] - center_y)
        #     )

        #     # qx = self.points[i][0]
        #     # qy = self.points[i][1]

        #     if i < 2:
        #         qx = center_x + (qx - center_x) * self.z + 0.1
        #         qy = center_y + (qy - center_y) * self.z + 0.1
        #     else:
        #         qx = center_x + (qx - center_x) * self.z + -0.1
        #         qy = center_y + (qy - center_y) * self.z + -0.1

        #     self.points[i] = (qx, qy)

        # pygame.draw.polygon(self.screen, (255, 0, 0), self.points, 0)

        z_m = np.matrix(
            [
                [math.cos(self.angle), -math.sin(self.angle), 0],
                [math.sin(self.angle), math.cos(self.angle), 0],
                [0, 0, 1],
            ]
        )
        y_m = np.matrix(
            [
                [math.cos(self.angle), 0, math.sin(self.angle)],
                [0, 1, 0],
                [-math.sin(self.angle), 0, math.cos(self.angle)],
            ]
        )

        x_m = np.matrix(
            [
                [1, 0, 0],
                [0, math.cos(self.angle), -math.sin(self.angle)],
                [0, math.sin(self.angle), math.cos(self.angle)],
            ]
        )
        self.angle += 0.01

        point = []
        for i in self.points:
            rotated2d = np.dot(z_m, i.reshape((3, 1)))
            rotated2d = np.dot(y_m, rotated2d)
            rotated2d = np.dot(x_m, rotated2d)
            projected2d = np.dot(
                [
                    [1, 0, 0],
                    [0, 1, 0],
                ],
                rotated2d,
            )

            point.append(
                (
                    int(projected2d[0][0] * self.scale) + self.width / 2 - 50,
                    int(projected2d[1][0] * self.scale) + self.height / 2 - 50,
                )
            )

            pygame.draw.circle(
                self.screen,
                (0, 0, 0),
                point[-1],
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


if __name__ == "__main__":
    # Создание экземпляра и запуск игры
    pg_game = ProgectLavel()
    pg_game.run_game()
