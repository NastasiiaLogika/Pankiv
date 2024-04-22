import math
import random
import sys
import time

import pygame
from pygame.locals import *

img_hole = "hole.png"

pygame.font.init()

CLICK = pygame.font.SysFont("Arial", 24).render("Click", True, (255, 255, 255))

WIDTH, HEIGHT = 600, 600
HOLE_WIDTH, HOLE_HEIGHT = 100, 100
DEFAULT_COLOR = (41, 75, 128)
FPS = 60


class Hole:
    def __init__(self, start_coordinates, color):
        self.rect = pygame.rect.Rect(*start_coordinates, HOLE_WIDTH, HOLE_HEIGHT)
        self.color = color
        self.fired = False

    def center(self):
        return self.rect.x + (self.rect.width - CLICK.get_width()) // 2, \
               self.rect.y + (self.rect.height - CLICK.get_height()) // 2


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.counter = 0
        self.message_font = pygame.font.SysFont("Arial", 24)

        self.rectangles = [
            Hole((25, 50), (41, 75, 128)),
            Hole((250, 50), (41, 75, 128)),
            Hole((475, 50), (41, 75, 128)),
            Hole((25, 200), (41, 75, 128)),
            Hole((250, 200), (41, 75, 128)),
            Hole((475, 200), (41, 75, 128)),
            Hole((25, 350), (41, 75, 128)),
            Hole((250, 350), (41, 75, 128)),
            Hole((475, 350), (41, 75, 128)),
        ]

        pygame.display.set_caption("Втовчи Ховраха")

    def run(self):
        start_time = time.time()
        random_rectangle = random.choice(self.rectangles)
        random_rectangle.fired = True

        while True:
            self.screen.fill((58, 101, 166))
            message = self.message_font.render(f"Рахунок: {self.counter}", True, (255, 255, 255))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    for rectangle in self.rectangles:
                        if rectangle.rect.collidepoint(event.pos) and rectangle.fired:
                            self.counter += 1

                            rectangle.color = (0, 255, 0)
                        elif rectangle.rect.collidepoint(event.pos) and not rectangle.fired:
                            self.counter -= 1

                            rectangle.color = (255, 0, 0)
                        else:
                            rectangle.color = DEFAULT_COLOR

            for rectangle in self.rectangles:
                pygame.draw.rect(self.screen, rectangle.color, rectangle)

                if rectangle.fired:
                    self.screen.blit(CLICK, rectangle.center())
                else:
                    pass

            if (start_time - time.time()) % 2 < 0.01:
                random_rectangle.fired = False
                random_rectangle = random.choice(self.rectangles)
                random_rectangle.fired = True

            self.screen.blit(message, (25, 10))

            pygame.display.update()
            self.clock.tick(FPS)


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()