import pygame

from object import Object

class GameWindow:
    def __init__(self, size: tuple):
        self.size = size

        pygame.init()
        self.background_color = (234, 212, 252)

        # create window
        self.screen = pygame.display.set_mode([self.size[0], self.size[1]])
        pygame.display.set_caption('sim')
        self.screen.fill(self.background_color)
        pygame.display.flip()

    def draw(self, obj):
        self.screen.fill(self.background_color) # clear screen
        pygame.draw.polygon(self.screen, obj.color, obj.footprint)
        pygame.display.flip()

    def get_events(self):
        return pygame.event.get()