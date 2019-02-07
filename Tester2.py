import pygame, sys
pygame.init()

windowWidth = 852
windowHeight = 480

windowSurface = pygame.display.set_mode((windowWidth,windowHeight))

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
backgroundImage = pygame.image.load('bg.jpg')
backgroundImage2 = pygame.image.load('8-bit_Space.png')
backgroundBaseImage3 = pygame.image.load('desert.png')
backgroundImage3 = pygame.transform.scale(backgroundBaseImage3 ,(852, 480))
bgImg= backgroundImage
character = pygame.image.load('standing.png')
Red = (255, 0, 0)
bgX = 0
bgY = 0
platform_Y = windowHeight - 128
platform_X = 0

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
    windowSurface.blit(bgImg, (bgX, bgY))
    pygame.draw.line(windowSurface, Red, (platform_X, 521), (windowWidth, 521), 220)
    player.draw(windowSurface)
    for bullet in bullets:
        bullet.draw(windowSurface)
    
    pygame.display.update()

def terminate():
    pygame.quit()
    sys.exit()




#mainloop
player = player(400, 240, 64,64)
bullets = []
while True:
    clock.tick(27)

    #print("Player Y = " + str(player.y))
    if player.y <= platform_Y and (player.y + player.velocity) >= platform_Y:
        player.y = platform_Y
    else:
        player.y += player.velocity
    
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

    if keys[pygame.K_LEFT]:
        player.x -= player.velocity
        player.left = True
        player.right = False
        player.standing = False
        if player.x <= 0:
            bgImg = backgroundImage3
            player.x = 851
    elif keys[pygame.K_RIGHT]:
        player.x += player.velocity
        player.right = True
        player.left = False
        player.standing = False
        if player.x > windowWidth:
            bgImg = backgroundImage2
            player.x = 1
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

	
