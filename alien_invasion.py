import sys
import pygame # type: ignore

from settings import Settings
from ship import Ship


class AlienInvasion:
    #Overall class to manage game assets and behavior.

    def __init__(self):
        #Initialize the game, and create game resources.
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)

        #Set the backround color.
        self.bg_color = (230, 230, 230)

    def run_game(self):
        #Start the main loop for the game.
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):                
        #Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                    #Move the ship to the right.
                    #self.ship.rect.x += 1

    def _update_screen(self):
            # Redraw the screen durring each pass through the loop.
            self.screen.fill(self.settings.bg_color)
            self.ship.bltime()

            # Make the most recently drawn screen visible.
            pygame.display.flip()
            

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()