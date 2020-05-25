import pygame
import random
pygame.init()
pygame.font.init()

WIN_WIDTH = 928
WIN_HEIGHT = 793

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
STAT_FONT = pygame.font.SysFont("comicsans", 50)
pygame.display.set_caption("Zombie Hop")
music = pygame.mixer.music.load("final.mp3")
pygame.mixer.music.play(-1)
''' 
    Sprites are downloaded from 
    https://www.gameart2d.com/the-zombies-free-sprites.html and 
    https://edermunizz.itch.io/free-pixel-art-forest

    Music downloaded from
    http://soundbible.com/ 
'''

walking_imgs = [pygame.image.load('Walk (1).png'),pygame.image.load('Walk (2).png'),pygame.image.load('Walk (3).png'),pygame.image.load('Walk (4).png'),pygame.image.load('Walk (5).png'),pygame.image.load('Walk (6).png'),pygame.image.load('Walk (7).png'),pygame.image.load('Walk (8).png'),pygame.image.load('Walk (9).png'),pygame.image.load('Walk (10).png')]
walk = []
for img in range(len(walking_imgs)):
    walk.append(pygame.transform.scale(walking_imgs[img] , (150, 170)))
bg = pygame.image.load('bg.png')
stand = pygame.transform.scale( pygame.image.load('Idle (1).png') , (150, 170))
cactus_img = pygame.transform.scale(pygame.image.load('cactus_3.png'), (120, 140))
cactus_imgs = [pygame.transform.scale(pygame.image.load('cactus_1.png'), (120, 140)),  pygame.transform.scale(pygame.image.load('cactus_2.png'), (120, 140)),  pygame.transform.scale(pygame.image.load('cactus_3.png'), (120, 140)),  pygame.transform.scale(pygame.image.load('cactus_4.png'), (120, 140))]

clock = pygame.time.Clock()
#laugh.play()
class Char(object):
    """
        This class represents main Zombie character
    """
    def __init__(self,x,y):
        """
            Initialize the object
            :param x: int
            :param y: int
            :return: None
        """
        self.x = x
        self.y = y
        self.walkCount = 0
        self.standing = True
        self.isJump = False
        self.jumpCount = 10

    def draw(self, win):
        """
            Draw the Zombie character and make it walk, jump and stand still
            :param win: the pygame surface/window
            :return: None
        """
        if self.walkCount + 1 >= 30:
            self.walkCount = 0

        if not(self.standing):
            win.blit(walk[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
        else:
            win.blit(stand, (self.x,self.y))                

    def get_mask(self):
        """
            Gets the mask for the current image of the bird
            :return: None
        """
        return pygame.mask.from_surface(walk[0])       

class Cactus():
    """
        This class represents main Cactus obstacles
    """
    VEL = 10
    CACTUS_BOTTOM = cactus_img

    def __init__(self, x, y, img_id):
        """
            Initialize the object
            :param x: int
            :param y: int
            :return: None
        """
        self.x = x
        self.y = y
        self.img_id = img_id
        self.passed = False

    def move(self):
        """
            Move the Cactus to left
            :return: None
        """        
        self.x -= self.VEL

    def collide(self, zombie):
        """
            returns True if a Zombie is colliding with the Cactus
            :param zombie: Char object
            :return: Bool
        """

        zombie_mask = zombie.get_mask()
        cactus_mask = pygame.mask.from_surface(self.CACTUS_BOTTOM)
        offset = (self.x - zombie.x + 5, self.y - round(zombie.y) + 7)

        b_point = zombie_mask.overlap(cactus_mask, offset)

        if b_point:
            return True

        return False    

    def draw(self, win):
        """
            Draw the Cactus
            :param win: the pygame surface/window
            :return: None
        """
        if self.img_id > 3:
            win.blit(cactus_imgs[0], (self.x,self.y))
        else:
            win.blit(cactus_imgs[self.img_id], (self.x,self.y))       



class Bgscroll:
    """
        Represnts the moving background of the game
    """
    VEL = 10
    WIN_WIDTH = WIN_WIDTH
    WIDTH = bg.get_width()
    IMG = pygame.image.load('bg.png')

    def __init__(self, y):
        """
            Initialize the object
            :param y: int
            :return: None
        """
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """
            Move backgrond image so it looks like its scrolling
            :return: None
        """
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        """
            Draw the backgrond. This is two images that move together.
            :param win: the pygame surface/window
            :return: None
        """
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def redrawGameWindow(win, zombie, cactuses, bgscroll, score):
    ''' 
        This function draws the game components on screen in real time 
        :return: None
    '''
    win.blit(bg, (0,0))
    bgscroll.draw(win)
    zombie.draw(win)
    for cactus in cactuses:
        cactus.draw(win)

    #Score
    score_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    pygame.display.update()

# main loop
def main(win):

    zombie = Char(200, 570)
    bgscroll= Bgscroll(0)
    cactuses = [Cactus(600, 600, 4)]
    run = True
    START_GAME = False
    lost = False
    score = 0
    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

                
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            START_GAME = True

        if START_GAME and not lost:
            bgscroll.move()
            zombie.standing = False        
            add_cactus = False
            rem = []
            for cactus in cactuses:
                cactus.move()
                if cactus.collide(zombie):
                    lost = True
                    START_GAME = False
                if cactus.x + cactus.CACTUS_BOTTOM.get_width() < 0:
                    rem.append(cactus)
                if not cactus.passed and cactus.x < zombie.x:
                    cactus.passed = True
                    add_cactus = True
                    score += 1
            if add_cactus:
                cactuses.append(Cactus(WIN_WIDTH, 600, random.randint(0,3)))
            for r in rem:
                cactuses.remove(r)                 
        else:
            zombie.standing = True
            zombie.walkCount = 0

        if not(zombie.isJump):
            if keys[pygame.K_SPACE]:
                zombie.isJump = True
                zombie.walkCount = 0
        else:
            if zombie.jumpCount >= -10:
                neg = 1
                if zombie.jumpCount < 0:
                    neg = -1
                zombie.y -= (zombie.jumpCount ** 2) * 0.5 * neg
                zombie.jumpCount -= 1
            else:
                zombie.isJump = False
                zombie.jumpCount = 10    

        redrawGameWindow(win, zombie, cactuses, bgscroll, score)

    pygame.quit()
    quit()

main(win)