import pygame, random
import data.config as config

#Sprite group for all food on the screen
class Food(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    #generates a given amount of food
    #takes amount of food to generate, and a snake object in order to make sure food doesn't spawn on a snake
    def generate_food(self, amount, snake_list, pos="random"):
        #this is a messy way of making sure food isn't spawned on top of an existing snakeblock
        #cut me some slack, it's been a long day
        for i in range(amount):
            while True:
                self.add(FoodBlock(pos))
                #v if the newly added sprite is in collision with any of the snake blocks v
                if self.food_on_snake(self.sprites()[-1], snake_list):
                    self.sprites()[-1].kill()
                    continue #redo the generation of this food piece
                else:
                    break #move on to generation of next food piece

    #Returns true if the given food block collides with any snake blocks
    def food_on_snake(self, foodblock, snake_list):
        for snake in snake_list:
            if len(pygame.sprite.spritecollide(foodblock, snake, False)) > 0:
                return True
        return False
        
    #deletes all food and generates new
    def reset(self, snake):
        for food_piece in self.sprites():
            food_piece.kill()
        self.generate_food(config.STARTING_FOOD_AMOUNT, snake)


##############################################################


#Class for each piece of snake food
#New instances need to be generated through game.generate_food() so that
#food isn't generated on top of the snake
class FoodBlock(pygame.sprite.Sprite):
    def __init__(self, pos): #pos can be string "random" or tuplet (x, y) 
        super().__init__()
        
        if pos == "random":
            #place the food randomly
            while True:
                #calcs "snap the food to the grid"
                random_x = random.randint(0, config.SCREEN_WIDTH_PX)
                random_y = random.randint(0, config.SCREEN_HEIGHT_PX)

                self.x = random_x - (random_x % config.GRID_SQUARE_SIZE[0])
                self.y = random_y - (random_y % config.GRID_SQUARE_SIZE[1])
                break
        else:
            self.x = pos[0]
            self.y = pos[1]

        self.rect = pygame.Rect(self.x, self.y, config.GRID_SQUARE_SIZE[0], config.GRID_SQUARE_SIZE[1])
        self.image = pygame.image.load("./data/assets/food_1.jpg")
        self.image = pygame.transform.scale(self.image, config.GRID_SQUARE_SIZE)
    
    #Used when generating food so it doesn't spawn on the snake or on other food
    #Get a random position until it finds one that doesn't match any food or snake blocks
    #There's some odd logic here that makes this difficult to implement. Look into it later
    def random_position():
        x = 0
        y = 0
        
        #calcs "snap the food to the grid"
        random_x = random.randint(0, config.SCREEN_WIDTH_PX)
        random_y = random.randint(0, config.SCREEN_HEIGHT_PX)

        x = random_x - (random_x % config.GRID_SQUARE_SIZE[0])
        y = random_y - (random_y % config.GRID_SQUARE_SIZE[1])           

    def draw(self, screen):
        screen.blit(self.image, self.rect)