#!/usr/bin/env python3

import config
import pygame
import random

# setup the screen and bounds around it so drone does not go off screen
class Environment:
    def __init__(self):
        self.WIDTH = config.SCREEN_WIDTH
        self.HEIGHT = config.SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Rocket Simulation")
        
        self.xTarget = self.WIDTH // 2
        self.yTarget = self.HEIGHT // 2
        self.count = 0
        
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Arial', 32)
        
        
    def checkBounds(self, player):
        safety_margin = config.SAFETY_MARGIN
        # lower bound
        if (player.y > self.HEIGHT - safety_margin - player.height):
            player.y = self.HEIGHT - safety_margin - player.height
            player.y_speed = 0
        # upper bound
        if (player.y < 0 + safety_margin):
            player.y = 0 + safety_margin
            player.y_speed = 0
        # left bound
        if (player.x < 0 + safety_margin):
            player.x = 0 + safety_margin
            player.x_speed = 0
        # right bound
        if (player.x > self.WIDTH - safety_margin - player.width):
            player.x = self.WIDTH - safety_margin - player.width
            player.x_speed = 0
            
            
    def createTarget(self, player):
        pygame.draw.circle(self.screen, (255, 0, 0), (int(self.xTarget), int(self.yTarget)), 5)
        
        if (abs(self.xTarget - player.x) < config.TARGET_MARGIN and abs(self.yTarget - player.y) < config.TARGET_MARGIN):
            self.count += 1
            if self.count >= config.TIME_ON_TARGET:
                self.xTarget = random.randint(config.TARGET_SPAWN_MARGIN, self.WIDTH - config.TARGET_SPAWN_MARGIN)
                self.yTarget = random.randint(config.TARGET_SPAWN_MARGIN, self.HEIGHT - config.TARGET_SPAWN_MARGIN)
        else:
            self.count = 0
        # put the target count on screen
        TargetText = f"Time on Target: {config.TIME_ON_TARGET - self.count}"
        text_surface = self.my_font.render(TargetText, True, (0, 0, 0))
        text_rect = text_surface.get_rect(topleft=(50, 50))
        self.screen.blit(text_surface, (50, 100))
            
        return self.xTarget, self.yTarget

    # print the windspeed and direction on screen 
    def printWindOnScreen(self, wind, maxWind):
        windText = f"wind: {wind}"
        text_surface = self.my_font.render(windText, True, (0, 0, 0))
        text_rect = text_surface.get_rect(topleft=(50, 50))
        self.screen.blit(text_surface, (50, 50))
        
        magnitudeAndDirection = wind / maxWind
        
        # Settings for the arrow
        start_x = text_rect.right + 150  # Start 150 pixels to the right of the text
        start_y = text_rect.centery     # Align vertically with the center of the text
        max_arrow_length = 100          # The longest the arrow can be at maxWind
        
        end_x = start_x + (magnitudeAndDirection * max_arrow_length)
        end_y = start_y
        
        line_color = (200, 0, 0) # Red
        pygame.draw.line(self.screen, line_color, (start_x, start_y), (end_x, end_y), 9)
        
        if wind != 0:
            tip_direction = 1 if wind > 0 else -1
            pygame.draw.polygon(self.screen, line_color, [
                (end_x + (10 * tip_direction), end_y),
                (end_x, end_y - 9),
                (end_x, end_y + 9)
            ])
    


