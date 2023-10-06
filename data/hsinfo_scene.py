import pygame
import data.config as config
import data.tools as tools


class HSinfoScene():
    def __init__(self, persistent_data) -> None:
        self.name = "HS_INFO"
        self.next_name = "HS_INFO"
        self.persistent_data = persistent_data


        self.text = """Snank responsibly. Snanking should only be performed in safe environments. \n Do not snank while driving or operating heavy machinery. \nDo not snank while drinking. Do not snank if pregnant.

Snanking, like any other activity, comes with side effects. \nIf you experience shortness of breath, \nheadaches, hair loss, explosive diarrhea, \ndry mouth, spontaneous disintegration, \ndandruff, swollen tongue, limb loss, sexual impotency, \nor other abnormal conditions while snanking, \nimmediately stop snanking and contact a pastor.

Remember to take a 15 minute break for every hour you snank."""

        self.text_list = self.text.split("\n")


        # yeahhh it's a list here but a dict in the title scene class.
        # it's cause buttons don't need to be iteratively placed here
        self.buttons = []
        self.buttons.append(tools.Button("Back", self.back_button_func, config.SCREEN_WIDTH_PX/20, config.SCREEN_WIDTH_PX/20, 60, 30))


    def process_input(self, events):
       for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buttons[0].mouse_on(pygame.mouse.get_pos()):
                self.back_button_func()

    
    def update(self):
        pass

    def render(self, screen):
        screen.fill((16.8, 154, 0))
        
        counter = 0
        for line in self.text_list:
            line = (tools.small_font.render(line, True, "BLACK"))
            centred_coords = tools.centre_coords(line.get_rect().width, line.get_rect().height)
            screen.blit(line, (centred_coords[0], centred_coords[1] + counter * line.get_height() + 10))
            counter += 1

        for button in self.buttons:
            button.draw(screen)

    def switch_to_scene(self, next_scene):
        self.next_name = next_scene

    def terminate(self):
        self.switch_to_scene(None)

    def back_button_func(self):
        self.switch_to_scene("TITLE")