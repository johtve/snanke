#contains some useful tools for calcs and drawing. independent.
#could be a class, but that would be pointless imo

import data.config as config
import pygame

pygame.font.init()

small_font = pygame.font.Font("data/assets/bahnschrift.ttf", 20) #Font object used for drawing various text
big_font = pygame.font.Font("data/assets/bahnschrift.ttf", 35)


#lets you centre something on the screen based on its size
#returns the coords where the upper left corner is to be placed
def centre_coords(width, height):
    x = config.SCREEN_WIDTH_PX/2 - width/2
    y = config.SCREEN_HEIGHT_PX/2 - height/2

    return (x, y)

#returns the ms passed since given time
def time_since(time):
    return pygame.time.get_ticks() - time

# draws the point display in the corner while the main loop is running. support for infinite players
def draw_point_display(screen, points_dict:dict):
        counter = 0
        for player, points in points_dict.items():
            point_display = small_font.render(f"Player {player}: {points}", True, "BLACK")
            screen.blit(point_display, (0, (config.SCREEN_HEIGHT_PX/20)*counter))
            counter += 1

# draws the words "press space to start" on the screen when the main loop is started and the game hasn't begun yet
def draw_game_start_text(screen):
    text = big_font.render(f"PRESS SPACE TO START", True, "BLACK")
    centred_coords = centre_coords(text.get_rect().width, text.get_rect().height)
    screen.blit(text, (centred_coords[0], centred_coords[1]))


class Button(pygame.rect.Rect):
    def __init__(self, text: str, func, x, y, width=200, height=100, colour="grey") -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.colour = colour
        self.func = func
        self.border_colour = "BLACK"
        
        self.border_rect = (pygame.rect.Rect(self.x, self.y, self.width, self.height))
    
    def draw(self, screen):
        text_render = small_font.render(self.text, True, "BLACK")
        text_x = self.x + (self.width - text_render.get_width())/2
        text_y = self.y + (self.height - text_render.get_height())/2

        pygame.draw.rect(screen, self.colour, self)
        pygame.draw.rect(screen, self.border_colour, self.border_rect, (1))
        screen.blit(text_render, (text_x, text_y))

    def mouse_on(self, mouse_pos):
        if self.left < mouse_pos[0] < self.right and self.top < mouse_pos[1] < self.bottom:
            return True
        else:
            return False
        

