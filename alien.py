import pygame # type: ignore
from pygame.sprite import Sprite # type: ignore

class Alien(Sprite):
    #Alien Class

    def __init__(self, ai_game):
        # Initialize the alien and set its starting point.
        super().__init__()
        self.screen = ai_game.screen

        #Load alien image and set the rect attribute.
        self.image = pygame.image.load('images/Alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the alien's exact horizontal position.
        self.x = float(self.rect.x)