import pygame
import sys
from image import *
from box import *

# [x] - Сделать класс image - отрисовка анимаций  и прогрузка катинок
# [x] - Отресовка картинок в Box через blit


class ProgectLavel:
    def __init__(self):
        pygame.init()

        self.bgcolor = (50, 50, 50)
        self.clock = pygame.time.Clock()
        info = pygame.display.Info()

        self.width = info.current_w
        self.height = info.current_h

        self.screen = pygame.display.set_mode((self.width, self.height))  # РАСШИРЕНИЕ
        self.screen_rect = self.screen.get_rect()
        pygame.mouse.set_visible(False)

        self.boxes = {
            "bg": [
                BG(self.screen),
            ],
            "hero": Hero(self.screen),
            "enemy": Enemy(self.screen),
            "focus": [Focus(self.screen)],
            "cart": [
                Cart(self.screen),
            ],
            "moveBox": [
                #'MoveBox': MoveBox(self.screen, 20),
            ],
            "hpBar": [],
            "hpBarBorder": [],
            "box": [],
        }

        self.boxes["hpBarBorder"].append(HpBarBorder(self.screen, self.boxes["hero"]))
        self.boxes["hpBarBorder"].append(HpBarBorder(self.screen, self.boxes["enemy"]))

        for border in self.boxes["hpBarBorder"]:
            self.boxes["hpBar"].append(border.hpBar())

        info = pygame.display.Info()

        for i in range(4):
            self.add_cart()

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

    def _update_screen(self):
        """ОТРИСОВКА ЭКРАНА"""
        self.screen.fill(self.bgcolor)

        for boxes in self.boxes.values():
            if type(boxes) == type([]):
                for box in boxes:
                    box.blit()
            else:
                boxes.blit()

        pygame.display.flip()
        self.clock.tick(60)  # limits FPS to 60


if __name__ == "__main__":
    # Создание экземпляра и запуск игры
    pg_game = ProgectLavel()
    pg_game.run_game()
