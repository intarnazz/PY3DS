import pygame
import sys


class Image:
    def __init__(self, path, scale) -> None:
        self.images = []
        self.path = path
        i = 1
        while True:
            try:
                self.image = pygame.image.load(f"img/{self.path}/{i}.gif")
            except:
                break

            if scale != ():
                self.image = pygame.transform.scale(self.image, scale)

            self.images.append(self.image)
            i += 1

        print(len(self.images))

        self.loop = 0

    def get(self):
        self.loop += 1
        if self.loop >= len(self.images):
            self.loop = 0
        return self.images[self.loop]
