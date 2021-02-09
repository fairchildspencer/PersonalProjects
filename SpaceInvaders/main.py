import pygame
import os
import time
import random
pygame.font.init()

# set up window dimensions
WIDTH, HEIGHT = 750, 650
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Invaderz")

# load the graphics
RED_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
PLAYER_YELLOW_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH,HEIGHT))

class SpaceShip:
    COOLDOWN = 30

    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_image = None
        self.laser_image = None
        self.lasers = []
        self.cool_down = 0

    def render(self,window):
        WINDOW.blit(self.ship_image, (self.x, self.y))
        for laser in self.lasers:
            laser.render(window)

    def move_lasers(self, velocity, object):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(object):
                object.health -= 10
                self.lasers.remove(laser)

    def get_width(self):
        return self.ship_image.get_width()

    def get_height(self):
        return self.ship_image.get_height()

    def cooldown(self):
        if self.cool_down >= self.COOLDOWN:
            self.cool_down = 0
        elif self.cool_down > 0:
            self.cool_down += 1

    def shoot(self):
        if self.cool_down == 0:
            laser = Laser(self.x, self.y, self.laser_image)
            self.lasers.append(laser)
            self.cool_down = 1

class Player(SpaceShip):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_image = PLAYER_YELLOW_SHIP
        self.laser_image = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.full_health = health

    def move_lasers(self, velocity, objects):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for object in objects:
                    if laser.collision(object):
                        objects.remove(object)
                        self.lasers.remove(laser)

class Enemy(SpaceShip):
    COLORS = {
                "red": (RED_SHIP, RED_LASER),
                "blue": (BLUE_SHIP, BLUE_LASER),
                "green": (GREEN_SHIP, GREEN_LASER)
             }

    def __init__(self, x, y, color, health = 100):
        super().__init__(x, y, health)
        self.ship_image, self.laser_image = self.COLORS[color]
        self.mask = pygame.mask.from_surface(self.ship_image)

    def move(self, velocity):
        self.y += velocity

    def shoot(self):
        if self.cool_down == 0:
            laser = Laser(self.x - 15, self.y, self.laser_image)
            self.lasers.append(laser)
            self.cool_down = 1

class Laser:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)

    def render(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self, velocity):
        self.y += velocity

    def off_screen(self, height):
        return not self.y <= height and self.y >= 0

    def collision(self, object):
        return collide(object, self)

def collide(object1, object2):
    offset_x = object1.x - object2.x
    offset_y = object1.y - object2.y
    return object1.mask.overlap(object2.mask, (offset_x, offset_y)) != None


def main():
    #initialize default values
    run = True
    lost = False
    lost_count = 0
    fps = 60
    level = 0
    lives = 3

    player_velocity = 5
    laser_velocity = 4

    enemies = []
    wave_length = 5
    enemy_velocity = 1

    font = pygame.font.SysFont("comicsans",50)
    font_lost = pygame.font.SysFont("comicsans", 80)
    clock = pygame.time.Clock()

    player = Player(375,550)

    def render_window():
        WINDOW.blit(BACKGROUND, (0,0))
        # render text
        lives_text = font.render(f"Lives: {lives}", 1, (255,255,255))
        level_text = font.render(f"Level: {level}", 1, (255,255,255))

        WINDOW.blit(lives_text, (10,10))
        WINDOW.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))

        for enemy in enemies:
            enemy.render(WINDOW)

        player.render(WINDOW)

        if lost:
            lost_text = font_lost.render("You Lost :(", 1, (255,0,0))
            WINDOW.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, 350))
        
        pygame.display.update()
    
    while run:
        clock.tick(fps)
        render_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > fps * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 50), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_velocity > 0: #left
            player.x -= player_velocity
        if keys[pygame.K_d] and player.x + player_velocity + player.get_width() < WIDTH: #right 
            player.x += player_velocity
        if keys[pygame.K_w] and player.y - player_velocity > 0: #up 
            player.y -= player_velocity
        if keys[pygame.K_s] and player.y + player_velocity + player.get_height() < HEIGHT: #down 
            player.y += player_velocity
        if keys[pygame.K_SPACE]: #shoot
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_velocity)
            enemy.move_lasers(laser_velocity, player)

            if random.randrange(0, 4 * fps) == 1:
                enemy.shoot()

            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_velocity, enemies)
main()

  
