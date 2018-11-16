import math
import sys
import pygame
black = (0, 0, 0)
white = (255, 255, 255)
blue = (51, 204, 255)
center = (500, 300)
r = (60)
grey = (206, 208, 191)
screen = pygame.display.set_mode([1000, 600])
pygame.display.set_caption('This game never ends')
clock = pygame.time.Clock()
milli = clock.tick()

pygame.init()
font = pygame.font.Font(None, 36)
background = pygame.Surface(screen.get_size())


class Ball(pygame.sprite.Sprite):
    speed = .5

    x = 400.0
    y = 400.0

    direction = 400

    width = 20
    height = 20

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([self.width, self.height])

        self.image.fill(grey)

        self.rect = self.image.get_rect()

        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

    def bounce(self, diff):
        self.direction = (180 - self.direction) % 360
        self.direction -= diff

    def xbounce(self, diff):
        self.direction = (-360 + self.direction) % 180
        self.direction += diff

    def update(self):

        direction_radians = math.radians(self.direction)

        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        self.rect.x = self.x
        self.rect.y = self.y

        if self.y <= 0:
            self.bounce(0)
            self.y = 1

        if self.y > 600:
            self.xbounce(600)
            self.y = (599)

        if self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenwidth - self.width - 1

        if self.x <= 0:
            return True
        else:
            return False


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.width = 15
        self.height = 75
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((grey))

        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.rect.topleft = (0, self.screenheight - self.height)

    def update(self):
        pos = pygame.mouse.get_pos()

        self.rect.midtop = pos
        if self.rect.left < self.screenwidth - self.width:
            self.rect.left = self.screenheight - 500


pygame.init()

screen = pygame.display.set_mode([1000, 600])

pygame.display.set_caption('You can never win')

pygame.mouse.set_visible(0)

font = pygame.font.Font(None, 36)

background = pygame.Surface(screen.get_size())

balls = pygame.sprite.Group()
allsprites = pygame.sprite.RenderPlain()

player = Player()
allsprites.add(player)

ball = Ball()
allsprites.add(ball)
balls.add(ball)

game_over = False

exit_program = False

while exit_program != True:

    screen.fill(blue)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True
            sys.exit

    if not game_over:
        player.update()
        game_over = ball.update()

    if game_over:
        text = font.render("Game Over", 1, black)
        textpos = text.get_rect(centerx=background.get_width() / 4)
        textpos.top = 300
        screen.blit(text, textpos)

    if pygame.sprite.spritecollide(player, balls, False):
        diff = (player.rect.left + player.width / 2) - (ball.rect.left + ball.width / 2)

        ball.rect.top = screen.get_width() - player.rect.width - ball.rect.width - 1
        ball.xbounce(diff)

    screen.lock()
    pygame.draw.circle(screen, white, center, 60)
    pygame.draw.circle(screen, blue, center, 30)
    pygame.draw.circle(screen, white, center, 15)
    pygame.draw.line(screen, white, (0, 0), (0, 600), 20)
    pygame.draw.line(screen, white, (1000, 0), (0, 0), 20)
    pygame.draw.line(screen, white, (1000, 0), (1000, 600), 20)
    pygame.draw.line(screen, white, (0, 600), (1000, 600), 20)
    pygame.draw.line(screen, white, (120, 0), (120, 600), 10)

    screen.unlock()

    allsprites.draw(screen)

    pygame.display.flip()

pygame.quit()