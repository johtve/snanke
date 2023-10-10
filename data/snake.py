#contains Snake class as well as SnakeBlock class for each of the snake's constituent blocks


#import Food class here when it has been moved into its own file
import pygame
from .food import Food
import data.config as config
import data.tools as tools
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_a,
    K_s,
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

class Snake(pygame.sprite.Group):
    def __init__(self, number:int, input_mode:str, start_x=config.SCREEN_WIDTH_PX/2, start_y=config.SCREEN_HEIGHT_PX/2, start_direction="right", colour=config.SNAKE_COLOURS[0]):
        super().__init__()
        self.number = number #this snake's numbering
        self.start_x = start_x
        self.start_y = start_y
        self.input_mode = input_mode #"arrows" or "wasd" currently
        self.colour = colour
        self.speed = config.DEFAULT_SNAKE_SPEED
        self.last_move = pygame.time.get_ticks() #used to count out when to move the snake one step
        self.points = 0
        self.head_direction = start_direction
        self.direction_change_coords = {} #Format: {(x, y):"direction"}
        self.generate_starting_blocks()

        head_sprite_image = pygame.image.load("data/assets/snake_head.png")
        self.head_sprite = pygame.transform.scale(head_sprite_image, (SnakeBlock.DEFAULT_BLOCK_SIZE))       

    #Before the game is started, all snake blocks are in the neutral position. When the user presses a button, only the first block
    #will have its direction changed. This function will only be ran when the "tail" blocks are neutral in order to give them a starting direction
    def tail_startup(self, direction):
        for block in self.sprites():
            block.direction = direction
    
    #Changes direction of the snake head based on user key input
    def recieve_input(self, key):
        # print(f"Key pressed: {key}")

        if self.input_mode == "arrows":
            if self.trying_to_go_back(key):
                # print(f"SNAKE {self.number} TRIED TO GO BACK ON ITSELF")
                pass
            elif key == K_RIGHT:
                # print("Right key pressed")
                if self.sprites()[0].direction != "right":
                    self.head_direction = "right"
            elif key == K_LEFT:
                if self.sprites()[0].direction != "left":
                    self.head_direction = "left"
            elif key == K_UP:
                if self.sprites()[0].direction != "up":
                    self.head_direction = "up"
            elif key == K_DOWN:
                if self.sprites()[0].direction != "down":
                    self.head_direction = "down"
        elif self.input_mode == "wasd":
            if self.trying_to_go_back(key):
                # print(f"SNAKE {self.number} TRIED TO GO BACK ON ITSELF")
                pass
            elif key == K_d:
                if self.sprites()[0].direction != "right":
                    self.head_direction = "right"
            elif key == K_a:
                if self.sprites()[0].direction != "left":
                    self.head_direction = "left"
            elif key == K_w:
                if self.sprites()[0].direction != "up":
                    self.head_direction = "up"
            elif key == K_s:
                if self.sprites()[0].direction != "down":
                    self.head_direction = "down"
        
        elif self.input_mode == None: # safety net to prevent motion of the demo snake
            pass

        #gives tail starting direction
        if self.sprites()[-1].direction == "neutral":
            self.tail_startup(self.start_direction)

    #moves all snakeblocks one step
    def move(self):
        for block in self.sprites():
            if block.direction == "neutral":
                return
            elif block.direction == "right":
                block.x += config.GRID_SQUARE_SIZE[0]
            elif block.direction == "left":
                block.x -= config.GRID_SQUARE_SIZE[0]
            elif block.direction == "up":
                block.y -= config.GRID_SQUARE_SIZE[1]
            elif block.direction == "down":
                block.y += config.GRID_SQUARE_SIZE[1]

            #the snake is drawn via pygame.sprite.Group.draw(), which uses the sprite rect for size and pos
            #meaning the rect needs to be updated after making changes to the block
            block.update_rect(block.x, block.y, block.size)
            self.last_move = pygame.time.get_ticks()
    
    #Returns true if the snake head is touching the border, otherwise false
    def collides_with_border(self):
        snake_head = self.sprites()[0].rect
        if snake_head.left < 0 or snake_head.left > config.SCREEN_WIDTH_PX - SnakeBlock.DEFAULT_BLOCK_SIZE[0]:
            return True
        elif snake_head.top < 0 or snake_head.top > config.SCREEN_HEIGHT_PX - SnakeBlock.DEFAULT_BLOCK_SIZE[1]:
            return True
        else:
            return False
    
    #Returns true if the snake head touches other snakeblocks
    def collides_with_self(self):
        snake_head = self.sprites()[0]
        if snake_head.rect.collidelist(self.sprites()[1::]) != -1:
            return True
        else:
            return False
    
    # Returns true if the snake head touches a snake block belonging to another snake
    def collides_with_other(self, snake_list):
        own_head = self.sprites()[0]
        for snake in snake_list:
            if snake != self: # only check collision with other snakes
                if own_head.rect.collidelist(snake.sprites()[1::]) != -1: # check collision between own head and any block in other snakes
                    print(f"Snake {self.number} collided with {snake.number} snake!")
                    return True
                else:
                    return False

    #returns True if the snake has collided with itself or the border
    def collides(self, snake_list):
        if self.collides_with_self():
            print(f"SNAKE {self.number} COLLIDED WITH ITSELF")
            return True
        elif self.collides_with_border():
            print(f"SNAKE {self.number} COLLIDED WITH BORDER")
            return True
        elif self.collides_with_other(snake_list): # fix and implement. currently just deletes the snakes
            return True
        else:
            return False
    

    # add a snakeblock at the end of the snake
    def append_block(self, save_coords=True):
        #this big ol' if block positions the new block relative to the last block of the snake so that the new one takes the old one's position the next frame
        if self.sprites()[-1].direction == "right":
            new_block_direction = "right"
            new_block_x = self.sprites()[-1].x - SnakeBlock.DEFAULT_BLOCK_SIZE[0]
            new_block_y = self.sprites()[-1].y
        elif self.sprites()[-1].direction == "left":
            new_block_direction = "left"
            new_block_x = self.sprites()[-1].x + SnakeBlock.DEFAULT_BLOCK_SIZE[0]
            new_block_y = self.sprites()[-1].y
        elif self.sprites()[-1].direction == "up":
            new_block_direction = "up"
            new_block_x = self.sprites()[-1].x
            new_block_y = self.sprites()[-1].y + SnakeBlock.DEFAULT_BLOCK_SIZE[1]
        elif self.sprites()[-1].direction == "down":
            new_block_direction = "down"
            new_block_x = self.sprites()[-1].x
            new_block_y = self.sprites()[-1].y - SnakeBlock.DEFAULT_BLOCK_SIZE[1]


        # print(self.snake.sprites()[-1].direction)
        # print(new_block_direction, new_block_x, new_block_y)

        self.add(SnakeBlock(snake=self, x=new_block_x, y=new_block_y, direction=new_block_direction, colour=self.colour))
        if save_coords == True: # prevents the title screen demo snake breaking, but need to be True for normal gameplay
            self.direction_change_coords[(self.sprites()[-1].x, self.sprites()[-1].y)] = self.sprites()[-1].direction
        #^ if the snake breaks, try switching the snakeblock generation line and the direction_change_coords line

    def kill(self):
        for block in self.sprites():
            block.kill()
    
    #Generates the starting blocks
    #pos is determined with the enumerator so the starting blocks are placed next to each other
    def generate_starting_blocks(self):
        # generates blocks from right to left or left to right depending on starting direction
        # generation always starts from head
        if self.head_direction == "right":
            direction_modifier = 1
        elif self.head_direction == "left":
            direction_modifier = -1
        for i in range(config.STARTING_BLOCKS_AMOUNT):
            #GRID_SQUARE_SIZE[0]/2 is there to adjust the snake to align with the grid
            new_block = SnakeBlock(snake=self, x=self.start_x-i*SnakeBlock.DEFAULT_BLOCK_SIZE[0]*direction_modifier + config.GRID_SQUARE_SIZE[0]/2, y=self.start_y, colour=self.colour)
            self.add(new_block)
            self.sprites().append(new_block)
    

    #When the user changes the direction of the snake, the coords of the first snakeblock are saved
    #When subsequent snakeblocks pass through those coords, they have their direction changed to what the user has entered.

    #Changes the direction of all blocks that move into coords where the user has changed directions
    #rewrite this whole thing. will not work
    def update_tail_directions(self):
        coords_for_deletion = set() #done via temp local var to not change self.sprites() during iteration

        for block in self.sprites():
            for coords in self.direction_change_coords.keys():
                #v if the given block is on the direction change coord and doesn't match its direction, set it to the coord's direction
                if block.x == coords[0] and block.y == coords[1]:
                    if block.direction != self.direction_change_coords[coords]:
                        block.direction = self.direction_change_coords[coords]

                #Remove coords from direction_change_coords when the last block passes through them
            if block == self.sprites()[-1]:
                for coords in self.direction_change_coords.keys():
                    if coords == (block.x, block.y):
                        coords_for_deletion.add(coords)
            #Try-except for coord deletion in case there is no coord to delete
        try:
            for coords in coords_for_deletion:
                del self.direction_change_coords[coords]
                print(f"{coords} removed from direction-changing dict")
        except:
            pass
    

    #Saves the current coords of the snake head when the user changes direction
    #Since the first input will always change the snake head's direction, this is always triggered on first movement input
    def attempt_save_direction_change(self):
        if self.sprites()[0].direction != self.head_direction:
            self.sprites()[0].direction = self.head_direction
            self.direction_change_coords[(self.sprites()[0].x, self.sprites()[0].y)] = self.head_direction
            print(f"New direction change saved at {self.sprites()[0].x, self.sprites()[0].y} ({self.head_direction})")

    # returns True if the user is trying to move the snake back on itself
    # takes input key
    def trying_to_go_back(self, key): # change this to work for WASD as well
        #might wanna make a dict for handlings things like this
        if (
            (self.head_direction == "up" and (key == K_DOWN or key == K_s)) or
            (self.head_direction == "down" and (key == K_UP or  key == K_w)) or
            (self.head_direction == "left" and (key == K_RIGHT or  key == K_d)) or
            (self.head_direction in ("right", "neutral") and (key == K_LEFT or key == K_a)) # change this so it support snakes starting in different directions
        ):
            return True
        else: 
            return False

    #Ran every frame to see if the snake is touching any food. If so, consumes it and becomes 1 block longer
    #Returns True if food is consumed
    def attempt_consumption(self, food_group):
        food_list = food_group.sprites()

        for food_block in food_list:
            if pygame.sprite.spritecollide(food_block, self, False):
                self.append_block()
                self.points += 1
                food_block.kill() #remove from all groups
                return True
    
    # draws a little tag above the snake's head that indicates its number
    def draw_tag(self, screen):
        head_x = self.sprites()[0].x
        head_y = self.sprites()[0].y

        player_number = tools.small_font.render(f"P{self.number}", True, "BLACK")
        arrow = tools.small_font.render("  \u25BC", True, "BLACK")
        screen.blit(player_number, (head_x + SnakeBlock.DEFAULT_BLOCK_SIZE[0]/3, head_y - config.SCREEN_HEIGHT_PX/20))
        #screen.blit(arrow, (head_x, head_y - config.SCREEN_HEIGHT_PX/35))
    
    # clears all snakeblocks, then generates new ones just like the beginning of the game
    def reset(self):
        for block in self.sprites():
            block.kill()
        self.direction_change_coords = {}
        self.head_direction = "neutral" #redundant? blocks are set to neutral on generation
        self.generate_starting_blocks()

    #draws the snake body AND the sprite for the head
    def draw_all(self, screen):
        if not config.DEBUG:
            # self.draw(screen)
            for block in self.sprites():
                pygame.draw.rect(screen, block.colour, block.rect)
        else:
            #draws an unfilled rectangle instead of the full sprite, if debug is enabled
            for block in self.sprites():
                pygame.draw.rect(screen, block.colour, block.rect, (1))



        #Draws an image on the snake head
        #Image has to point up by default
        if self.sprites()[0].direction == "right" or self.head_direction == "neutral": #snake points right when starting
            head_rotated = pygame.transform.rotate(self.head_sprite, 270)
        elif self.sprites()[0].direction == "left":
            head_rotated = pygame.transform.rotate(self.head_sprite, 90)
        elif self.sprites()[0].direction == "up":
            head_rotated = pygame.transform.rotate(self.head_sprite, 0)
        elif self.sprites()[0].direction == "down":
            head_rotated = pygame.transform.rotate(self.head_sprite, 180)

        screen.blit(head_rotated, self.sprites()[0].rect)
        if config.DEBUG == True:
            #Writes the blocks' numbers onto them
            for block in self.sprites():
                screen.blit(block.label_number, (block.x + SnakeBlock.DEFAULT_BLOCK_SIZE[0]/2, block.y + SnakeBlock.DEFAULT_BLOCK_SIZE[1]/2))



