#!/usr/bin/env python3

import pygame
import math

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
            
            # Debug prints
            print('----')
            print('Player center x = ' + str(self.player.surface_center_x) + ', y = ' + str(self.player.surface_center_y))
            print('Player orientation angle = ' + str(self.player.surface_angle_deg))
            print('Player size w = ' + str(self.player.width) + ', h = ' + str(self.player.height))
            
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

    g = Game(500,500)
    g.run()
