# Main loop variation for multiple players
# might actually be better to merge this with the singleplayer scene -
# - and just separate the functionality via if statements

import pygame
import data.tools as tools
import data.config as config
from data.snake import Snake
from data.food import Food

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

class MainLoopScene():
    def __init__(self, persistent_data: dict):
        super().__init__()
        self.name = "MAIN_LOOP"
        self.next_name = "MAIN_LOOP"

        self.all_snakes = []
        self.game_started = False
        
        # persistent data stuff. remember that this is carried over to future scenes
        self.players = persistent_data["players"]
        self.persistent_data = persistent_data
        self.persistent_data["points"] = {} # little reset
        self.persistent_data["living_players"] = [snake.number for snake in self.all_snakes]

        self.last_sync = pygame.time.get_ticks()

        # generates appropriate number of snakes
        input_modes = ["arrows", "wasd"]
        snake_start_directions = ["right", "left"]
        for i in range(self.players):
            x_offset = i * config.GRID_SQUARE_SIZE[0] * config.STARTING_BLOCKS_AMOUNT
            y_offset = i * 2 * config.GRID_SQUARE_SIZE[1] # snakes are generated with a space of 1 grid square
            if self.persistent_data["mode"] == "lmp":
                self.all_snakes.append(Snake(i+1, input_modes[i], config.SCREEN_WIDTH_PX/2-x_offset, config.SCREEN_HEIGHT_PX/2-y_offset, snake_start_directions[i%2], colour=config.SNAKE_COLOURS[i])) # i+1 is to get the numbering right. first snake is snake 1
            elif self.persistent_data["mode"] == "sp":
                self.all_snakes.append(Snake(1, input_modes[0], config.SCREEN_WIDTH_PX/2-x_offset, config.SCREEN_HEIGHT_PX/2-y_offset, snake_start_directions[0])) # i+1 is to get the numbering right. first snake is snake 1
        
        self.food = Food()
        self.food.generate_food(config.STARTING_FOOD_AMOUNT, self.all_snakes)


    def process_input(self, events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # outside of recieve_input() because it's not related to snakes
                     self.terminate()
                elif event.key == K_SPACE: # space starts the game
                    if self.game_started == False:
                        self.game_started = True
                else:
                    if self.game_started == False: #don't take any movement input before the game starts
                        return
                    for snake in self.all_snakes:
                            snake.recieve_input(event.key)
            
            elif event.type == pygame.QUIT: # Stops if the user clicks the window close button
                self.terminate()

    def update(self):
        if self.game_started == False: # snakes should stand still before any buttons have been pressed
            return
        
        self.sync_snakes()

        for snake in self.all_snakes:
            # waits for the second expression's number of milliseconds between each time it executes this block
            print(f"DIFFERENCE: {self.all_snakes[0].last_move-self.all_snakes[1].last_move}")
            if round(tools.time_since(snake.last_move), -1) > round(1000/snake.speed):

                # this if/elif block sets depends on game rules, and mainly handles win conditions
                if self.persistent_data["mode"] == "sp":
                    if snake.collides(self.all_snakes):
                        self.persistent_data["points"] = {snake.number:snake.points for snake in self.all_snakes} #puts all the snake points into a list for passing on to next scene
                        self.all_snakes.remove(snake)
                        self.switch_to_scene("GAME_OVER")
                elif self.persistent_data["mode"] == "lmp" or "omp":
                    if "survival" in self.persistent_data["rules"]["win"]:
                        if snake.collides(self.all_snakes):
                            self.all_snakes.remove(snake)
                        if len(self.all_snakes) == 1: # if only one player remains, end the game
                            self.persistent_data["points"] = {snake.number:snake.points for snake in self.all_snakes} #puts all the snake points into a list for passing on to next scene
                            self.persistent_data["living_players"] = [snake.number for snake in self.all_snakes]
                            print(self.persistent_data["living_players"])
                            self.switch_to_scene("GAME_OVER")

                    print(len(self.all_snakes))

                else:
                    print("Invalid game mode/rules")
                    raise ValueError

                
                
                
                
                snake.move()
                snake.attempt_save_direction_change()
                if snake.attempt_consumption(self.food) == True: # generates 1 new food if one has been consumed
                    self.food.generate_food(1, self.all_snakes) # argument 2 is snake list to ensure no food spawns on any snake
                snake.update_tail_directions()

    def render(self, screen):
        screen.fill((16.8, 154, 0))
        self.food.draw(screen) #Food is drawn before snake blocks so it doesn't cover the snake
        points = {}
        for snake in self.all_snakes:
            snake.draw_all(screen)
            if self.persistent_data["mode"] == "lmp" or "omp": # draws a tag on the snake if multiplayer
                snake.draw_tag(screen)
            points[snake.number] = snake.points
        tools.draw_point_display(screen, points)
        if self.game_started == False:
            tools.draw_game_start_text(screen)
    
    def switch_to_scene(self, next_scene):
        self.next_name = next_scene

    def terminate(self):
        self.switch_to_scene(None)

    # if all snakes have the same speed, return their speed. else return false
    def snakes_same_speed(self):
        base_speed = self.all_snakes[0].speed
        for snake in self.all_snakes:
            if snake.speed != base_speed:
                return False
        return base_speed

    # snakes get out of sync over time due to things like varying food consumption causing different calc times for each snake
    # this func syncs all snakes if they have the same speed (done every interval)
    # if they don't have the same speed, no one expects them to move in sync
    def sync_snakes(self):
        interval = 7 # how many snake motion steps should pass between each sync

        if self.snakes_same_speed() != False:
            for snake in self.all_snakes:
                if tools.time_since(self.last_sync) > round(1000/snake.speed)*interval:
                    snake.last_move = 0
            print("SNAKES SYNCED")
            self.last_sync = pygame.time.get_ticks()