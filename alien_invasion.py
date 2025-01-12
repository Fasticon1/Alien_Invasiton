import sys
import pygame # type: ignore

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


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
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #Set the backround color.
        self.bg_color = (230, 230, 230)

    def run_game(self):
        #Start the main loop for the game.
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()            
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):                
        #Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        # Respont to keypresses.
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
         # Respond to key releases.
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        #Creat a new bullet and add it to the bullets group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
            #Update position of bullets and get rid of old bullets.
            #Update bullet positions.
            self.bullets.update()
        #Get rid of the bullets that go off top of the screen
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <=0:
                    self.bullets.remove(bullet)                                
            #this line helps's verify that bullets are being removed.
            #print(len(self.bullets))
            self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
            # Check for any bullets that have hit aliens.
            # If so, get rid of the bullet and the alien.
            collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)
            
            if not self.aliens:
                # Destriy existing bullets and create new fleet.
                self.bullets.empty()
                self._create_fleet()

    def _create_fleet(self):
        #Create the alien fleet.
        #Create an alien and keep adding aliens until there's no more room
        # Spacing is one alien width and height apart.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 10 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            #Finished a row; reset x vale, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
            new_alien = Alien(self)
            new_alien.x = x_position 
            new_alien.rect.x = x_position
            new_alien.rect.y = y_position
            self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        # Respond appropriately if any aliens have reached an edge.
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        # Drop the entire fleet and change direction.
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        # Check if fleet is at an edge, the update positions.
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!!!")

    def _update_screen(self):
            # Redraw the screen durring each pass through the loop.
            self.screen.fill(self.settings.bg_color)
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.ship.bltime()
            self.aliens.draw(self.screen)

            # Make the most recently drawn screen visible.
            pygame.display.flip()
            

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()