#################################################################################



#Class for each segment ("block") of the snake
class SnakeBlock(pygame.sprite.Sprite):
    #these two class attributes are more logical here than in Snake
    q = 0 #The number of blocks in the snake. += 1 upon object generation
    DEFAULT_BLOCK_SIZE = config.GRID_SQUARE_SIZE #Defined here so it can be used in calculations outside the objects/class

    # i want the parent snake direction to be the default for new blocks (on initial generation in particular). direction can still be given in case of appending blocks when food is eaten
    def __init__(self, snake, x=config.SCREEN_WIDTH_PX/2, y=config.SCREEN_HEIGHT_PX/2, colour=(16.8, 79, 0), size=DEFAULT_BLOCK_SIZE, direction=None):
        super().__init__() #important to call this when deriving from another class. runs parent init
        #x and y coords of the block
        self.x = x
        self.y = y
        self.snake = snake
        self.colour = colour
        #print(self.colour)
        self.size = size
        SnakeBlock.q += 1
        self.q = SnakeBlock.q #Numbering of the SnakeBlocks object
        if direction == None:
            self.direction = self.snake.head_direction #Blocks can be moved in four directions, default state is matching parent snake's head direction
        else:
            self.direction = direction

        #for the future: change v this v line to use a func from fonts.py so fonts can be reused easily
        self.label_number =  pygame.font.SysFont(None, 30).render(str(self.q), True, "GREEN") #Surface object containing the number of the snake block

        self.rect = pygame.Rect((self.x, self.y), self.size) #updated every time the block is drawn
        self.image = pygame.image.load("data/assets/snake_block.png")
        self.image = pygame.transform.scale(self.image, config.GRID_SQUARE_SIZE)

    #updates the rect attr of the snake block using the given x, y, and size values
    #could be changed to only have optional vars, but it's a hassle implementing the defaut values
    def update_rect(self, x, y, size):
        self.rect = pygame.Rect((x, y), size)