#!/usr/bin/env python3

import pygame
import random
import numpy as np
import config
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.count = 0
        self.duration = config.GRAPH_DURATION # frames
        
        # Data storage lists
        self.time_data = []
        self.player_x = []
        self.player_y = []
        self.target_x = []
        self.target_y = []
        self.wind_data = []
        

    def createGraph(self, player, xTarget, yTarget, wind):
        # create the 3 graphs here
        # one graph for the player.x and the xTarget VS time
        # one graph for the player.y and the yTarget VS time
        # one graph for the wind VS time
        
        # Record data for the current frame
        self.time_data.append(self.count)
        self.player_x.append(player.x)
        self.player_y.append(player.y)
        self.target_x.append(xTarget)
        self.target_y.append(yTarget)
        self.wind_data.append(wind.windSpeed)

        self.count += 1
        
        if self.count >= self.duration:
            return True
        return False
        
        
        
    def showGraph(self):
        # dispaly the graphs
        # Create a figure with 3 subplots (Vertical stack)
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
        fig.tight_layout(pad=5.0)

        # Plot 1: X Position vs Time
        ax1.plot(self.time_data, self.player_x, label='Rocket X', color='blue')
        ax1.plot(self.time_data, self.target_x, label='Target X', linestyle='--', color='orange')
        ax1.set_title('X Position Over Time')
        ax1.set_ylabel('Coordinate')
        ax1.legend()

        # Plot 2: Y Position vs Time
        ax2.plot(self.time_data, self.player_y, label='Rocket Y', color='red')
        ax2.plot(self.time_data, self.target_y, label='Target Y', linestyle='--', color='orange')
        ax2.set_title('Y Position Over Time')
        ax2.set_ylabel('Coordinate')
        ax2.legend()

        # Plot 3: Wind Force vs Time
        ax3.plot(self.time_data, self.wind_data, label='Wind Intensity', color='green')
        ax3.set_title('Wind Speed Over Time')
        ax3.set_xlabel('Frame')
        ax3.set_ylabel('Speed')
        ax3.legend()

        plt.show()
