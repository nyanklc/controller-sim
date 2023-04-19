import pygame
import math

from object import Object

class GameWindow:
    def __init__(self, size: tuple):
        self.size = size

        pygame.init()
        self.background_color = (234, 212, 252)

        self.font = pygame.font.SysFont(None, 24)
        self.info_text_surface: None

        # create window
        self.screen = pygame.display.set_mode([self.size[0], self.size[1]])
        pygame.display.set_caption('sim')
        self.screen.fill(self.background_color)
        pygame.display.flip()

    def draw(self, obj_list, info_text: bool = True):
        self.screen.fill(self.background_color) # clear screen
        for obj in obj_list:
            # draw footprint of the object
            pygame.draw.polygon(self.screen, obj.color, obj.footprint)
            # indicate orientation
            if obj.has_orientation == True:
                offsetted_center = (obj.x + math.cos(obj.yaw) * obj.radius / 3, obj.y + math.sin(obj.yaw) * obj.radius / 3)
                pygame.draw.circle(self.screen, invert_color(obj.color), offsetted_center, obj.radius / 5)
        if info_text:
            self.screen.blit(self.info_text_surface, (0, 0))
        pygame.display.flip()

    def get_events(self):
        return pygame.event.get()

    def set_info_text(self, s: str, color: tuple):
        self.info_text_surface = self.font.render(s, True, color)

    def quit(self):
        pygame.display.quit()
        pygame.quit()

def invert_color(color):
    return (255 - color[0], 255 - color[1], 255 - color[2])