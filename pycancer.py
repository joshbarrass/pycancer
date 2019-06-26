#!/usr/bin/env python3.6

import math
import time

import pygame
from pygame.locals import *

from constants import *
from sprites import Spinner

class App():
    def __init__(self,width,height,title="pygame window",icon=None):
        self.running = False
        self.size = (width,height)
        self.title = title
        self.icon = icon
        pygame.init()

    def init(self):
        """Commands to be processed before the application starts"""
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(self.title)
        if self.icon != None:
            self.icon = pygame.image.load(self.icon)
            pygame.display.set_icon(self.icon)
        self.display = pygame.display.set_mode(self.size, pygame.HWSURFACE | DOUBLEBUF)

        self.small_font = pygame.font.SysFont("sans-serif",15)
        self.medium_font = pygame.font.SysFont("sans-serif",22)

        # Open the fidget spinner sprite
        self.spinner = Spinner(SPRITE_PATH, (self.size[0]//2,self.size[1]//2))
        self.spinner.set_centre_pos((self.size[0]/2,self.size[1]/2))

        self.reset()

        self.difficulty = 1
        self.legendary = False ## will be interpreted as int

        return True

    def reset(self):
        # displayed as acceleration in-game as in the original
        self.speed = 0
        self.highest_speed = 0

        # time in the 90s tracking
        self.time_start = None
        self.time_spent_in_90s = 0
        self.highest_time_spent_in_90s = 0

        # reset spinner position
        self.spinner.angle = 0
        self.spinner.rotate(0)

        self.background = 0

        self.pressed = False

    def __loop__(self):
        """Commands processed every frame"""
        ## speed decreases by 12.5 every second
        #self.speed -= 12.5*(self.clock.get_time()/1000)
        ## exponential speed decrease makes it slightly easier the faster you go
        ## this is to recreate the slight lag in scratch as the spinner got faster
        self.speed -= (10 + 2.5*math.exp(-self.speed/200))*(self.clock.get_time()/1000)
        if self.speed < 0:
            self.speed = 0

        if self.speed > self.highest_speed:
            self.highest_speed = self.speed

        if self.speed >= 90:
            self.background = (self.background+1)%len(BACKGROUND_COLOURS)
            if self.time_start is None:
                self.time_start = time.time()
            self.time_spent_in_90s = time.time() - self.time_start
            if self.time_spent_in_90s > self.highest_time_spent_in_90s:
                self.highest_time_spent_in_90s = self.time_spent_in_90s
        else:
            self.background = 0
            self.time_spent_in_90s = 0
            self.time_start = None
            
        ## Rotate the spinner according to the angular speed
        self.spinner.rotate(-self.speed)
        ## set the hue shift as it would in scratch
        self.spinner.set_hueshift(self.speed/360)

    def __events__(self, event):
        """Event Handling"""
        if event.type == pygame.QUIT:
            self.running = False

        ## Handle key press
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            if not self.pressed:
                self.pressed = True
                self.speed += (5- self.speed/(39 - self.legendary*10 - self.difficulty))
        if event.type == pygame.KEYUP and event.key == pygame.K_s:
            self.pressed = False

        ## Enter to reset
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.reset()

    def __render__(self):
        """Rendering"""
        # Clear background
        self.display.fill(BACKGROUND_COLOURS[self.background])
        self.spinner.draw(self.display)

        # draw texts
        fps_text = self.small_font.render("FPS: "+str(round(self.clock.get_fps(),1)), 1, COLOUR_BLACK)
        self.display.blit(fps_text, (0,0))
        
        speed_text = self.medium_font.render("Acceleration: "+str(round(self.speed,1)), 1, COLOUR_BLACK)
        self.display.blit(speed_text, (0,20))
        
        highest_text = self.medium_font.render("Highest: "+str(round(self.highest_speed,1)), 1, COLOUR_BLACK)
        highest_text_rect = highest_text.get_rect()
        highest_text_rect.topright = (self.size[0]-3, 20)
        self.display.blit(highest_text, highest_text_rect)

        nineties_text = self.medium_font.render("Time Spent Running in the 90s: "+str(round(self.time_spent_in_90s,1))+"s", 1, COLOUR_BLACK)
        nineties_text_rect = nineties_text.get_rect()
        nineties_text_rect.bottomleft = (3, self.size[1])
        self.display.blit(nineties_text, nineties_text_rect)

        highest_nineties_text = self.medium_font.render("Longest Time Spent Running in the 90s: "+str(round(self.highest_time_spent_in_90s,1))+"s", 1, COLOUR_BLACK)
        highest_nineties_text_rect = highest_nineties_text.get_rect()
        highest_nineties_text_rect.bottomright = (self.size[0]-3, self.size[1])
        self.display.blit(highest_nineties_text, highest_nineties_text_rect)
        
        pygame.display.flip()

    def __cleanup__(self,e=None):
        """Commands to be processed when quiiting"""
        pygame.quit()
        if e != None:
            raise e

    def start(self,fps_limit=0):
        """Start the application"""
        self.fps_limit = fps_limit #This way fps can be dynamically adjusted
        ex = None
        try:
            self.running = self.init()
        except Exception as e:
            self.running = False
            ex = e
        
        while self.running == True:
            try:
                self.clock.tick(self.fps_limit)
                for event in pygame.event.get():
                    self.__events__(event)

                self.__loop__()
                self.__render__()
            except Exception as e:
                self.running = False
                ex = e
    

        self.__cleanup__(ex)

if __name__ == "__main__":
    app = App(WINDOW_SIZE[0], WINDOW_SIZE[1],
              WINDOW_NAME)
    app.start(FPS_LIMIT)
