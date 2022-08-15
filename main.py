# Credits
# music https://www.youtube.com/watch?v=5vwWFYy9UA0
import pygame, sys
from settings import Settings
from level import Level

from pygame import mixer

class JumpDead():
    def __init__(self):
            pygame.init()
            pygame.display.set_caption(Settings.title)

            self.screen = pygame.display.set_mode((Settings.window['width'], Settings.window['height']))
            self.clock = pygame.time.Clock()
            self.level = Level()
            self.volume = 0.5

            

            mixer.init()
            pygame.mixer.music.load(Settings.musicpath('music.wav'))
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(self.volume)

            font = pygame.font.SysFont(None, 40)
            click = False

            self.current_loop = "main"
            self.overlay_surface = False

    def draw_text(self, surface, text, font, x, y, color):
            textobj = font.render(text, 1, color)
            textrect = textobj.get_rect()
            textrect.topleft = (x, y)
            surface.blit(textobj, textrect)

    def run(self):
            running = True
            while running:
                if self.current_loop == "main": 
                    self.main_loop()

                elif self.current_loop == "pause":
                    self.pause_loop()

                elif self.current_loop == "settings":
                    self.settings_loop()

                elif self.current_loop == 'exit':
                    self.exit_loop()	
                self.general_keybinds()

                self.clock.tick(Settings.FPS)
                pygame.display.update()
                pygame.display.flip()

    def general_keybinds(self):
            for event in pygame.event.get():   
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.current_loop is "main":
                            self.current_loop = "pause"
                        else: 
                            self.current_loop = "main"

                    if event.key == pygame.K_KP_PLUS:            
                        pygame.mixer.music.set_volume(self.volume +0.1)
                        print(self.volume)

                    if event.key == pygame.K_KP_MINUS:
                        pygame.mixer.music.set_volume(self.volume -0.1)
                        print(self.volume)

    def pause_loop(self):
            if not self.overlay_surface:
                surface = pygame.Surface((Settings.window['width'], Settings.window['height']))
                surface.fill((0,0,0))
                surface.set_alpha(75)
                self.screen.blit(surface, (0,0))
                self.overlay_surface = True

            self.draw_text(self.screen, 'Game', pygame.font.Font(None, 40), Settings.window['width']//2, Settings.window['height']//2, (255,255,255))
            self.draw_text(self.screen, 'Pause', pygame.font.Font(None, 40), Settings.window['width']//2 - 69, Settings.window['height']//2 - 100,(255,255,255))
            
            mx, my = pygame.mouse.get_pos()
            button_1 = pygame.Rect(Settings.window['width']//2 - 100, Settings.window['height']//2 + 100, 50, 50)
            button_2 = pygame.Rect(Settings.window['width']//2 - 100, Settings.window['height']//2 + 200, 50, 50)
            button_3 = pygame.Rect(Settings.window['width']//2 - 100, Settings.window['height']//2 + 300, 50, 50)
            self.draw_text(self.screen, 'Resume', pygame.font.Font(None, 40),Settings.window['width']//2 - 10, Settings.window['height']//2 + 110  ,(255,255,255))
            self.draw_text(self.screen, 'Settings', pygame.font.Font(None, 40),Settings.window['width']//2 - 10, Settings.window['height']//2 + 210  ,(255,255,255))
            self.draw_text(self.screen, 'Exit', pygame.font.Font(None, 40),Settings.window['width']//2 - 10, Settings.window['height']//2 + 310  ,(255,255,255))

            pygame.draw.rect(self.screen, (255,0,0), button_1)
            pygame.draw.rect(self.screen, (255,0,0), button_2)
            pygame.draw.rect(self.screen, (255,0,0), button_3)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if button_1.collidepoint ((mx,my)):
                            self.current_loop = "main"

                        elif button_2.collidepoint ((mx,my)):
                            self.current_loop = "settings"

                        elif button_3.collidepoint ((mx,my)):
                            self.current_loop = "exit"


    def main_loop(self):
            self.overlay_surface = False
            self.level.run()

    def settings_loop(self):
            if not self.overlay_surface:
                surface = pygame.Surface((Settings.window['width'], Settings.window['height']))
                surface.fill((0,0,0))
                surface.set_alpha(75)
                self.screen.blit(surface, (0,0))
                self.overlay_surface = True

            self.draw_text(self.screen, 'Settings', pygame.font.Font(None, 40), Settings.window['width']//4, Settings.window['height']//4, (255,255,255))
            

            mx, my = pygame.mouse.get_pos()
            button_1 = pygame.Rect(Settings.window['width']//2 - 300, Settings.window['height']//2 + 130 + 100, 50, 50)
            button_2 = pygame.Rect(Settings.window['width']//2 - 500, Settings.window['height']//2 + 130 + 100, 50, 50)
            button_3 = pygame.Rect(Settings.window['width']//2 + 500, Settings.window['height']//2 + 300 + 100, 50, 50)
            self.draw_text(self.screen, 'Lauter', pygame.font.Font(None, 30),Settings.window['width']//2 - 200 , Settings.window['height']//2 +250  ,(255,255,255))
            self.draw_text(self.screen, 'Leiser', pygame.font.Font(None, 30),Settings.window['width']//2 - 400 , Settings.window['height']//2 +250  ,(255,255,255))
            self.draw_text(self.screen, 'Zurück', pygame.font.Font(None, 30),Settings.window['width']//2 + 400 , Settings.window['height']//2 +420  ,(255,255,255))

            pygame.draw.rect(self.screen, (255,255,255), button_1)
            pygame.draw.rect(self.screen, (255,255,255), button_2)
            pygame.draw.rect(self.screen, (255,255,255), button_3)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if button_1.collidepoint ((mx,my)):
                            self.volume +=0.1
                            pygame.mixer.music.set_volume(self.volume)
                            # if self.volume >= 1:
                            #     self.volume = 1
                                
                        if button_2.collidepoint ((mx,my)):
                            self.volume -=0.1
                            pygame.mixer.music.set_volume(self.volume)
                            # if self.volume <= 1:
                            #     self.volume = 1
                                
                        if button_3.collidepoint ((mx,my)):
                            self.current_loop = "main"



    def exit_loop(self):

            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    game = JumpDead()
    game.run()    