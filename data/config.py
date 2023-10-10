#only consts in this file

DEBUG = False

#these are given in number of grid squares
SCREEN_WIDTH_SQ = 15
SCREEN_HEIGHT_SQ = 10

GRID_SQUARE_SIZE = (60, 60) #size of each square of the grid

# screen size in pixels
SCREEN_WIDTH_PX = SCREEN_WIDTH_SQ * GRID_SQUARE_SIZE[0]
SCREEN_HEIGHT_PX = SCREEN_HEIGHT_SQ * GRID_SQUARE_SIZE[1]

BACKGROUND_COLOUR = ()

DEFAULT_SNAKE_SPEED = 5 #grid squares per second. 6.67 = 150 ms between each step

STARTING_BLOCKS_AMOUNT = 3 #How many blocks in the snake the player starts with
STARTING_FOOD_AMOUNT = 7

# snake colours are currently assigned iteratively, NOT randomly.
# this means player 1 is always colour 0, 2 is colour 1, etc.
# in the future this should be changed to generate a random colour for each player in multiplayer when the game is booted,
# and keeping that colour until the game is closed
# storing a persistent colour required a major restructuring of the way persistent data is saved,
# which proved to be, as we call it in the industry, a bitch
# but it might still be implemented in the future

SNAKE_COLOURS =  [
    (16.8, 79, 0), # dark green (default)
    (20, 49, 92), # dark blue
    (166, 225, 19) # yellow
]



# base for the dict that stores data from the scenes past scene changes
# this is only to be edited manually in the main file
#mode is either "sp" (singleplayer), "lmp" (local multiplayer), or in the future (hopefully) "omp" (online multiplayer)
persistent_data = {
"mode" : str,
"players" : int,
"living_players" : [], #player number of all living players
"points" : {int:int},
"rules" : {
    "timer" : int,
    "win" : str, # "survival" or "points"
}

}