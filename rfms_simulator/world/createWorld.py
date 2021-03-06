#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Author: Italo Barros
Email: ircbarros@pm.me
License: MIT
An grid generator using the PyGame module!

This module will create a New World Grid to run the Path Planning Algorithms.

For more informations take a look at the "WorldGrid" Class.

Classes:

    WorldGrid: Create a new World Grid with specified or inputed Arguments

Comments:

If you are using VS Code, please install the Better Comments Extension:
    # Indicates the Method
    #* Indicates some Important Information
    #! Indicates a deprecated or Warning Information
    #? Indicates possible future changes and questions
    #TODO: Indicates the future changes and optimizations
Need to change the code? Refactor? Help the next developer! Use a 
Style Guide to help others understand of your code. For more informations
about the Google Style Guide used here go to:
https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
'''

import os
import sys
import time
import pygame
import heapq
from collections import deque


# GLOBAL VARIABLES
#* Load the PyGame Vector2 lib
vec = pygame.math.Vector2
#* START POINT
START = (0,0)
#* GOAL POINT
GOAL = (9,3)
#* SET the DEFAULT Grid Width
GRID_WIDTH = 12
#* SET the DEFAULT Grid Height
GRID_HEIGHT = 9
#* SET the DEFAULT Width and Height of the Grid Cells
CELL_WIDTH = 100
CELL_HEIGHT = 100
#* SET the DEFAULT Margin value
DEFAULT_CELL_MARGIN = 1
#* SET the DEFAULT World Colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_CYAN = (0, 255, 255)
COLOR_MAGENTA = (255, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_YELLOW_ROYAL = (250, 218, 94)
#* The Recharge Zone Color
COLOR_SOFT_YELLOW = (239, 217, 127)
COLOR_DARKGRAY = (40, 40, 40)
COLOR_MEDGRAY = (75, 75, 75)
COLOR_STATEGRAY = (211,211,211)
#* The Obstacles Color
COLOR_LIGHTGRAY = (170, 170, 169)
#* The Workers Color
COLOR_PRUSSIAN = (9, 71, 99)
#* The Delivery Zone Color
COLOR_CAROLINA = (118, 180, 214)
#* The Treadmill Zone Color
COLOR_INDEPENDENCE = (64, 90, 155)
#* The Pickup Zone Color
COLOR_VERMILION = (163, 44, 50)
#* The Dont Move Zone Color
COLOR_GRAYISH = (226, 230, 230)
#? For more RGB Colors go to:
# https://graf1x.com/shades-of-red-color-palette-hex-rgb-code/
#? To translate Corors to the Decimal RGB Format go to:
# https://www.colorhexa.com/
#* SET the DEFAULT FPS
FPS = 60
#* SET the DEFAUL VELOCITY
MAX_VELOCITY = 100
# OBSTACLES AND SOME CELL POSITIONS IN THE GRID
#! BE CAREFUL AND NOT TO SET CELL VALUE TO MORE THAN ONE VARIABLE!
#! ALSO CHECK THE FREE SPACE AVAILABLE!
#* SET the DEFAULT Obstacles (Pods)
OBSTACLES = [(1,1), (2,1), (3,1), (1,2), (2,2), (3,2),
             (5,1), (6,1), (7,1), (5,2), (6,2), (7,2),
             (1,4), (2,4), (3,4), (1,5), (2,5), (3,5),
             (5,4), (6,4), (7,4), (5,5), (6,5), (7,5)]
#* SET the DEFAULT Treadmill Zone
TREADMILL_ZONE = [(11, 8), (11, 7), (11, 6), (11, 5), (11, 4),
                  (11, 3), (11, 2), (11, 1), (11, 0)]
#* SET the DEFAULT Workers Zone
WORKERS_POS = [(10, 3)]
#* SET the DEFAULT Delivery Zone
DELIVERY_ZONE = [(9,2),(9,3), (9,4)]
#* SET the DEFAULT Recharge Zone Queue
RECHARGE_ZONE_QUEUE = [(0, 7), (1, 7), (2, 7), (3, 7)]
#* SET the DEFAUL Recharge Zoen
RECHARGE_ZONE = [(0, 8), (1, 8), (2, 8), (3, 8)]
#* SET the DEFAULT Pickup Zone Queue (Where the robots fills the empty pods)
PICKUP_ZONE_QUEUE = [(4, 7), (5, 7), (6, 7), (7, 7)]
#* SET the DEFAULT Pickup Zone
PICKUP_ZONE = [(4, 8), (5, 8), (6, 8), (7, 8)]
#* SET the DEFAUL Cells that the Robot Can't Move
#? In this case is the Column where the worker is located
DONT_MOVE = [(10, 8), (10, 7), (10, 6), (10, 5), (10,4),
             (10, 2), (10, 1), (10,0)]
# CENTER THE GRID TO THE MIDDLE OF THE SCREEN
os.environ['SDL_VIDEO_CENTERED'] = '1'
# DEFINE THE FONT NAME
font_name = pygame.font.match_font('dejavusans')
# INIT THE PYGAME MODULE
pygame.init()
# INIT THE PYGAME CLOCK
clock = pygame.time.Clock()

class WorldGrid:
    '''
    Create a Word Grid in a screen size defined by the user
    or by default using the cells and the grid size. Use this function
    if you DO NOT WANT THE SCREEN and ONLY THE NODE VALUES

    Attributes:

     (GRID_WIDTH, GRID_HEIGHT) (tuple)
     (CELL_WIDTH, CELL_HEIGHT) (tuple)
     [(OBSTACLE1_x, OBSTACLE1_y), ... ,(OBSTACLEX_x, OBSTACLEY_y)] (list)
     [(RECHARGE1_x, RECHARGE1_y), ... ,(RECHARGEX_x, RECHARGEY_y)] (list)
     [(TREADMILL1_x, TREADMILL1_y), ... ,(TREADMILLX_x, TREADMILLY_y)] (list)
     [(WORKERS1_x, WORKERS1_y), ... ,(WORKERSX_x, WORKERSY_y)] (list)
     [(DELIVERY1_x, DELIVERY1_y), ... ,(DELIVERYX_x, DELIVERYY_y)] (list)
     [(PICKUP1_x, PICKUP1_y), ... ,(PICKUPX_x, PICKUPY_y)] (list)
     [(DONTMOVE_x, DELIVERY1_y), ... ,(DELIVERYX_x, DELIVERYY_y)] (list)
    
        Where:

            GRID_WIDTH (int)
            GRID_HEIGHT (int)
            CELL_WIDTH (int)
            CELL_HEIGHT (int)
            OBSTACLEX_x (int)
            OBSTACLEY_x (int)
            RECHARGEX_x (int)
            RECHARGEY_x (int)
            TREADMILLX_x (int)
            TREADMILLY_x (int)
            WORKERSX_x (int)
            WORKERSY_x (int)
            DELIVERYX_x (int)
            DELIVERYY_x (int)
            PICKUPX_x (int)
            PICKUPY_x (int)

    Args:

        (GRID_WIDTH, GRID_SIZE): An tuple with the desired grid size
        (CELL_WIDTH, CELL_HEIGHT): An tuple with the desired cell size
        (OBSTACLEX_x, OBSTACLEY_y): An tuple with the desired obstacles positions
        (RECHARGEX_x, RECHARGEX_y): An tuple with the desired recharge stations positions
        (TREADMILLX_x, TREADMILLY_y): An tuple with the desired treadmill position
        (WORKERSX_x, WORKERSY_y): An tuple with the desired workers positions
        (DELIVERYX_x, DELIVERYY_y): An tuple with the desired delivery points positions

    Vars:

        GRID_WIDTH = The desired grid WIDTH
        GRID_HEIGHT = The desired grid HEIGHT
        CELL_WIDTH = The desired grid WIDTH
        CELL_HEIGHT = The desired grid HEIGHT
        OBSTACLEX_x = The Obstacle location on the Grid in pos. X
        OBSTACLEY_y = The Obstacle location on the Grid in pos. Y
        RECHARGEX_x = The Recharge location on the Grid in pos. X
        RECHARGEY_y = The Recharge location on the Grid in pos. Y
        TREADMILLX_x = The Treadmill location on the Grid in pos. X
        TREADMILLY_y = The Treadmill location on the Grid in pos. Y
        WORKERSX_x = The Workers location on the Grid in pos. X
        WORKERSY_y = The Workers location on the Grid in pos. Y
        DELIVERYX_x = The Delivery location on the Grid in pos. X
        DELIVERYY_y = The Delivery location on the Grid in pos. Y

    Returns:

        A Node Grid Graph with Obstacles, Recharge Zone, Treadmill Zone,
        Workers Zone, Delivery Zone with size e height inputed by the
        user WITHOUT SCREEN VISUALIZATION!

    [Examples]

        USER DEFINED VALUES:
        import grid
        world = grid.WorldGrid((10,10), (100,100), (2,2), (6,6), (9,9), (8,9), (8,8)) 
        >>> Will show a 10x10 Grid Screen with cells size 100x100 and obstacle
            at positions (2,2), recharge zone at position (6,6), treadmill
            at position (9,9), worker at position (8,9), and delivery at position
            (8,8)

        DEFAULT VALUES:
        import grid
        world = grid.WorldGrid()
        >>> Will show the DEFAULT grid (12x9) with cell size 100x100 and
            similar to the image on the github
    '''

    def __init__(self, world_grid_size = (GRID_WIDTH, GRID_HEIGHT),
                 world_cell_size = (CELL_WIDTH, CELL_HEIGHT),
                 world_obstacles_positions = OBSTACLES,
                 world_recharge_queue_positions = RECHARGE_ZONE_QUEUE,
                 world_recharge_positions = RECHARGE_ZONE,
                 world_treadmill_positions = TREADMILL_ZONE,
                 world_workers_positions = WORKERS_POS,
                 world_delivery_positions = DELIVERY_ZONE,
                 world_pickup_queue_positions = PICKUP_ZONE_QUEUE,
                 world_pickup_positions = PICKUP_ZONE,
                 world_dont_move = DONT_MOVE):
        # SET THE GRID SIZE USING LIST COMPREHENSION
        self.grid_size_width, self.grid_size_height = world_grid_size[0], world_grid_size[1]
        # SET THE CELL SIZE USING LIST COMPREHENSION
        self.cell_size_width, self.cell_size_height = world_cell_size[0], world_cell_size[1]
        # SET  THE OBSTACLES POSITION
        self.world_obstacles_position = world_obstacles_positions
        # SET THE RECHARGE ZONE QUEUE POSITION
        self.world_recharge_queue_position = world_recharge_queue_positions
        # SET THE RECHARGE ZONE POSITION
        self.world_recharge_position = world_recharge_positions
        # SET THE TREADMILL POSITION
        self.world_treadmill_position = world_treadmill_positions
        # SET THE WORKERS POSITIONS
        self.world_workers_positions = world_workers_positions
        # SET THE DELIVERY POSITIONS
        self.world_delivery_positions = world_delivery_positions
        # SET THE PICKUP QUEUE POSITIONS
        self.world_pickup_queue_positions = world_pickup_queue_positions
        # SET THE PICKUP POSITIONS
        self.world_pickup_positions = world_pickup_positions
        # SET THE CANT MOVE POSITIONS
        self.world_dont_move = world_dont_move
        # SET THE OBSTACLES VECTOR
        self.obstaclesPosition = []
        for obstacle in self.world_obstacles_position:
            self.obstaclesPosition.append(vec(obstacle))
        # SET THE TREADMILL VECTOR
        global treadmillPositionGlobal
        treadmillPositionGlobal = []
        for treadmill_zone in self.world_treadmill_position:
            treadmillPositionGlobal.append(vec(treadmill_zone))
        # SET THE WORKERS ZONE VECTOR
        global workersPositionGlobal
        workersPositionGlobal = []
        for worker_position in self.world_workers_positions:
            workersPositionGlobal.append(vec(worker_position))
        # SET THE DELIVERY AS GLOBAL
        global deliveryPositionGlobal
        deliveryPositionGlobal = []
        for delivery_position in self.world_delivery_positions:
            deliveryPositionGlobal.append(vec(delivery_position))
       # SET THE CANT MOVE ZONE VECTOR
        global dontMoveGlobal
        dontMoveGlobal = []
        for dont_move in self.world_dont_move:
            dontMoveGlobal.append(vec(dont_move))
       #* SET THE RECHARGE AND PICKUP QUEUE ZONE VECTOR
        global rechargeQueuePositionGlobal, pickupQueuePositionGlobal
        rechargeQueuePositionGlobal = []
        for recharge_queue_position in self.world_recharge_queue_position:
            rechargeQueuePositionGlobal.append(vec(recharge_queue_position))
        pickupQueuePositionGlobal = []
        for pickup_queue_position in self.world_pickup_queue_positions:
            pickupQueuePositionGlobal.append(vec(pickup_queue_position))
       #* SET THE RECHARGE AND PICKUP ZONE VECTOR
        global rechargePositionGlobal, pickupPositionGlobal
        rechargePositionGlobal = []
        for recharge_position in self.world_recharge_position:
            rechargePositionGlobal.append(vec(recharge_position))
        pickupPositionGlobal = []
        for pickup_position in self.world_pickup_positions:
            pickupPositionGlobal.append(vec(pickup_position))
        # CALCULATE THE SCREEN SIZE
        #* The Width will be the grid width size * the cell witdh size
        self.screen_width = self.grid_size_width * self.cell_size_width
        #* The Height will be the grid height size * the cell height size
        self.screen_height = self.grid_size_height * self.cell_size_height
        #* The screen will be a tuple with the previous values W x H
        self.screen = (self.screen_width, self.screen_height)
        # ? Allow acces to the screenSize, and cellSize variables
        # ? as global, Maybe there's a better way to do it?
        global screenSizeWidth, screenSizeHeight, cellSizeWidth, cellSizeHeight, screenSize
        screenSizeWidth = self.screen_width
        screenSizeHeight = self.screen_height
        cellSizeWidth = self.cell_size_width
        cellSizeHeight = self.cell_size_height
        screenSize = self.screen
        # SET ALLOWED CONNECTIONS
        # *Where I can travel? In this case LEFT, RIGHT, TOP, BOTTOM
        self.travel_left = vec(1, 0)
        self.travel_right = vec(-1, 0)
        self.travel_bottom = vec(0, 1)
        self.travel_top = vec(0, -1)
        # * In this way the allowed connections are
        self.allowed_connections = [self.travel_left, self.travel_right,
                                    self.travel_bottom, self.travel_top]
        # SETUP THE SCREEN
        global screen
        screen = pygame.display.set_mode(screenSize)
        print(
        '''
                         _           _____ _____________ 
                        | |         /  ___|  ___| ___  /
                        | |     __ _\ `--.| |__ | |_/ /
                        | |    / _` |`--. |  __||    / 
                        | |___| (_| /\__/ | |___| |\ \ 
                        \_____/\__,_\____/\____/\_| \_|
                  Laboratory of Systems Engineering and Robotics
                            João Pessoa, PB - Brazil
                            https://laser.ci.ufpb.br/
                        Dev.: https://github.com/Ircbarros
       ===================================================================
                Welcome to the Path Planning Grid World Simulator
            Remember to correctly discretize the grid! If you place a 
             10x10 grid (10m x 10m) with cells of size 100x100, the
               ratio will be 1 px = 1 cm. If you want a 100x100
                 (100m x 100m) grid, the blocks must be 10x10,
                               that is 10px = 1m
                    
             IF YOU DO NOT DISCRETIZE CORRECTLY THE PC WILL FREEEZE!
               (if you put a long grid with long cell values e.g.)
           * TO QUIT THE APPLICATION: PRESS 'ESC' OR EXIT
           * TO DRAWN OR REMOVE A OBSTACLE PRESS THE LEFT MOUSE BUTTON
           * TO SHOW THE OBSTACLES DRAWN: PRESS 'CTRL+S'
           * TO ADD AN OBSTACLE (GREY CELLS) IN THE SCREEN PRESS THE
             LEFT MOUSE BUTTON
           * TO REMOVE AN OBSTACLE (GREY CELLS) IN THE SCREEN PRESS
             THE MOUSE BUTTON AT THE CELL YOU WANT TO REMOVE
           * TO CHANGE THE GOAL POSITION PRESS THE RIGHT MOUSE BUTTON

       ===================================================================
        ''')
        print(f'\nCreating a Grid with Screen Size: {screenSizeWidth}px x {screenSizeHeight}px....\n')
        print(f'The Grid Size Values are: {self.grid_size_width}px x {self.grid_size_height}px\n')
        print(f'The Grid Cell Size Values are: {cellSizeWidth}px x {cellSizeHeight}px\n')
        print('Grid Objects:')
        print('.................')
        print(f'The Obstacles are located in:\n {self.obstaclesPosition}\n')
        print(f'The Recharge Queue Zone are located in:\n {rechargeQueuePositionGlobal}\n')
        print(f'The Recharge Zone are located in:\n {rechargePositionGlobal}\n')
        print(f'The Treadmill Zone are located in:\n {treadmillPositionGlobal}\n')
        print(f'The Workers Zone are located in:\n {workersPositionGlobal}\n')
        print(f'The Delivery Zone are located in:\n {deliveryPositionGlobal}\n')
        print(f'The Pickup Queue Zone are located in:\n {pickupQueuePositionGlobal}\n')
        print(f'The Pickup Zone are located in:\n {pickupPositionGlobal}\n')
        print(f"The Grid Cells block to robot movement are:\n {dontMoveGlobal}\n")

    def grid_in_bounds(self, node):
        ''' Define the Grid bounds an limits that the robot can visit
        '''
        #* If the robot is inside the bounds of the grid
        if 0 <= node.x < self.grid_size_width and 0 <= node.y < self.grid_size_height:
            #? The function will return TRUE anyway, just to add more readability
            return True

    def is_passable(self, node):
        ''' Define if a Grid Node is passable or if is a obstacle

        Returns:

            True: If the Node is Passable
            False: If Node 
        '''
        #* If the node is not in the obstacles vector
        if node not in self.obstaclesPosition:
            #* If the node is not in the treadmill vector
            if node not in treadmillPositionGlobal:
                #* If the node is not in the workers position vector
                if node not in workersPositionGlobal:
                    #* If the node is not in the don't move vector
                    if node not in dontMoveGlobal:
                        # TO USE THE BREATH SEARCH ONLY, USE THE FOLLOWS IFs
                        #if node not in rechargePositionGlobal
                            #if node note in pickupPositionGlobal
                        #? The function will return TRUE anyway,
                        #? just to add more readability
                        return True

    def find_neighbors(self, node):
        '''
        Find the node Neighbors filtering the walls and points outside the grid

        Returns:


            (neigbors) (filter object): The available neighbors node filtered in the
                                        Vec2d (PyGame) format

        '''
        #* The neighbors will be the connections available on that node
        neighbors = [node + connection for connection in self.allowed_connections]
        # FILTER THE NEIGHBORS
        #* Filter the Neigbors points outside the Grid and that are not passable
        neighbors = filter(self.grid_in_bounds, neighbors)    
        neighbors = filter(self.is_passable, neighbors)
        #! DO NOT USE THE PRINT BELLOW WILL BREAK THE FUNCTION
        # print(list(neighbors))
        return neighbors

    def draw_obstacles(self):
        '''
        Draw the obstacles (pods) in the grid

        Returns:

            The Obstacles cells (Pods) inserted in the Main Screen
        '''
        # For the obstacles in the obstacles zone do
        for obstacle in self.obstaclesPosition:
            # Draw a obstacle as a retancle with format of the cell size
            rect_obstacle = pygame.Rect(obstacle * cellSizeWidth,
                                        (cellSizeWidth-1, cellSizeHeight-1))
            pygame.draw.rect(screen, COLOR_LIGHTGRAY, rect_obstacle)
            self.obstacle_vector = vec(obstacle)
            # THE DIRECTORY WERE THE ROBOT IMG FILE IS LOCATED
            self.icon_dir = os.path.join(os.path.dirname(__file__), '../icons')
            # LOAD THE ROBOT IMG TO THE PYGAME MODULE
            self.obstacle_img = pygame.image.load(os.path.join(self.icon_dir, 'pod.png')).convert_alpha()
            # SCALE THE IMAGE
            self.obstacle_img = pygame.transform.scale(self.obstacle_img, (70,70))
            # FILL THE IMAGE WITH THE BLEND MODULE
            self.start_center = ((self.obstacle_vector.x * cellSizeWidth) + (cellSizeHeight / 2),
                                (self.obstacle_vector.y * cellSizeWidth) + (cellSizeHeight / 2))
            screen.blit(self.obstacle_img,
                        self.obstacle_img.get_rect(center=self.start_center))

    def draw_treadmill_zone(self):
        '''
        Draw the Treadmill zone in the grid

        Returns:

            The Treadmill Zone cells inserted in the Main Screen
        '''
        # For the cells in the treadmill zone do
        for treadmill_zone in treadmillPositionGlobal:
            self.treadmill_vector = vec(treadmill_zone)
            # THE DIRECTORY WERE THE ROBOT IMG FILE IS LOCATED
            self.icon_dir = os.path.join(os.path.dirname(__file__), '../icons')
            # LOAD THE ROBOT IMG TO THE PYGAME MODULE
            self.treadmill_img = pygame.image.load(os.path.join(self.icon_dir,
                                                   'treadmill.png')).convert_alpha()
            # SCALE THE IMAGE
            self.treadmill_img = pygame.transform.scale(self.treadmill_img, (100,100))
            # FILL THE IMAGE WITH THE BLEND MODULE
            self.start_center = ((self.treadmill_vector.x * cellSizeWidth) + (cellSizeHeight / 2),
                                (self.treadmill_vector.y * cellSizeWidth) + (cellSizeHeight / 2))
            screen.blit(self.treadmill_img,
                        self.treadmill_img.get_rect(center=self.start_center))

    def draw_workers_zone(self):
        '''
        Draws the Workers zone in the grid

        Returns:

            The Workers Zone cells inserted in the Main Screen
        '''
        # For the cells in the worker zone do
        for workers_zone in workersPositionGlobal:
            # Draw a obstacle as a retancle with format of the cell size
            rect_workers = pygame.Rect(workers_zone * cellSizeWidth,
                                       (cellSizeWidth-1, cellSizeHeight-1))
            pygame.draw.rect(screen, COLOR_PRUSSIAN, rect_workers)

    def draw_delivery_zone(self):
        '''
        Draw the Delivery zone cells in the grid

        Returns:

            The Delivery Zone cells inserted in the Main Screen
        '''
        # For the cells in the delivery zone do
        for delivery_zone in deliveryPositionGlobal:
            # Draw a obstacle as a retancle with format of the cell size
            rect_delivery = pygame.Rect(delivery_zone * cellSizeWidth,
                                        (cellSizeWidth-1, cellSizeHeight-1))
            pygame.draw.rect(screen, COLOR_CAROLINA, rect_delivery)

    def draw_grid(self):
        '''
        Draws the Grid Cells

        Returns:

            The Grid cells inserted in the Main Screen
        '''
        # FOR X VALUES IN RANGE OF SCREEN WIDTH AND CELL WIDTH DO
        for x in range(0, screenSizeWidth, cellSizeWidth):
            # DRAW A LINE IN THE SCREEN WITH COLOR FROM 0 TO THE HEIGHT
            pygame.draw.line(screen, COLOR_DARKGRAY, (x, 0), (x, screenSizeHeight))
        # FOR X VALUES IN RANGE OF SCREEN HEIGHT AND CELL HEIGHT DO
        for y in range(0, screenSizeHeight, cellSizeHeight):
            # DRAW A LINE IN THE SCREEN WITH COLOR FROM 0 TO THE WIDTH
            pygame.draw.line(screen, COLOR_DARKGRAY, (0, y), (screenSizeWidth, y))

    def draw_queue_recharge_zone(self):
        '''
        Draw the Recharge Queue zone in the grid
    
        Returns:

            The Recharge Queue Zone cells inserted in the Main Screen
        '''
        # For the cells in the delivery zone do
        for queue_recharge_zone in rechargeQueuePositionGlobal:
            # Draw a obstacle as a retancle with format of the cell size
            rect_recharge = pygame.Rect(queue_recharge_zone * cellSizeWidth,
                                        (cellSizeWidth-1, cellSizeHeight-1))
            pygame.draw.rect(screen, COLOR_SOFT_YELLOW, rect_recharge)
            self.queue_recharge_vector = vec(queue_recharge_zone)
            # THE DIRECTORY WERE THE ROBOT IMG FILE IS LOCATED
            self.icon_dir = os.path.join(os.path.dirname(__file__), '../icons')
            # LOAD THE ROBOT IMG TO THE PYGAME MODULE
            self.queue_recharge_arrow = pygame.image.load(os.path.join(self.icon_dir,
                                                          'arrow_white.png')).convert_alpha()
            # SCALE THE IMAGE
            self.queue_recharge_arrow = pygame.transform.scale(self.queue_recharge_arrow,
                                                               (50,50))
            # FILL THE IMAGE WITH THE BLEND MODULE
            self.start_center = ((self.queue_recharge_vector.x * cellSizeWidth) + (cellSizeHeight / 2),
                                (self.queue_recharge_vector.y * cellSizeWidth) + (cellSizeHeight / 2))
            screen.blit(self.queue_recharge_arrow,
                        self.queue_recharge_arrow.get_rect(center=self.start_center))

    def draw_recharge_zone(self):
        '''
        Draw the Pickup Zone cells in the grid
    
        Returns:

            The Pickup Zone cells inserted in the Main Screen
        '''
        # For the cells in the pickup zone do
        for recharge_zone in rechargePositionGlobal:
            self.recharge_vector = vec(recharge_zone)
            # THE DIRECTORY WERE THE ROBOT IMG FILE IS LOCATED
            self.icon_dir = os.path.join(os.path.dirname(__file__), '../icons')
            # LOAD THE ROBOT IMG TO THE PYGAME MODULE
            self.recharge_img = pygame.image.load(os.path.join(self.icon_dir,
                                                          'recharge.png')).convert_alpha()
            # SCALE THE IMAGE
            self.recharge_img = pygame.transform.scale(self.recharge_img,
                                                       (90,90))
            # FILL THE IMAGE WITH THE BLEND MODULE
            self.start_center = ((self.recharge_vector.x * cellSizeWidth) + (cellSizeHeight / 2),
                                (self.recharge_vector.y * cellSizeWidth) + (cellSizeHeight / 2))
            screen.blit(self.recharge_img,
                        self.recharge_img.get_rect(center=self.start_center))

    def draw_queue_pickup_zone(self):
        '''
        Draw the Pickup Queue Zone cells in the grid
    
        Returns:

            The Pickup Queue Zone cells inserted in the Main Screen
        '''
        # For the cells in the pickup zone do
        for queue_pickup_zone in pickupQueuePositionGlobal:
            # Draw a obstacle as a retancle with format of the cell size
            rect_pickup = pygame.Rect(queue_pickup_zone * cellSizeWidth,
                                      (cellSizeWidth-1, cellSizeHeight-1))
            pygame.draw.rect(screen, COLOR_VERMILION, rect_pickup)
            self.queue_pickup_vector = vec(queue_pickup_zone)
            # THE DIRECTORY WERE THE ROBOT IMG FILE IS LOCATED
            self.icon_dir = os.path.join(os.path.dirname(__file__), '../icons')
            # LOAD THE ROBOT IMG TO THE PYGAME MODULE
            self.queue_pickup_arrow = pygame.image.load(os.path.join(self.icon_dir,
                                                          'arrow_white.png')).convert_alpha()
            # SCALE THE IMAGE
            self.queue_pickup_arrow = pygame.transform.scale(self.queue_pickup_arrow,
                                                             (50,50))
            # FILL THE IMAGE WITH THE BLEND MODULE
            self.start_center = ((self.queue_pickup_vector.x * cellSizeWidth) + (cellSizeHeight / 2),
                                (self.queue_pickup_vector.y * cellSizeWidth) + (cellSizeHeight / 2))
            screen.blit(self.queue_pickup_arrow,
                        self.queue_pickup_arrow.get_rect(center=self.start_center))

    def draw_pickup_zone(self):
        '''
        Draw the Pickup Zone cells in the grid
    
        Returns:

            The Pickup Zone cells inserted in the Main Screen
        '''
        # For the cells in the pickup zone do
        for pickup_zone in pickupPositionGlobal:
            self.pickup_vector = vec(pickup_zone)
            # THE DIRECTORY WERE THE ROBOT IMG FILE IS LOCATED
            self.icon_dir = os.path.join(os.path.dirname(__file__), '../icons')
            # LOAD THE ROBOT IMG TO THE PYGAME MODULE
            self.pickup_img = pygame.image.load(os.path.join(self.icon_dir,
                                                             'pickup.png')).convert_alpha()
            # SCALE THE IMAGE
            self.pickup_img = pygame.transform.scale(self.pickup_img,
                                                             (90,90))
            # FILL THE IMAGE WITH THE BLEND MODULE
            self.start_center = ((self.pickup_vector.x * cellSizeWidth) + (cellSizeHeight / 2),
                                (self.pickup_vector.y * cellSizeWidth) + (cellSizeHeight / 2))
            screen.blit(self.pickup_img,
                        self.pickup_img.get_rect(center=self.start_center))

    def draw_arrows(self):
        '''
        Draws Arrows in the Grid

        Returns:

            An arrow in the Grid Cell with Defined Direction
        '''
        # THE DIRECTORY WERE THE ARROW IMG FILE IS LOCATED
        self.icon_dir = os.path.join(os.path.dirname(__file__), '../icons')
        # CREATE A GLOBAL DIC WITH THE ARROWS
        self.arrows = {}
        # LOAD THE ARROW IMG TO THE PYGAME MODULE
        self.arrow_img = pygame.image.load(os.path.join(self.icon_dir, 'arrow_black.png')).convert_alpha()
        # SCALE THE IMAGE
        self.arrow_img = pygame.transform.scale(self.arrow_img, (50,50))
        # SET ARROW DIRECTIONS
        #* Since the arrow icon is pointing to right we need the arrows in other directions
        self.arrow_point_up = (1,0)
        self.arrow_point_down = (0,1)
        self.arrow_point_left = (-1,0)
        self.arrow_pont_right = (0,-1)
        # CREATE A LIST WITH THE ARROWS POINTING IN ALL DIRECTIONS
        for direction in [self.arrow_point_up, self.arrow_point_down,
                          self.arrow_point_left, self.arrow_pont_right]:
            # ROTATE THE ARROWS
            self.arrows[direction] = pygame.transform.rotate(self.arrow_img,
                                                             vec(direction).angle_to(vec(self.arrow_point_up)))

    def draw_start(self, start):
        '''
        Adjust the Start Icon and draw in the Grid


        Args:

            start (tuple): The start Position (X,Y)

        Returns:

            The Start icon translated to the PyGame Library and Draw
            at the specified START location
        '''
        # SET THE GOAL
        self.start = vec(start)
        # THE DIRECTORY WERE THE ROBOT IMG FILE IS LOCATED
        self.icon_dir = os.path.join(os.path.dirname(__file__), '../icons')
        # LOAD THE ROBOT IMG TO THE PYGAME MODULE
        self.start_img = pygame.image.load(os.path.join(self.icon_dir, 'start.png')).convert_alpha()
        # SCALE THE IMAGE
        self.start_img = pygame.transform.scale(self.start_img, (50,50))
        # FILL THE IMAGE WITH THE BLEND MODULE
        self.start_img.fill((255, 0, 0, 255), special_flags = pygame.BLEND_RGBA_MULT)
        self.start_center = ((self.start.x * cellSizeWidth) + (cellSizeHeight / 2),
                             (self.start.y *cellSizeWidth) + (cellSizeHeight / 2))
        screen.blit(self.start_img,
                    self.start_img.get_rect(center = self.start_center))

    def draw_goal(self, goal):
        '''
        Adjust the Goals Icon and draw in the Grid

        Args:

            goal (tuple): The goal Position (X,Y)

        Returns:

            The Goal icon translated to the PyGame Library and Draw
            at the specified GOAL location
        '''
        # SET THE GOAL
        self.goal = vec(goal)
        # THE DIRECTORY WERE THE ROBOT IMG FILE IS LOCATED
        self.icon_dir = os.path.join(os.path.dirname(__file__), '../icons')
        # LOAD THE ROBOT IMG TO THE PYGAME MODULE
        self.goal_img = pygame.image.load(os.path.join(self.icon_dir, 'goal.png')).convert_alpha()
        # SCALE THE IMAGE
        self.goal_img = pygame.transform.scale(self.goal_img, (50,50))
        # FILL THE IMAGE WITH THE BLEND MODULE
        #self.goal_img.fill(special_flags = pygame.BLEND_RGBA_MULT)
        self.goal_center = ((self.goal.x * cellSizeWidth) + (cellSizeHeight / 2),
                            (self.goal.y *cellSizeWidth) + (cellSizeHeight / 2))
        screen.blit(self.goal_img,
                    self.goal_img.get_rect(center = self.goal_center))

    def draw_text(self, text, size, color, x, y, align="topleft"):
        '''
        Draws the Text in the Screen using the Pygame Module

        Args:

            text (Pygame function): The text desired
            size (int): The size of the Text
            color (tuple): The Desired Color
            x (int): The X position in the Screen
            y (int): The Y position in the Screen
            align (str): The Alignment Desired

        '''
        self.font = pygame.font.Font(font_name, size)
        self.text_surface = self.font.render(text, True, color)
        self.text_rect = self.text_surface.get_rect(**{align: (x, y)})
        screen.blit(self.text_surface, self.text_rect)

class WeightedGrid(WorldGrid):
    '''
    Create a Word Grid in a screen size defined by the user
    or by default using the cells and the grid size with Inheritance
    from the WorldGrid Class, creating then a Weighted Graph. The
    Recharge Zone and the Pickup Zone have more weight than the other
    nodes, and aren't obstacles.

    Attributes:

     (GRID_WIDTH, GRID_HEIGHT) (tuple)
     (CELL_WIDTH, CELL_HEIGHT) (tuple)
     [(OBSTACLE1_x, OBSTACLE1_y), ... ,(OBSTACLEX_x, OBSTACLEY_y)] (list)
     [(RECHARGE1_x, RECHARGE1_y), ... ,(RECHARGEX_x, RECHARGEY_y)] (list)
     [(TREADMILL1_x, TREADMILL1_y), ... ,(TREADMILLX_x, TREADMILLY_y)] (list)
     [(WORKERS1_x, WORKERS1_y), ... ,(WORKERSX_x, WORKERSY_y)] (list)
     [(DELIVERY1_x, DELIVERY1_y), ... ,(DELIVERYX_x, DELIVERYY_y)] (list)
     [(PICKUP1_x, PICKUP1_y), ... ,(PICKUPX_x, PICKUPY_y)] (list)
     [(DONTMOVE_x, DELIVERY1_y), ... ,(DELIVERYX_x, DELIVERYY_y)] (list)
    
        Where:

            GRID_WIDTH (int)
            GRID_HEIGHT (int)
            CELL_WIDTH (int)
            CELL_HEIGHT (int)
            OBSTACLEX_x (int)
            OBSTACLEY_x (int)
            RECHARGEX_x (int)
            RECHARGEY_x (int)
            TREADMILLX_x (int)
            TREADMILLY_x (int)
            WORKERSX_x (int)
            WORKERSY_x (int)
            DELIVERYX_x (int)
            DELIVERYY_x (int)
            PICKUPX_x (int)
            PICKUPY_x (int)

    Args:

        (GRID_WIDTH, GRID_SIZE): An tuple with the desired grid size
        (CELL_WIDTH, CELL_HEIGHT): An tuple with the desired cell size
        (OBSTACLEX_x, OBSTACLEY_y): An tuple with the desired obstacles positions
        (RECHARGEX_x, RECHARGEX_y): An tuple with the desired recharge stations positions
        (TREADMILLX_x, TREADMILLY_y): An tuple with the desired treadmill position
        (WORKERSX_x, WORKERSY_y): An tuple with the desired workers positions
        (DELIVERYX_x, DELIVERYY_y): An tuple with the desired delivery points positions

    Vars:

        GRID_WIDTH = The desired grid WIDTH
        GRID_HEIGHT = The desired grid HEIGHT
        CELL_WIDTH = The desired grid WIDTH
        CELL_HEIGHT = The desired grid HEIGHT
        OBSTACLEX_x = The Obstacle location on the Grid in pos. X
        OBSTACLEY_y = The Obstacle location on the Grid in pos. Y
        RECHARGEX_x = The Recharge location on the Grid in pos. X
        RECHARGEY_y = The Recharge location on the Grid in pos. Y
        TREADMILLX_x = The Treadmill location on the Grid in pos. X
        TREADMILLY_y = The Treadmill location on the Grid in pos. Y
        WORKERSX_x = The Workers location on the Grid in pos. X
        WORKERSY_y = The Workers location on the Grid in pos. Y
        DELIVERYX_x = The Delivery location on the Grid in pos. X
        DELIVERYY_y = The Delivery location on the Grid in pos. Y

    Returns:

        A Weighted Node Grid Graph with Obstacles, Recharge Zone, Treadmill
        Zone, Workers Zone, Delivery Zone with size e height inputed by the
        user.
    '''

    def __init__(self, world_grid_size = (GRID_WIDTH, GRID_HEIGHT),
                 world_cell_size = (CELL_WIDTH, CELL_HEIGHT),
                 world_obstacles_positions = OBSTACLES,
                 world_recharge_queue_positions = RECHARGE_ZONE_QUEUE,
                 world_recharge_positions = RECHARGE_ZONE,
                 world_treadmill_positions = TREADMILL_ZONE,
                 world_workers_positions = WORKERS_POS,
                 world_delivery_positions = DELIVERY_ZONE,
                 world_pickup_queue_positions = PICKUP_ZONE_QUEUE,
                 world_pickup_positions = PICKUP_ZONE,
                 world_dont_move = DONT_MOVE):
 
        super().__init__()
        # CREATE A DIC TO SAVE THE NODE WEIGHTS
        self.weights = {}
        # CREATE WEIGHTS FOR THE RECHARGE ZONE
        for Recharge_Queue in self.world_recharge_position:
            self.weights[Recharge_Queue] = 50
        for Recharge in self.world_recharge_position:
            self.weights[Recharge] = 40
        # CREATE WEIGHTS FOR THE PICKUP ZONE
        for Pickup_Queue in self.world_pickup_queue_positions:
            self.weights[Pickup_Queue] = 50
        for Pickup in self.world_pickup_positions:
            self.weights[Pickup] = 40

    # COST FUNCTION
    def cost(self, from_node, to_node):
        '''
        The cost function responsible to put weights at each grid cell
        node.

        Args:

            from_node (tuple)
            to_node (tuple)
        
        Vars:

            from_node: A tuple with the actual node cell position (X,Y)
            to_node: A tuple with the desired node cell position (X,Y)


        Returns:

            The cell node weighted in 10 if moving horizontal/vertical
            and 14 if moving diagonal
        '''
        #* If the move is horizontal or vertical the cost is 1
        #? Uses the Length Squared function of PyGame to return the
        #? Euclidean length of the vector
        if (vec(to_node) - vec(from_node)).length_squared() == 1:
            #* Multiply to 10 to work only with integers
            return self.weights.get(to_node, 0) + 10
        #* If the move is diagonal, the cost is 1.4 (diagonal move in squares)
        else:
            #* Multiply to 10 to work only with integers
            return self.weights.get(to_node, 0) + 14

class PriorityQueue:
    '''
    Class responsible to create de Priority Queue using the heapq
    library to elaborate the path planning algorithm based on the
    cells with lower cost values

    '''
    def __init__(self):
        #* Initwith a empty list of nodes
        self.nodes = []
    
    def put(self, node, cost):
        '''
        Function responsible to insert a node with a cost to the
        searched nodes

        Args:

            node (tuple)
            cost (int)
        
        Vars:

            node: A tuple with the actual node cell position (X,Y)
            cost: A integer with the actual cell cost value


        Returns:

            The cell node weighted in 10 if moving horizontal/vertical
            and 14 if moving diagonal inserted to the heapq node list
        '''
        #* Put the nodes and the cost at the Heap Queue
        heapq.heappush(self.nodes, (cost, node))
    
    def get(self):
        '''
        Function responsible to get a node with his cost

        Returns:

            The cell node cost
        '''
        #* Get the node in the Priority Queue
        return heapq.heappop(self.nodes)[1]

    def empty(self):
        '''
        Function responsible to check if the search is finished
        and that's no more frontier nodes available

        Returns:

            True if the search finishes
        '''
        #* Check if the search ends
        return len(self.nodes) == 0

class Robots(pygame.sprite.Sprite):
    '''
    Adjust the Robot Icon and draw in the Grid as a Sprite

    Args:

        start (vector2d): The Robot start node position (X , Y)
                          in the Vector2d PyGame format
        goal (vector2d):  The Robot goal position (X, Y) in the
                          Vector2d PyGame format
        path (vector2d):  The Shortest Path the robot will run

    Returns:

        The Robot icon translated to the PyGame Library and Draw
        at the specified START location
    '''
    # The Sprite for the Robots
    def __init__(self, start, goal, path):

        pygame.sprite.Sprite.__init__(self)
        # THE PATH VARIABLES
        self.path = path
        self.start = start
        #* The Start used to Move the Robot
        self.start_pos = (int(start.x), int(start.y))
        self.goal_pos = goal
        # THE DIRECTORY WERE THE ROBOT IMG FILE IS LOCATED
        self.icon_dir = os.path.join(os.path.dirname(__file__), '../icons')
        # LOAD THE ROBOT IMG TO THE PYGAME MODULE
        self.image = pygame.image.load(os.path.join(self.icon_dir, 'robot.png')).convert_alpha()
        # SCALE THE IMAGE
        self.image = pygame.transform.scale(self.image, (50,50))
        # DRAWS A RECTANGLE FOR THE FIGURE
        self.rect = self.image.get_rect()
        # FILL THE IMAGE WITH THE BLEND MODULE
        self.rect.center = ((self.start.x * cellSizeWidth) + (cellSizeHeight / 2),
                            (self.start.y * cellSizeWidth) + (cellSizeHeight / 2))
        # SET THE ROTATION
        self.rotation = 0
        # SET THE SPEED
        self.x_speed = MAX_VELOCITY
        self.y_speed = MAX_VELOCITY
        # SET THE PATH HEAP WHERE THE ROBOT WILL MOVE
        self.robot_path_pop = deque([])
        # SET the PATH for the Robot as Global
        global robotPath, pathVector
        robotPath = deque([])
        pathVector = deque([])
        #* Where I can travel? In this case LEFT, RIGHT, TOP, BOTTOM
        self.move_left = vec(1, 0)
        self.move_bottom = vec(0, 1)
        self.move_right = vec(-1, 0)
        self.move_top = vec(0, -1)
        #* Set the Current position on the Node
        self.current_pos = self.path[(self.start_pos)] + self.start
        robotPath.extend([self.current_pos])
        path_vector_start = self.current_pos - self.start
        pathVector.extend([path_vector_start])
        while self.current_pos != self.goal_pos:
            self.path_vector = self.path[(self.current_pos.x, self.current_pos.y)]
            pathVector.extend([self.path_vector])
            self.current_pos = self.current_pos + self.path[(int(self.current_pos.x),
                                                             int(self.current_pos.y))]
            robotPath.extend([self.current_pos])         

        print(f'The robot path was the nodes: {list(robotPath)}\n')
        print(f'The robot movements desired is: {list(pathVector)}\n')

    def update(self):
        '''
        Update the Robot Location at every Frame when SPACE is Pressed

        Args:

            None
        
        Returns:

            The Robot icon translated to the PyGame Library and Draw
            at the Screen moving to START to GOAL along the shortest
            path found by the Search Algorithm.
        '''
        try:
            #* Pick the Path Vector 
            vector = pathVector.popleft()
            #* Move to Left
            if (vector.x == self.move_left.x) and (vector.y == self.move_left.y):

                self.rect.x += MAX_VELOCITY
            #* Move to Right
            elif (vector.x == self.move_right.x) and (vector.y == self.move_right.y):

                self.rect.x -= MAX_VELOCITY
            #* Move to Top
            elif (vector.x == self.move_top.x) and (vector.y == self.move_top.y):

                self.rect.y -= MAX_VELOCITY
            #* Move to Bottom
            else:

                self.rect.y += MAX_VELOCITY
        #* Finish the Animation
        except:
            print('------------------')
            print('Animation Finised!')
            print('------------------\n')
            print('To RESTART change the robot start or goal position and press SPACE\n')
            print('To QUIT close the Screen\n')

class Workers(pygame.sprite.Sprite):
    '''
    Adjust the Workers Icon and draw in the Grid as a Sprite

    Args:
        workers (Tuple): The workers start position (X , Y) 

    Returns:

        The Worker icon translated to the PyGame Library and Draw
        at the specified START location
    '''
    # The Sprite for the Robots
    def __init__(self, workers_pos):

        pygame.sprite.Sprite.__init__(self)

        for workers in workers_pos:
            workers_vector = vec(workers)
            # SET THE START NODE
            self.start = workers_vector
            # THE DIRECTORY WERE THE ROBOT IMG FILE IS LOCATED
            self.icon_dir = os.path.join(os.path.dirname(__file__), '../icons')
            # LOAD THE ROBOT IMG TO THE PYGAME MODULE
            self.image = pygame.image.load(os.path.join(self.icon_dir, 'worker.png')).convert_alpha()
            # SCALE THE IMAGE
            self.image = pygame.transform.scale(self.image, (50,50))
            # DRAWS A RECTANGLE FOR THE FIGURE
            self.rect = self.image.get_rect()
            # FILL THE IMAGE WITH THE BLEND MODULE
            self.rect.center = ((self.start.x * cellSizeWidth) + (cellSizeHeight / 2),
                                    (self.start.y * cellSizeWidth) + (cellSizeHeight / 2))
    
    def update(self):

        # SET THE SPEED
        self.x_speed = 0
        self.y_speed = 0

class TreadmillItems(pygame.sprite.Sprite):
    '''
    Adjust the Treadmill Items and draw in the Grid as a Sprite

    Args:
        items_start (Tuple): The items start position (X, Y) in
                            the treadmill

    Returns:

        The Items icon are translated to the PyGame Library and Drawn
        at the specified START location
    '''
    # The Sprite for the Robots
    def __init__(self, items_start=(11,0)):

        pygame.sprite.Sprite.__init__(self)
    
        # SET THE START NODE
        self.start = vec(items_start)
        # THE DIRECTORY WERE THE ROBOT IMG FILE IS LOCATED
        self.icon_dir = os.path.join(os.path.dirname(__file__), '../icons')
        # LOAD THE ROBOT IMG TO THE PYGAME MODULE
        self.image = pygame.image.load(os.path.join(self.icon_dir, 'box.png')).convert_alpha()
        # SCALE THE IMAGE
        self.image = pygame.transform.scale(self.image, (50,50))
        # DRAWS A RECTANGLE FOR THE FIGURE
        self.rect = self.image.get_rect()
        # FILL THE IMAGE WITH THE BLEND MODULE
        self.rect.center = ((self.start.x * cellSizeWidth) + (cellSizeHeight / 2),
                                (self.start.y * cellSizeWidth) + (cellSizeHeight / 2))
    
    def update(self):

        self.rect.y += 2

        if self.rect.top > screenSizeHeight:
            self.rect.bottom = 0