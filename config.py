#!/usr/bin/env python3

# ======================
# Simulation
# ======================
FPS = 60
DT = 1 / FPS

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SAFETY_MARGIN = 0

# ======================
# Rocket Physics
# ======================
ROCKET_MASS = 2
ROCKET_WIDTH = 120
ROCKET_HEIGHT = 20
THRUSTER_WIDTH = 20
FLAME_HEIGHT = 25

GRAVITY = 1000
MAX_THRUSTER_FORCE = 1200

# ======================
# Wind
# ======================
WIND_SPEED_MIN = 30
WIND_SPEED_MAX = 50
WIND_DURATION = 1000
WIND_DRAG_FACTOR = 10.0

# ======================
# Targeting
# ======================
TARGET_MARGIN = 40
TARGET_SPAWN_MARGIN = 200
TIME_ON_TARGET = 600 #frames

# ======================
# Graph
# ======================
GRAPH_DURATION = 2000 # frames


