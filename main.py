#!/usr/bin/env python3


import pygame
import random
import config

from rocket import Rocket
from environment import Environment
from control import Control
from wind import Wind
from graph import Graph

# Initialize pygame
pygame.init()

# Screen setup
environment = Environment()
fps = config.FPS
dt = config.DT

# Player
player = Rocket()
player.setPosition(100, 100, 0.0)

clock = pygame.time.Clock()
running = True

contt = Control(player)
wind = Wind()

xTarget = 0
yTarget = 0
windSpeed = 0

#count = 0

graphData = Graph()


while running:
    clock.tick(fps)
    environment.screen.fill((255, 255, 255)) # white

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    contt.steerRocket(player, dt, xTarget, yTarget)
    environment.checkBounds(player)
    
    # add gusts of wind at random moments
    wind.applyWind(player, dt, environment)
    
    # create and draw target
    xTarget, yTarget = environment.createTarget(player)
 
    # draw rocket
    rotated_image = pygame.transform.rotate(player.current_surface, -player.angle)
    rect = rotated_image.get_rect(center=(player.x, player.y))
    environment.screen.blit(rotated_image, rect.topleft)
    
    pygame.display.flip()
    
    # create a graph
    done = graphData.createGraph(player, xTarget, yTarget, wind)
    if done:
        break

pygame.quit()

graphData.showGraph()
