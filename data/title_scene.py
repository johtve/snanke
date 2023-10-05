# A title scene for the title screen

import pygame
import data.config as config
import data.tools as tools
from data.snake import Snake

class TitleScene():
    def __init__(self, persistent_data) -> None:
        self.name = "TITLE"
        self.next_name = "TITLE"
        self.persistent_data = persistent_data
        
        self.demo_snake = Snake(1, None, -config.SCREEN_WIDTH_PX*0.4, config.SCREEN_HEIGHT_PX * 0.6) # demo snake that moves back and forth horizontally on the title screen
        self.demo_snake.speed = 10
        self.snake_moves = 0 #used to count how far the demo snake goes so it can be turned around
        for block in self.demo_snake:
            block.direction == self.demo_snake.head_direction

        self.buttons = []
        self.title = pygame.image.load("data/assets/title.png")
        self.title = pygame.transform.scale(self.title, (config.SCREEN_WIDTH_PX*0.4, config.SCREEN_HEIGHT_PX*0.4))
    def process_input(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.switch_to_scene("MAIN_LOOP")
        # elif event.type == pygame.QUIT: # Stops if the user clicks the window close button
        #     self.terminate()
    
    def update(self):
        # demo snake moves with a certain interval, like a regular snake
        if round(tools.time_since(self.demo_snake.last_move), -1) > round(1000/self.demo_snake.speed):
            if self.snake_moves == 25:
                # turn the demo snake around if it's gone far enough
                if self.demo_snake.head_direction == "right":
                    self.demo_snake.head_direction = "left"
                elif self.demo_snake.head_direction == "left":
                    self.demo_snake.head_direction = "right"
                self.snake_moves = 0
            self.demo_snake.move()
            self.demo_snake.attempt_save_direction_change()
            self.demo_snake.update_tail_directions()
            self.snake_moves += 1


    def render(self, screen):
        screen.fill((16.8, 154, 0))
        
        title_centred_coords = tools.centre_coords(self.title.get_width(), self.title.get_height())
        title_rect = pygame.Rect(title_centred_coords[0], title_centred_coords[1] - config.SCREEN_HEIGHT_PX*0.2, self.title.get_width(), self.title.get_height())
        screen.blit(self.title, title_rect)

        self.demo_snake.draw_all(screen)
    
    def switch_to_scene(self, next_scene):
        self.next_name = next_scene


    def terminate(self):
        self.switch_to_scene(None)



class TitleButtons():
    def __init__(self) -> None:
        pass
