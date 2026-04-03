#!/usr/bin/env python3

import pygame
import random
import numpy as np
import config

class Wind:
    def __init__(self):
        self.windSpeedMin = config.WIND_SPEED_MIN
        self.windSpeedMax = config.WIND_SPEED_MAX
        self.windSpeed = 0
        self.windDirection = 1 # 1=to the left, -1=to the right
        self.windDuration = config.WIND_DURATION # frames
        self.windTarget = 0
        
        self.counter = 900
        
    def applyWind(self, player, dt, environment):

        if (self.counter == self.windDuration):
            if bool(random.getrandbits(1)): #get random wind direction
                self.windDirection *= -1
            self.windTarget = random.randint(self.windSpeedMin, self.windSpeedMax) * self.windDirection
            self.counter = 0
          
        if (self.counter % 15 == 0):
            if (self.windSpeed > self.windTarget):
                self.windSpeed -= random.randint(-1, 2)
            if (self.windSpeed < self.windTarget):
                self.windSpeed += random.randint(-1, 2)
            if (self.windSpeed == self.windTarget):
                self.windSpeed += random.randint(-2, 2)
        
        dragFactor = config.WIND_DRAG_FACTOR
        Fwind = dragFactor * self.windSpeed
     
        player.x_speed += Fwind * dt / player.mass
        
        environment.printWindOnScreen(self.windSpeed, self.windSpeedMax)
        self.counter += 1

        
            
    


