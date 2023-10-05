import data.tools as tools
import data.config as config
from pygame.locals import (
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

class GameOverScene():
    def __init__(self, persistent_data):
        self.name = "GAME_OVER"
        self.next_name = "GAME_OVER"
        self.persistent_data = persistent_data
        print("GAMOVERSCENE INIT RAN")

    def process_input(self, events):
        for event in events:
            if event.type == KEYDOWN and event.key == K_SPACE:
                self.switch_to_scene("MAIN_LOOP")
    
    def update(self):
        pass
    
    def render(self, screen):
        screen.fill((16.8, 154, 0))
        self.draw_game_over_text(screen, self.persistent_data)
    
    def switch_to_scene(self, next_scene):
        self.next_name = next_scene
    
    def terminate(self):
        self.switch_to_scene(None)


    # takes persistent_data dict because it needs info about what happened before this scene
    def draw_game_over_text(self, screen, persistent_data):
        #game over text is multiline, but pygame doesn't support \n.
        #render and blit iterably over each line of the text display
        lines = []
        # singleplayer
        if persistent_data["mode"] == "sp":
            lines.append(tools.big_font.render("GAME OVER", True, "BLACK"))
            lines.append(tools.big_font.render(f"YOU GOT {persistent_data['points'][0]} POINTS", True, "BLACK"))
            lines.append(tools.small_font.render("wow", True, "BLACK"))
        
        # multiplayer points win condition
        elif persistent_data["mode"] == "lmp" and persistent_data["rules"]["win"] == "points":
            # get player with the most points
            winner_number = self.pick_highest_points(persistent_data)
            
            lines.append(tools.big_font.render(f"PLAYER {winner_number} WON WITH {persistent_data['points'][winner_number]} POINTS!", True, "BLACK"))
            lines.append(tools.small_font.render("the other player got some points too: ", True, "BLACK"))
            
            # supports infinite losers
            for player_number, points in persistent_data["points"].items():
                if player_number is not winner_number:
                    lines.append(tools.small_font.render(f"Player {player_number}: {points} points", True, "BLACK"))

        # multiplayer survival win condition
        elif persistent_data["mode"] == "lmp" and persistent_data["rules"]["win"] == "survival":
            assert len(persistent_data["living_players"]) == 1 # make sure there's only one player alive
            winner_number = persistent_data["living_players"][0]
            lines.append(tools.big_font.render(f"PLAYER {winner_number} WON!", True, "BLACK"))
            lines.append(tools.small_font.render(f"AND GOT {persistent_data['points'][winner_number]} points", True, "BLACK"))

        # consider turning this into a function if you often need to display multiline text
        counter = 0
        for line in lines:
            centred_coords = tools.centre_coords(line.get_rect().width, line.get_rect().height)
            screen.blit(line, (centred_coords[0], centred_coords[1] + counter * (line.get_height() + 20)))
            counter += 1
    
    # takes persistent_data, returns the number of the player with the most points
    def pick_highest_points(self, persistent_data:dict) -> int:
        winner = 1 #works because player 1 will always be the first entry. 
        for player, points in persistent_data["points"].items():
            if points > persistent_data["points"][winner]:
                winner = player
        
        return winner
