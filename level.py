
import pygame
from settings import Settings
vec = pygame.math.Vector2

class Level():
    def __init__(self):
        
        self.jumping = False
        self.velocity_index = 1
        self.velocity = ([-10,-9.5,-9,-8.5,-8,-7.5, -7, -6.5, -6, -5.5, -5, -4.5, -4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0,
                             0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10])
        self.tile_rect = []
        self.display_dimension = (3842,3970)
        self.window_size = (Settings.window['width'],Settings.window['height'])
        # self.test_surface = pygame.Surface((3842,50))
        # self.test_rect = pygame.Rect((0,0),(3842,50))
        self.screen = pygame.display.set_mode(self.window_size)
        self.display = pygame.Surface((self.display_dimension)) 
        self.player_location= (Settings.window['width'] /2, Settings.window['height']/2)
        self.wood_image = pygame.image.load(Settings.imagepath('Oak_topView.png'))
        self.border_image = pygame.image.load(Settings.imagepath('wood_block.png'))
        self.background = pygame.image.load(Settings.imagepath('background.png'))
        self.wood_image = pygame.transform.scale(self.wood_image, Settings.player_size)
        self.border_image = pygame.transform.scale(self.border_image, Settings.player_size)
        self.tile_size = self.wood_image.get_width()
        self.player_image = pygame.image.load(Settings.imagepath('player.png')).convert_alpha()
        self.player_image = pygame.transform.scale(self.player_image, Settings.player_size)
        self.player_rect = self.player_image.get_rect(center = (1800,3800))
        self.finish_image = pygame.image.load(Settings.imagepath('finish.png')).convert_alpha()
        self.finish_image = pygame.transform.scale(self.finish_image, Settings.player_size)
        self.finish_rect = self.finish_image.get_rect(center = (1800,190))
        self.uWon_image = pygame.image.load(Settings.imagepath('u won.png'))
        self.uWon_image = pygame.transform.scale(self.uWon_image, (1800,1800))
        self.rect = self.player_rect
        self.moving_right = False
        self.moving_left = False
        self.player_falling = 1
        self.player_y_momentum = 0.1
        self.air_timer = 0
        self.maploading = {'Map1': True, 'Map2': False}
        #self.map()
        


    def map(self):
        y = 0
        for row in Settings.WORLDMAP:
            x = 0
            for tile in row :
                if tile =='1':
                    self.display.blit(self.border_image,(x*self.tile_size, y*self.tile_size))
                if tile == '2':
                    self.display.blit(self.wood_image,(x*self.tile_size, y*self.tile_size)) 
                if tile != '0':
                    self.tile_rect.append(pygame.Rect(x *self.tile_size, y*self.tile_size, self.tile_size ,self.tile_size))
                x +=1
            y+=1 
    def map2(self): 
            y = 0
            for row in Settings.WORLDMAP2:
                x = 0
                for tile in row :
                    if tile =='1':
                        self.display.blit(self.border_image,(x*self.tile_size, y*self.tile_size))
                    if tile == '2':
                        self.display.blit(self.wood_image,(x*self.tile_size, y*self.tile_size)) 
                    if tile != '0':
                        self.tile_rect.append(pygame.Rect(x *self.tile_size, y*self.tile_size, self.tile_size ,self.tile_size))
                    x +=1
                y+=1 

    def get_collisions(self, tiles):
        self.hitlist = []
        for tile in tiles:
            if self.rect.colliderect(tile):
               self.hitlist.append(tile)         
        return self.hitlist
    
    def collision(self, hitlist):
        self.collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.ending = {'yes': False}
        if self.rect.colliderect(self.finish_rect):
            self.ending = True
            if self.ending == True:
                self.display.blit(self.uWon_image,self.window_size)
        if self.maploading ['Map1'] == True:
            self.map()
        if self.player_rect.y < 0:
            self.maploading['Map1'] = False
            self.maploading['Map2'] = True
            self.player_rect.y += 3500
        if self.maploading['Map2'] == True:
            self.map2()
            self.maploading['Map1'] = False
            self.display.blit(self.finish_image,self.finish_rect)
            if self.rect.colliderect(self.finish_rect):
                    self.ending = True
            if self.ending == True:
                    self.display.blit(self.uWon_image,self.window_size)
        if self.rect.left <=0:
            self.rect.left = 0
        if self.rect.right >= 3834:
            self.rect.right = 3834
                
        for tile in hitlist:
            if self.rect.bottom >= tile.top and self.rect.bottom <= tile.bottom:
                self.rect.bottom = tile.top
                self.player_falling = 0
                self.collision_types['bottom'] = True

                if self.rect.right <= tile.left:
                    self.rect.right = tile.left
                    self.collision_types['right'] = True

                elif self.rect.left >= tile.right:
                    self.rect.left = tile.right
                    self.collision_types['left'] = True
            
    def camerafollow(self):
        self.offset = vec(0, 0)
        self.offset_float = vec(0,0)
        self.DISPLAY_W, self.DISPLAY_H = 480, 270
        self.CONST = vec(-self.DISPLAY_W / 2 + self.rect.w / 2, -self.rect.y + 20)
        self.offset_float.y += (self.rect.y - self.offset_float.y + self.CONST.y)
        self.offset.y = int(self.offset_float.y)

    def player_move(self):
        self.keys = pygame.key.get_pressed()
        

        if not self.collision_types['bottom']:
            self.player_rect.y += self.player_falling
            self.player_falling += 0.5

        
        if self.keys[pygame.K_a]:
            if not self.collision_types['left']:
                self.player_rect.x -= 20

        if self.keys[pygame.K_d]:
            if not self.collision_types['right']:
                self.player_rect.x += 20

        if self.keys[pygame.K_SPACE]:
            self.player_rect.y -= 20

        if self.player_falling >40:
            self.player_falling = 40
        
            
    def draw(self):
        self.back = (pygame.transform.scale(self.background, self.display_dimension))
        self.surf = (pygame.transform.scale(self.display, self.window_size))
        #self.test = (pygame.transform.scale(self.test_surface, self.test_rect))
        self.display.blit(self.back, (0,0))
        self.screen.blit(self.surf, (0,0))
        self.display.blit(self.player_image,self.player_rect)
        
        #self.display.blit(self.test_surface, self.test_rect)
        
    def run(self):
        self.collision(self.get_collisions(self.tile_rect))
        self.player_move()
        self.draw()
        self.camerafollow()

