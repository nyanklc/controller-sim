import pygame

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
            pygame.draw.polygon(self.screen, obj.color, obj.footprint)
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