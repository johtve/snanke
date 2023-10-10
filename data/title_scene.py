# A title scene for the title screen

import pygame
import data.config as config
import data.tools as tools
from data.snake import Snake, SnakeBlock
from pygame.locals import (
    K_ESCAPE,
    K_SPACE,
    QUIT,
)

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

        self.buttons = self.generate_buttons()

        self.title = pygame.image.load("data/assets/title.png")
        self.title = pygame.transform.scale(self.title, (config.SCREEN_WIDTH_PX*0.4, config.SCREEN_HEIGHT_PX*0.4))
    def process_input(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                for b_name in self.buttons.keys():
                    if self.buttons[b_name]["obj"].mouse_on(mouse_pos):
                        self.buttons[b_name]["func"]()

                if self.mouse_on_demo_snake(mouse_pos):
                    self.demo_snake.append_block(save_coords=False) # snake breaks if the demo snake saves coords here

            elif event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    self.switch_to_scene("MAIN_LOOP")
        # elif event.type == pygame.QUIT: # Stops if the user clicks the window close button
        #     self.terminate()

    def update(self):
        # demo snake moves with a certain interval, like a regular snake
        if round(tools.time_since(self.demo_snake.last_move), -1) > round(1000/self.demo_snake.speed):
            if self.snake_moves == config.SCREEN_WIDTH_SQ + len(self.demo_snake.sprites()*2) + 2: # makes it move all the way out of the window, then back in again regardless of length
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
        
        for b_name in self.buttons.keys():
            self.buttons[b_name]["obj"].draw(screen)
    
    def switch_to_scene(self, next_scene):
        self.next_name = next_scene

    def terminate(self):
        self.switch_to_scene(None)

    def generate_buttons(self):
        
        # this is a bit of a cursed way of doing this, but essentially i needed a way to -
        # - iterably create buttons so they're positioned below each other.
        # this allows for creating and handling the buttons in a general way without hardcoding -
        # the formatting
        
        # has to be a way to only iteratively do the positioning without having to do all this shit

        # button object is placed at [name]["obj"] by generate_buttons()
        buttons = {
            "singleplayer" : {"text" : "Singleplayer", "func" : self.sp_button_func},
            "multiplayer" : {"text" : "Multiplayer", "func" : self.lmp_button_func},
            "hs_info" : {"text" : "Health and safety information", "func": self.hsinfo_button_func}
        }

        button_width = config.SCREEN_WIDTH_PX/3
        button_height = config.SCREEN_HEIGHT_PX/15

        counter = 0
        for name in buttons.keys():
            buttons[name]["obj"] = tools.Button(buttons[name]["text"], buttons[name]["func"], x=config.SCREEN_WIDTH_PX/2-button_width/2, y=config.SCREEN_HEIGHT_PX/1.7+counter*button_height*1.5, width=button_width, height=button_height)
            counter += 1
        return buttons


    # these funcs are executed when the user clicks a given button
    # remember to change the amount of players when changing the mode. should do it differently if accomodating for more players
    def sp_button_func(self):
        self.persistent_data["mode"] = "sp"
        self.persistent_data["players"] = 1
        self.switch_to_scene("MAIN_LOOP")
    
    def lmp_button_func(self):
        self.persistent_data["mode"] = "lmp"
        self.persistent_data["players"] = 2
        self.switch_to_scene("MAIN_LOOP")
    
    def hsinfo_button_func(self):
        self.switch_to_scene("HS_INFO")

    def mouse_on_demo_snake(self, mouse_pos):
        for block in self.demo_snake:
            if block.rect.left < mouse_pos[0] < block.rect.right and block.rect.top < mouse_pos[1] < block.rect.bottom:
                return True