# Game loop function (60 fps)
# https://realpython.com/pygame-a-primer/#basic-pygame-program

import pygame
import math.maheshwashere
from pygame.locals import (
  K_UP,
  K_DOWN,
  K_LEFT,
  K_RIGHT,
  K_SPACE,
  K_ESCAPE,
  KEYDOWN,
)
screen = None
currentPlayer = None
currentProjectile = None
playerOne = None
playerTwo = None
all_sprites = None

class Projectile(pygame.sprite.Sprite):

  def __init__(self, x, y, speedx, speedy, image):
    super(Projectile, self).__init__()
    # self.surf = pygame.image.load(image).convert()
    # self.surf.set_colorkey((255, 255, 255), RLEACCEL)
    self.image = pygame.image.load(image)

    # self.rect = self.surf.get_rect()
    self.x = x
    self.y = y
    self.speedx = speedx
    self.speedy = speedy

  def move(self, gravity=10):
    print("vx: "+str(self.speedx))
    print("vy: "+str(self.speedy))
    print("(x, y): "+str(self.x)+str(self.y))
    self.x += self.speedx
    self.y += self.speedy
    self.speedy += gravity

  def intercepts(self):
    if pygame.sprite.spritecollide(self, playerOne):
      return playerOne
    elif pygame.sprite.spritecollide(self, playerTwo):
      return playerTwo

class Tank(pygame.sprite.Sprite):

  def __init__(self, x, y, launchSpeed, launchAngle, pictureName):
    super(Tank, self).__init__()
    self.x = x
    self.y = y
    self.launchSpeed = launchSpeed
    self.launchAngle = launchAngle
    # self.surf = pygame.image.load(pictureName).convert()
    # self.surf.set_colorkey((255, 255, 255), RLEACCEL)
    self.image = pygame.image.load(pictureName)
    self.rect = self.image.get_rect()
    self.dx = 0


  def adjustAngle(self, upNotDown):
    if upNotDown:
      self.launchAngle += 5
    else:
      self.launchAngle -= 5
    print(f"adjusted angle to {self.launchAngle} degrees")
  def move(self, amnt):
    tempdx = self.dx+amnt
    if math.fabs(tempdx) > 100:
      return
    self.x += amnt
    self.dx += amnt
    self.rect.move_ip(amnt, 0)

  def launch(self):
    global currentProjectile
    currentProjectile = Projectile(self.x, self.y, self.launchSpeed * math.cos(self.launchAngle),
    self.launchSpeed * math.sin(self.launchAngle), "images\smallTankProjectile.png")


def gameInit():
  global currentPlayer, playerOne, playerTwo
  playerOne = Tank(100, 600, 1, -45, "images\smallBlueTank.png")
  currentPlayer = playerOne
  playerTwo = Tank(700, 600, 1, -135, "images\smallRedTank.png")


def update():
  keys = pygame.key.get_pressed()
  # print("hit Key " + str(keys))
  global currentPlayer, playerOne, playerTwo
  
  if keys[K_RIGHT]:
    currentPlayer.move(5)
  elif keys[K_LEFT]:
    currentPlayer.move(-5)
  elif keys[K_UP]:
    currentPlayer.adjustAngle(True)
  elif keys[K_DOWN]:
    currentPlayer.adjustAngle(False)
  elif keys[K_SPACE] and currentProjectile==None:
    currentPlayer.launch()
  
  screen.blit(playerOne.image, (playerOne.x, playerOne.y))
  screen.blit(playerTwo.image, (playerTwo.x, playerTwo.y))
  if currentProjectile!=None:
    currentProjectile.move()
    screen.blit(currentProjectile.image, (currentProjectile.x, currentProjectile.y))

  
  if currentPlayer == playerOne:
    currentPlayer = playerTwo
  elif currentPlayer == playerTwo:
    currentPlayer = playerOne
  else:
    print("should not have reached here")
def gameLoop():
  pygame.init()
  fps = 20
  timer = pygame.time.Clock()
  
  global screen
  screen = pygame.display.set_mode([800, 800])
  screen.fill((255, 255, 255))
  running = True
  gameInit()
  while running:
    timer.tick(fps)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        print("quit")
        running = False
      elif event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          running = False
      screen.fill((255, 255, 255))
      update()

    pygame.display.flip()
  pygame.quit()
gameLoop()