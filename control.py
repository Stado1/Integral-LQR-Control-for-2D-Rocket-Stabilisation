#!/usr/bin/env python3

import pygame
import random
import numpy as np
import scipy.linalg
import config

class Control:
    def __init__(self, player):

        self.A = np.array([[0, 1, 0, 0, 0, 0],
                           [0, 0, 0, 0, player.gravity, 0],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1],
                           [0, 0, 0, 0, 0, 0]])
                           
        self.B = np.array([[0, 0],
                           [0, 0],
                           [0, 0],
                           [-1/player.mass, -1/player.mass],
                           [0, 0],
                           [player.d/player.inertia, -player.d/player.inertia]])

        self.C = np.array([[1, 0, 0, 0, 0, 0],  # Track X
                           [0, 0, 1, 0, 0, 0]]) # Track Y
        
        n_states = self.A.shape[0]
        n_controls = self.B.shape[1]
        n_integral = self.C.shape[0]

        # Augment A and B matrices
        A_top = np.hstack((self.A, np.zeros((n_states, n_integral))))
        A_bot = np.hstack((self.C, np.zeros((n_integral, n_integral))))
        self.A_aug = np.vstack((A_top, A_bot))
        
        self.B_aug = np.vstack((self.B, np.zeros((n_integral, n_controls))))

        # Augment Q matrix
        # [x, x_dot, y, y_dot, theta, theta_dot, int_x, int_y]
        self.Q_aug = np.diag([0.1, 0.01, 0.1, 0.01, 1000000, 0.5, 0.8, 0.8])
        self.R = np.diag([1.0, 1.0])

        P = scipy.linalg.solve_continuous_are(self.A_aug, self.B_aug, self.Q_aug, self.R)
        self.K = np.linalg.inv(self.R) @ self.B_aug.T @ P
        
        # Initialize the integrator
        self.error_integral = np.zeros(n_integral)
        
        closed_loop_A = self.A_aug - self.B_aug @ self.K
        poles = np.linalg.eigvals(closed_loop_A)
        print("stability check (all real parts must be negative")
        print(poles.real)

    def steerRocket(self, player, dt, x_target, y_target):
        curr_state = np.array([
            player.x,
            player.x_speed,
            player.y,
            player.y_speed,
            np.deg2rad(player.angle),
            np.deg2rad(player.angle_speed)
        ])
        
#        print(self.error_integral)
        
        target_state = np.array([x_target, 0, y_target, 0, 0, 0])
        
        error = curr_state - target_state
        
        # Update the integral of the error
        limit = 1000
        threshold = 200  # pixels
        pos_error = self.C @ error
        if np.linalg.norm(pos_error) < threshold:
            self.error_integral += pos_error * dt
            self.error_integral = np.clip(self.error_integral, -limit, limit)
        else:
            self.error_integral = np.zeros(self.C.shape[0])
        
        
        # Create augmented error vector [error, integral_error]
        aug_error = np.concatenate((error, self.error_integral))
        
        # Compute control law
        u = -self.K @ aug_error

        # Standard mixer and motor logic
        hover_force = (player.mass * player.gravity) / 2
        player.force_thrusterL = hover_force + u[0]
        player.force_thrusterR = hover_force + u[1]
        
        maxForce = player.max_force_thruster
        player.force_thrusterL = np.clip(player.force_thrusterL, 0, maxForce)
        player.force_thrusterR = np.clip(player.force_thrusterR, 0, maxForce)
        
        leftMotor = player.force_thrusterL > 0
        rightMotor = player.force_thrusterR > 0
        
        player.movePhysics(dt, leftMotor, rightMotor)


