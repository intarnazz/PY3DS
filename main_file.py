import pygame
import sys
from box3D import *


class ProgectLavel:
    def __init__(self):
        pygame.init()

        self.bgcolor = (0, 120, 56)
        self.clock = pygame.time.Clock()
        info = pygame.display.Info()

        self.width = info.current_w
        self.height = info.current_h
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((50, 50, 50))
        # self.screen_A = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        self.screen_rect = self.screen.get_rect()
        pygame.mouse.set_visible(False)

        self.boxes = {
            "Box3D": [Box3D(self.screen, color=(255, 150, 40))],
        }

    def run_game(self):
        """ОСНОВНОЙ ЦИКЛ"""
        while True:
            self._check_events()
            self._update_screen()

    # /////////////////////////////////////////////////////////////// "RUN_GAME" //////////////////////////////////////////
    # ================= check events ============================
    def _check_events(self):
        """Проверка ивентов"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.KEYUP:
                pass

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
    pg_game = ProgectLavel()
    pg_game.run_game()
