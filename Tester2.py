import pygame, sys
pygame.init()

windowWidth = 852
windowHeight = 480

windowSurface = pygame.display.set_mode((windowWidth,windowHeight))

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
backgroundImage = pygame.image.load('bg.jpg')
character = pygame.image.load('standing.png')
bgX = 0
bgY = 0

clock = pygame.time.Clock()

pygame.display.set_caption("Second Game")

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True

    def draw(self, windowSurface):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                windowSurface.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                windowSurface.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                windowSurface.blit(walkRight[0], (self.x, self.y))
            else:
                windowSurface.blit(walkLeft[0], (self.x, self.y))
                


class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.velocity = 8 * facing

    def draw(self,windowSurface):
        pygame.draw.circle(windowSurface, self.color, (self.x,self.y), self.radius)
    

def redrawGameWindow():
    windowSurface.blit(backgroundImage, (bgX, bgY))
    player.draw(windowSurface)
    for bullet in bullets:
        bullet.draw(windowSurface)
    
    pygame.display.update()

def terminate():
    pygame.quit()
    sys.exit()


#mainloop
player = player(200, 410, 64,64)
bullets = []
while True:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        
    for bullet in bullets:
        if bullet.x < windowWidth and bullet.x > 0:
            bullet.x += bullet.velocity
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        terminate()

    if keys[pygame.K_SPACE]:
        if player.left:
            facing = -1
        else:
            facing = 1
            
        if len(bullets) < 5:
            bullets.append(projectile(round(player.x + player.width //2), round(player.y + player.height//2), 6, (0,0,0), facing))

    if keys[pygame.K_LEFT] and player.x > player.velocity:
        player.x -= player.velocity
        player.left = True
        player.right = False
        player.standing = False
        backgroundImage.scroll(-5, 0)
    elif keys[pygame.K_RIGHT] and player.x < windowWidth - player.width - player.velocity:
        player.x += player.velocity
        player.right = True
        player.left = False
        player.standing = False
        backgroundImage.scroll(5, 0)
    else:
        player.standing = True
        player.walkCount = 0
        
    if not(player.isJump):
        if keys[pygame.K_UP]:
            player.isJump = True
            player.right = False
            player.left = False
            player.walkCount = 0
    else:
        if player.jumpCount >= -10:
            neg = 1
            if player.jumpCount < 0:
                neg = -1
            player.y -= (player.jumpCount ** 2) * 0.5 * neg
            player.jumpCount -= 1
        else:
            player.isJump = False
            player.jumpCount = 10
            
    redrawGameWindow()

	
