#!/usr/bin/env python3

import pygame
import random
import numpy as np
import config

class Rocket:
    def __init__(self):
        self.width = config.ROCKET_WIDTH
        self.height = config.ROCKET_HEIGHT
        self.thruster_width = config.THRUSTER_WIDTH # Width of the grey side parts
        self.flame_height = config.FLAME_HEIGHT   # How far the flame sticks out
        self.d = 0.5*self.width - 0.5*self.thruster_width # distance from center to center of the thruster
        
        self.mass = config.ROCKET_MASS # in kg
        self.inertia = self.mass * (self.width*self.width + self.height*self.height) / 12
        self.gravity = config.GRAVITY
        
        self.max_force_thruster = config.MAX_THRUSTER_FORCE
        self.force_thrusterL = 0
        self.force_thrusterR = 0
        self.right_on = False
        self.left_on = False
        
        self.x = 0
        self.y = 0
        self.x_speed = 0
        self.y_speed = 0
        self.x_acceleration = 0
        self.y_acceleration = 0
        self.angle = 0
        self.angle_speed = 0
        self.angle_acceleration = 0
        
        self.img_idle = self._create_rocket_surface(left=False, right=False)
        self.img_left = self._create_rocket_surface(left=True, right=False)
        self.img_right = self._create_rocket_surface(left=False, right=True)
        self.img_both = self._create_rocket_surface(left=True, right=True)

        self.current_surface = self.img_idle
        
        
    def _create_rocket_surface(self, left, right):
        
        surf_w = self.width
        surf_h = self.height + self.flame_height
        
        # Create a transparent surface
        surface = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)
        
        # Colors
        COLOR_BODY = (50, 150, 255)    # Blue
        COLOR_THRUSTER = (70, 70, 70)  # Dark Grey
        COLOR_FLAME = (255, 120, 0)    # Orange

        # Draw the Main Blue Body
        body_rect = (self.thruster_width, 0, self.width - (2 * self.thruster_width), self.height)
        pygame.draw.rect(surface, COLOR_BODY, body_rect)

        # Draw Left Grey Side
        pygame.draw.rect(surface, COLOR_THRUSTER, (0, 0, self.thruster_width, self.height))

        # Draw Right Grey Side
        pygame.draw.rect(surface, COLOR_THRUSTER, (self.width - self.thruster_width, 0, self.thruster_width, self.height))

        # Draw Flames if active
        if left:
            # Flame under left pod
            flame_height = (self.force_thrusterL / self.max_force_thruster) * self.flame_height
            pygame.draw.polygon(surface, COLOR_FLAME, [(0, self.height), (self.thruster_width, self.height), (self.thruster_width // 2, self.height + flame_height)])
        if right:
            # Flame under right pod
            flame_height = (self.force_thrusterR / self.max_force_thruster) * self.flame_height
            pygame.draw.polygon(surface, COLOR_FLAME, [
                (self.width - self.thruster_width, self.height),
                (self.width, self.height),
                ((2*self.width - self.thruster_width)//2, self.height + flame_height)])

        return surface
        
    def setPosition(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        
    def movePhysics(self, dt, left_motor=False, right_motor=False):
        keys = pygame.key.get_pressed()
        
        # Reset thruster states
        left_on = False
        right_on = False
        
        total_force = 0
        total_momentum = 0
        
        if (keys[pygame.K_LEFT] or left_motor):
            left_on = True
            total_force += self.force_thrusterL
            total_momentum += self.force_thrusterL * self.d
            
        if (keys[pygame.K_RIGHT] or right_motor):
            right_on = True
            total_force += self.force_thrusterR
            total_momentum -= self.force_thrusterR * self.d
           
        rad = np.deg2rad(self.angle)
        
        self.x_acceleration = (total_force * np.sin(rad)) / self.mass
        self.y_acceleration = self.gravity - ((total_force * np.cos(rad)) / self.mass)
        self.angle_acceleration = total_momentum / self.inertia
           
        self.x_speed += self.x_acceleration * dt
        self.y_speed += self.y_acceleration * dt
        self.angle_speed += np.rad2deg(self.angle_acceleration) * dt
        
        self.y += self.y_speed * dt
        self.x += self.x_speed * dt
        self.angle += self.angle_speed * dt
        
        self.updateImage(left_on, right_on)
            
    
    def moveDirect(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.x += -5
        elif keys[pygame.K_d]:
            self.x += 5
            
        if keys[pygame.K_w]:
            self.y += -5
        elif keys[pygame.K_s]:
            self.y += 5
            
        if keys[pygame.K_q]:
            self.angle += 3
        elif keys[pygame.K_e]:
            self.angle += -3
    


    def updateImage(self, left_on, right_on):
        # Update the image based on thruster state
        if left_on and right_on:
            self.current_surface = self._create_rocket_surface(left=True, right=True)
        elif left_on:
            self.current_surface = self._create_rocket_surface(left=True, right=False)
        elif right_on:
            self.current_surface = self._create_rocket_surface(left=False, right=True)
        else:
            self.current_surface = self.img_idle
            

