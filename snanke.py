#Project started 28.8.2023

import data.config as config
from data.main_loop_scene import MainLoopScene
from data.game_over_scene import GameOverScene
from data.title_scene import TitleScene
from data.hsinfo_scene import HSinfoScene
import pygame
from time import sleep
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

#######DEFINITIONS#######

# mainly be global to avoid scenes trying to access data that aren't set until the main menu is implemented
# can probably be made into local within run_game() when that's implemented
persistent_data = config.persistent_data # dict of data that is transferred between scenes

# PLACEHOLDERS - DATA WILL ACTUALLY BE SET VIA MAIN MENU
persistent_data["players"] = 2
persistent_data["mode"] = "lmp"
persistent_data["rules"]["win"] = "survival"

#######MAIN GAME FUNCTION#####
def run_game(width, height, starting_scene):
    pygame.init()
    screen = pygame.display.set_mode((width, height))

    #Using the actual classes to switch scenes within each scene class -
    # - quickly results in a lot of circular imports. Instead, all scene switching within -
    # - the scene classes is done via strings. They are then converted to classes in this file

    scene_dict =  {
        "MAIN_LOOP" : MainLoopScene,
        "GAME_OVER" : GameOverScene, 
        "TITLE" : TitleScene,
        "HS_INFO" : HSinfoScene
        }

    active_scene = starting_scene

    while active_scene != None:

        #code for things like ESCAPE quitting should be in this file, not in every scene
        #if the events aren't filtered after the quit check, the active scene will waste time -
        # - trying to process the quiwtting event
        filtered_events = []

        for event in pygame.event.get():
            if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == pygame.QUIT:
                active_scene.terminate()
            else:
                filtered_events.append(event)

        active_scene.process_input(filtered_events)
        active_scene.update()
        active_scene.render(screen)

        #if a new scene is set, set the active scene to a new object of the new scene class
        if active_scene.next_name != active_scene.name:
            active_scene = scene_dict[active_scene.next_name](active_scene.persistent_data)

        

        pygame.display.flip()



run_game(config.SCREEN_WIDTH_PX, config.SCREEN_HEIGHT_PX, TitleScene(config.persistent_data))