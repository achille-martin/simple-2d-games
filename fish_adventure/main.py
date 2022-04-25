#!/usr/bin/env python3

import pygame

class Player():
    
    # Measure definition for player's avatar
    width_body = 50
    width_side_fin = 20
    width_back_fin = 10
    width_face = 10
    width_eye = 2.5
    height_body = 20
    height_side_fin = 10
    height_back_fin = 30
    height_face = 20
    height_eye = 2.5
    colour_body = (0, 0, 255)
    colour_side_fin = (0, 100, 200)
    colour_back_fin = (0, 0, 0)
    colour_face = (200, 150, 200)
    colour_eye = (255, 255, 255)

    def __init__(self, startx, starty):
        self.x = startx
        self.y = starty
        self.width = self.width_body + self.width_back_fin
        self.height = self.height_body + self.height_side_fin
        self.linear_velocity = 1
        self.colour_default = (0, 0, 255)

    def draw(self, surface):
        # Body
        pygame.draw.rect(surface, self.colour_body, (self.x - 2*self.width_body/5, self.y - self.height_body/2, self.width_body, self.height_body))
        # Top Fin
        pygame.draw.rect(surface, self.colour_side_fin, (self.x - 1*self.width_body/5, self.y - self.height_body, self.width_side_fin, self.height_side_fin))
        # Bottom Fin
        pygame.draw.rect(surface, self.colour_side_fin, (self.x - 1*self.width_body/5, self.y + self.height_body/2, self.width_side_fin, self.height_side_fin))
        # Back Fin
        pygame.draw.rect(surface, self.colour_back_fin, (self.x - 3*self.width_body/5, self.y - self.height_body/1.5, self.width_back_fin, self.height_back_fin))
        # Face
        pygame.draw.rect(surface, self.colour_face, (self.x + 2*self.width_body/5, self.y - self.height_body/2, self.width_face, self.height_face))
        # Top Eye
        pygame.draw.rect(surface, self.colour_back_fin, (self.x + 2.5*self.width_body/5, self.y - self.height_body/3.5, self.width_eye, self.height_eye))
        # Bottom Eye
        pygame.draw.rect(surface, self.colour_back_fin, (self.x + 2.5*self.width_body/5, self.y + self.height_body/4.5, self.width_eye, self.height_eye))
   
    def move(self, mv_type):
        # mv_type is either 't' for translation or 'r' for rotation
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

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((255,255,255))

if __name__ == "__main__":
    g = Game(250,250)
    g.run()
