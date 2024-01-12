#!/usr/bin/env python3

# MIT License

# Copyright (c) 2023 Achille MARTIN

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pygame
import math
import random

class Player():
    
    # Measurement definition for avatar
    width_body = 50
    width_side_fin = 20
    width_tail_fin = 10
    width_face = 10
    width_eye = 2.5
    height_body = 20
    height_side_fin = 10
    height_tail_fin = 10
    height_face = 20
    height_eye = 2.5
    colour_body = (0, 0, 255)
    colour_side_fin = (0, 100, 200)
    colour_tail_fin = (0, 0, 0)
    colour_face = (200, 150, 200)
    colour_eye = (255, 255, 255)

    def __init__(self, avatar_pos, surface_pos, surface_angle_deg):
        # Avatar characteristics within surface
        self.avatar_x = avatar_pos[0]
        self.avatar_y = avatar_pos[1]
        self.width = self.width_body + self.width_tail_fin
        self.height = self.height_body + 2*self.height_side_fin
        # Surface characteristics within canvas
        self.surface = pygame.Surface((self.width, self.height))
        self.surface_x = surface_pos[0] - self.width/2
        self.surface_y = surface_pos[1] - self.height/2
        self.surface_center_x = surface_pos[0]
        self.surface_center_y = surface_pos[1]
        self.surface_angle_deg = surface_angle_deg
        self.linear_velocity = 1
        self.angular_velocity = 1
        self.colour_default = (0, 0, 255)

    def draw_onto_surface(self):
        
        # Setting the surface
        surface = self.surface
        
        # Filling the surface with a background colour
        surface.fill((255, 255, 255))
    
        # Body
        pygame.draw.rect(surface, 
                         self.colour_body, 
                         (self.avatar_x - 2*self.width_body/5, self.avatar_y - self.height_body/2, self.width_body, self.height_body))
        
        # Top Fin
        pygame.draw.rect(surface, 
                         self.colour_side_fin, 
                         (self.avatar_x - 1*self.width_body/5, self.avatar_y - self.height_body, self.width_side_fin, self.height_side_fin))
        
        # Bottom Fin
        pygame.draw.rect(surface, 
                         self.colour_side_fin, 
                         (self.avatar_x - 1*self.width_body/5, self.avatar_y + self.height_body/2, self.width_side_fin, self.height_side_fin))
        
        # Tail Fin
        pygame.draw.rect(surface, 
                         self.colour_tail_fin, 
                         (self.avatar_x - 3*self.width_body/5, self.avatar_y - self.height_body/4, self.width_tail_fin, self.height_tail_fin))
        
        # Face
        pygame.draw.rect(surface, 
                         self.colour_face, 
                         (self.avatar_x + 2*self.width_body/5, self.avatar_y - self.height_body/2, self.width_face, self.height_face))
        
        # Top Eye
        pygame.draw.rect(surface, 
                         self.colour_tail_fin, 
                         (self.avatar_x + 2.5*self.width_body/5, self.avatar_y - self.height_body/3.5, self.width_eye, self.height_eye))
        
        # Bottom Eye
        pygame.draw.rect(surface, 
                         self.colour_tail_fin, 
                         (self.avatar_x + 2.5*self.width_body/5, self.avatar_y + self.height_body/4.5, self.width_eye, self.height_eye))
   
    def display_onto_canvas(self, canvas):
        # Only the rotated surface must be displayed
        [rot_surf, rot_surf_rect] = self.rotate_surface(canvas, 
                                                        self.surface,
                                                        (self.surface_x + self.width/2, self.surface_y + self.height/2), 
                                                        (self.width/2, self.height/2),
                                                        self.surface_angle_deg)
        canvas.blit(rot_surf, rot_surf_rect)
   
    def move_player(self, mv_type, rot_direction = 'counterclockwise'):
        # mv_type is either 't' for translation or 'r' for rotation
        if mv_type == 't':
            self.surface_x += self.linear_velocity * math.cos(self.surface_angle_deg * math.pi/180)
            self.surface_center_x += self.linear_velocity * math.cos(self.surface_angle_deg * math.pi/180)
            # The minus sign for y comes from the coordinate frame of pygame:
            # x goes from topleft to top right
            # y goes from topleft to bottom left
            self.surface_y -= self.linear_velocity * math.sin(self.surface_angle_deg * math.pi/180)
            self.surface_center_y -= self.linear_velocity * math.sin(self.surface_angle_deg * math.pi/180)
        elif mv_type == 'r':
            if rot_direction == 'counterclockwise':
                self.surface_angle_deg += self.angular_velocity
            elif rot_direction == 'clockwise':
                self.surface_angle_deg -= self.angular_velocity
            else:
                # Not coded
                pass
            # Angle constrained to [0, 360[ deg
            self.surface_angle_deg = self.surface_angle_deg % 360
        else:
            # Not coded
            pass
    
    def rotate_surface(self, canvas, surface, canvas_point, surface_point, angle):
        # The surface_point defines a point on the surface around which to rotate the surface
        # The canvas_point defines a point on the canvas at which the surface_point is placed
        
        # The following piece of code is inspired from Rabbid76 
        # Link: https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_surface_rotate.md
            
        # offset from pivot to center
        surface_rect = surface.get_rect(topleft = (canvas_point[0] - surface_point[0], canvas_point[1] - surface_point[1]))
        offset_center_to_pivot = pygame.math.Vector2(canvas_point) - surface_rect.center
        
        # rotated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(-angle)

        # rotated image center
        rotated_surface_center = (canvas_point[0] - rotated_offset.x, canvas_point[1] - rotated_offset.y)

        # get a rotated image
        rotated_surface = pygame.transform.rotate(surface, angle)
        rotated_surface_rect = rotated_surface.get_rect(center = rotated_surface_center)        
        
        return [rotated_surface, rotated_surface_rect]

