#!/usr/bin/env python3.6

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

        # displayed as acceleration in-game as in the original
        self.speed = 0

        return True

    def __loop__(self):
        """Commands processed every frame"""
        self.speed += 5*self.clock.get_time()/1000

        ## Rotate the spinner according to the angular speed
        self.spinner.rotate(-self.speed)
        ## set the hue shift as it would in scratch
        self.spinner.set_hueshift(self.speed/360)

    def __events__(self, event):
        """Event Handling"""
        if event.type == pygame.QUIT:
            self.running = False

    def __render__(self):
        """Rendering"""
        # Clear background
        self.display.fill(BACKGROUND_COLOUR)
        self.spinner.draw(self.display)

        # draw texts
        fps_text = self.small_font.render("FPS: "+str(round(self.clock.get_fps(),1)), 1, COLOUR_BLACK)
        self.display.blit(fps_text, (0,0))
        speed_text = self.medium_font.render("Acceleration: "+str(round(self.speed,1)), 1, COLOUR_BLACK)
        self.display.blit(speed_text, (0,20))
        
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
