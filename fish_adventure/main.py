#!/usr/bin/env python3

import pygame

class Player():
    width = height = 25

    def __init__(self, startx, starty, color=(255,0,0)):
        self.x = startx
        self.y = starty
        self.linear_velocity = 1
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, 
                         self.color,
                         (self.x - self.width/2, 
                          self.y - self.height/2, 
                          self.width, 
                          self.height),
                         0)

    def move(self, mv_type):
        """
        :param mv_type: 't' or 'r' (translation, rotation)
        :return: None
        """
        if mv_type == 't':
            self.x += self.linear_velocity
        elif dirn == 'r':
            pass
        else:
            pass

class Game:

    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.player = Player(50, 50)
        self.canvas = Canvas(self.width, self.height, "Initiating Canvas...")

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                if self.player.x + self.player.width/2 <= self.width - self.player.linear_velocity:
                    self.player.move('t')

            if keys[pygame.K_RIGHT]:
                pass

            if keys[pygame.K_LEFT]:
                pass

            # Update Canvas
            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()

class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))
        self.screen.draw(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((255,255,255))

if __name__ == "__main__":
    g = Game(250,250)
    g.run()