class Game:

    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.player = Player((30, 20), (50, 50), 0)
        self.canvas = Canvas(self.width, self.height)

    def run_manual(self):
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
                # Checking canvas constraints
                if self.player.surface_center_x + self.player.width/2 < self.width - self.player.linear_velocity \
                    and self.player.surface_center_x - self.player.width/2 > self.player.linear_velocity \
                    and self.player.surface_center_y + self.player.width/2 < self.height - self.player.linear_velocity \
                    and self.player.surface_center_y - self.player.width/2 > self.player.linear_velocity:
                    self.player.move_player('t')

            if keys[pygame.K_RIGHT]:
                self.player.move_player('r', 'clockwise')

            if keys[pygame.K_LEFT]:
                self.player.move_player('r', 'counterclockwise')
            
            # Nudging the player to avoid getting it stuck to a canvas boundary
            if self.player.surface_center_x + self.player.width/2 >= self.width - self.player.linear_velocity:
                self.player.surface_x -= self.player.linear_velocity
                self.player.surface_center_x -= self.player.linear_velocity

            if self.player.surface_center_x - self.player.width/2 <= self.player.linear_velocity:
                self.player.surface_x += self.player.linear_velocity
                self.player.surface_center_x += self.player.linear_velocity
            
            if self.player.surface_center_y + self.player.width/2 >= self.height - self.player.linear_velocity:
                self.player.surface_y -= self.player.linear_velocity
                self.player.surface_center_y -= self.player.linear_velocity
            
            if self.player.surface_center_y - self.player.width/2 <= self.player.linear_velocity:
                self.player.surface_y += self.player.linear_velocity
                self.player.surface_center_y += self.player.linear_velocity
            
            # Clear canvas
            self.canvas.draw_background()
            
            # Draw player's avatar
            self.player.draw_onto_surface()
            
            # Add surface to canvas
            self.player.display_onto_canvas(self.canvas.get_canvas())
            
            # Display canvas
            self.canvas.update()

        pygame.quit()

    def run_automatic(self):
        clock = pygame.time.Clock()
        run = True
        
        # Setting motion params
        is_angle_reached = 1
        angle_desired_deg = 0
        rot_direction_desired = 0
        angle_precision = 5
        is_distance_reached = 1
        distance_desired = 0
        distance_travelled = 0
        distance_precision = 5
        iteration_max = 5
                
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
            
            # Continuous forward motion
            self.player.move_player('t')
            
            # Random angular motion
            if is_angle_reached and is_distance_reached:
                angle_desired_deg = random.randint(0, 359)
                rot_direction_desired = random.randint(0, 2)
                distance_desired = random.randint(0, int(self.width/8))
                # Making sure that we don't ask for a distance outside the canvas' boundaries
                iteration = 1
                while self.player.surface_center_x + self.player.width/2 + distance_desired >= self.width \
                    or self.player.surface_center_x - self.player.width/2 - distance_desired <= 0 \
                    or self.player.surface_center_y + self.player.width/2 + distance_desired >= self.height \
                    or self.player.surface_center_y - self.player.width/2 - distance_desired <= 0:
                    if iteration > iteration_max:
                        rot_direction_desired = random.randint(0, 1)
                        break
                    distance_desired = random.randint(0, int(self.width/8))
                    iteration+=1
                is_angle_reached = 0
                is_distance_reached = 0
            else:
                if rot_direction_desired == 0:
                    self.player.move_player('r', 'counterclockwise')
                elif rot_direction_desired == 1:
                    self.player.move_player('r', 'clockwise')
                elif rot_direction_desired == 2:
                    # Keep going on a straight line
                    distance_travelled+=1
                else:
                    # Not coded
                    pass
                if self.player.surface_angle_deg >= angle_desired_deg - angle_precision \
                    and self.player.surface_angle_deg <= angle_desired_deg + angle_precision:
                    is_angle_reached = 1
                    is_distance_reached = 1
                if distance_travelled >= distance_desired - distance_precision \
                    and distance_travelled <= distance_desired + distance_precision:
                    is_angle_reached = 1
                    is_distance_reached = 1
                    distance_travelled = 0
            
            # Nudging the player to avoid getting it stuck to a canvas boundary
            if self.player.surface_center_x + self.player.width/2 >= self.width - self.player.linear_velocity:
                self.player.surface_x -= self.player.linear_velocity
                self.player.surface_center_x -= self.player.linear_velocity

            if self.player.surface_center_x - self.player.width/2 <= self.player.linear_velocity:
                self.player.surface_x += self.player.linear_velocity
                self.player.surface_center_x += self.player.linear_velocity
            
            if self.player.surface_center_y + self.player.width/2 >= self.height - self.player.linear_velocity:
                self.player.surface_y -= self.player.linear_velocity
                self.player.surface_center_y -= self.player.linear_velocity
            
            if self.player.surface_center_y - self.player.width/2 <= self.player.linear_velocity:
                self.player.surface_y += self.player.linear_velocity
                self.player.surface_center_y += self.player.linear_velocity
            
            # Clear canvas
            self.canvas.draw_background()
            
            # Draw player's avatar
            self.player.draw_onto_surface()
            
            # Add surface to canvas
            self.player.display_onto_canvas(self.canvas.get_canvas())
            
            # Display canvas
            self.canvas.update()

        pygame.quit()

class Canvas:

    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
    
    @staticmethod
    def update():
        pygame.display.update()

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((255,255,255))

if __name__ == "__main__":
    
    # Instantiating the game
    g = Game(500,500)
    
    # Startup guide
    print('\n*** WELCOME to the Fish Adventure Game ***\n')
    fish_control_input = input('Would you like to let the fish live its own life (0) or control the fish (1) ? ')
    if (fish_control_input == '0'):
        print('\nThe fish will move on its own')
        print('Press ESCAPE to quit the game')
        g.run_automatic()
    elif (fish_control_input == '1'):
        print('\nTo control the fish, use: ')
        print('* UP arrow to go forward')
        print('* RIGHT arrow to turn clockwise')
        print('* LEFT arrow to turn counterclockwise')
        print('Press ESCAPE to quit the game')
        g.run_manual()    
    else:
        exit()
