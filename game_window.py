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

    def draw(self, obj_list, path, info_text: bool = False):
        self.screen.fill(self.background_color) # clear screen
        self.draw_path(path)
        for obj in obj_list:
            # draw footprint of the object
            pygame.draw.polygon(self.screen, obj.color, obj.footprint)
            # draw goal radius if master
            if obj.goal_radius is not 0:
                pygame.draw.circle(self.screen, (255-obj.color[0], 255-obj.color[1], 255-obj.color[2]), (obj.x, obj.y), obj.goal_radius, width=3)
                # also draw goal point on path
                pygame.draw.circle(self.screen, (255-obj.color[0], 255-obj.color[1], 255-obj.color[2]), (path[obj.goal_index][0], path[obj.goal_index][1]), 8)
            # indicate orientation
            if obj.has_orientation == True:
                offsetted_center = (obj.x + math.cos(obj.yaw) * obj.radius / 3, obj.y + math.sin(obj.yaw) * obj.radius / 3)
                pygame.draw.circle(self.screen, invert_color(obj.color), offsetted_center, obj.radius / 5)
        if info_text:
            self.screen.blit(self.info_text_surface, (0, 0))
        pygame.display.flip()

    def draw_path(self, path):
        for i in range(len(path) - 1):
            pygame.draw.circle(self.screen, (0, 0, 255), (path[i][0], path[i][1]), 4)
            pygame.draw.line(self.screen, (255, 0, 0), path[i], path[i+1], 3)

    def get_events(self):
        return pygame.event.get()

    def set_info_text(self, s: str, color: tuple):
        self.info_text_surface = self.font.render(s, True, color)

    def quit(self):
        pygame.display.quit()
        pygame.quit()

def invert_color(color):
    return (255 - color[0], 255 - color[1], 255 - color[2])
