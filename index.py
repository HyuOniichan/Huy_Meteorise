#import

import pygame 
from pygame.locals import * 
import random 
import math 
import time 

pygame.init() 



#screen

screen_width = 1000 
screen_height = 700 

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_icon(pygame.image.load('./assets/play.png'))
pygame.display.set_caption('Meteorise')

background = pygame.image.load('./assets/universe.jpg')
clock = pygame.time.Clock() 
score = 0 
lv = 1; 



#player 

playerSize = 50 
playerImage = pygame.transform.scale(pygame.image.load('./assets/play.png'), (playerSize, playerSize))
posx = (screen_width - playerSize) / 2
posy = (screen_height - playerSize) / 2
move = 6 + 0.0 
direction = 'up'



#meteor 

ms = 2; 
mx = 0; my = 0; md = 0; 
meteorNumber = 5; 
meteor = []



#bullet 

bulletImage = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('./assets/bullet.png'), (playerSize / 2, playerSize / 2)), 90)
bx = posx + playerSize / 4; 
by = posy + playerSize / 4; 
bs = 8; 
fire = False; 
directionBullet = 'up' 



#skill 

    #laser 

laserAct = False; 
laserUse = time.time(); 
laserUsing = False; 
directionLaser = 'up' 
laserDistance = 1000 
laserTime = 10 

    #shield 

shieldAct = False; 
shieldTime = 5 


#planet 

planetAppear = time.time() 
px = 0; py = 0; pd = 0; 
planetAct = False 





class Player(pygame.sprite.Sprite): 
    def __init__(self): 
        super(Player, self).__init__() 
        self.surf = playerImage

    def control(self): 
        global posx, posy, direction, bx, by 
        if laserAct: return; 
        holding = pygame.key.get_pressed() 
        if holding[pygame.K_w]: 
            if posy > 0: 
                posy -= move 
                direction = 'up'
                self.surf = pygame.transform.rotate(playerImage, 0)
                if fire == False: 
                    bx = posx + playerSize / 4 
                    by = posy + playerSize / 4 
        elif holding[pygame.K_s]: 
            if posy < screen_height - playerSize: 
                posy += move 
                direction = 'down'
                self.surf = pygame.transform.rotate(playerImage, 180)
                if fire == False: 
                    bx = posx + playerSize / 4 
                    by = posy + playerSize / 4 
        elif holding[pygame.K_a]: 
            if posx > 0: 
                posx -= move 
                direction = 'left'
                self.surf = pygame.transform.rotate(playerImage, 90)
                if fire == False: 
                    bx = posx + playerSize / 4 
                    by = posy + playerSize / 4 
        elif holding[pygame.K_d]: 
            if posx < screen_width - playerSize: 
                posx += move 
                direction = 'right'
                self.surf = pygame.transform.rotate(playerImage, 270)
                if fire == False: 
                    bx = posx + playerSize / 4 
                    by = posy + playerSize / 4 


main = Player()        


""" 
3 kinds of object (meteor) 
+ normal 
+ fast (move faster)
+ hp (2 hit to destroy)

1 kind of gift (earth) 
-> have 1 laser, shield or sth 
 """


class Meteor(pygame.sprite.Sprite): 
    def __init__(self, type):
        super(Meteor, self).__init__()

        self.surf = pygame.image.load('./assets/meteor.png') 
        m_xyd = meteorRandom() 
        self.m_x = m_xyd[0] 
        self.m_y = m_xyd[1] 
        self.m_d = m_xyd[2]

        self.type = type 
        
        if (self.type == 1): 
            self.surf = pygame.transform.scale(pygame.image.load('./assets/meteor.png'), (playerSize, playerSize))
            self.hp = 1; 
            self.speed = ms; 
        elif (self.type == 2): 
            self.surf = pygame.transform.scale(pygame.image.load('./assets/meteor_fast.png'), (playerSize, playerSize))
            self.hp = 1; 
            self.speed = ms * 2; 
        elif (self.type == 3): 
            self.surf = pygame.transform.scale(pygame.image.load('./assets/meteor_hp.png'), (playerSize, playerSize))
            self.hp = 2; 
            self.speed = ms; 

    def flying(self): 
        global score, fire 

        if (self.m_d == 1): 
            self.m_y += self.speed; 
            if self.m_y > screen_height: 
                r = meteorRandom(); 
                self.m_x = r[0] 
                self.m_y = r[1] 
                self.m_d = r[2] 
        elif (self.m_d == 2): 
            self.m_y -= self.speed; 
            if self.m_y < 0: 
                r = meteorRandom(); 
                self.m_x = r[0] 
                self.m_y = r[1] 
                self.m_d = r[2] 
        elif (self.m_d == 3): 
            self.m_x += self.speed; 
            if self.m_x > screen_width: 
                r = meteorRandom(); 
                self.m_x = r[0] 
                self.m_y = r[1] 
                self.m_d = r[2] 
        elif (self.m_d == 4): 
            self.m_x -= self.speed; 
            if self.m_x < 0: 
                r = meteorRandom(); 
                self.m_x = r[0] 
                self.m_y = r[1] 
                self.m_d = r[2] 




def meteorRandom(): 
    global mx, my, md 
    r = random.randint(1, 4) 
    if (r == 1): 
        mx = random.randint(0, screen_width) 
        my = -playerSize
        md = 1 
    elif (r == 2): 
        mx = screen_width 
        my = random.randint(0, screen_height)
        md = 4 
    elif (r == 3): 
        mx = random.randint(0, screen_width) 
        my = screen_height 
        md = 2 
    elif (r == 4): 
        mx = -playerSize
        my = random.randint(0, screen_height)
        md = 3 
    return mx, my, md



class Skill(pygame.sprite.Sprite): 
    def __init__(self, type):
        super(Skill, self).__init__()
        if type == 'laser': 
            self.surf = pygame.transform.scale(pygame.transform.rotate(pygame.image.load('./assets/laser.png'), 90), (playerSize * 2, laserDistance))
        if type == 'aura': 
            self.surf = pygame.transform.scale(pygame.image.load('./assets/aura.png'), (playerSize, playerSize))
        if type == 'shield': 
            self.surf = pygame.transform.scale(pygame.image.load('./assets/shield.png'), (playerSize * 3/2, playerSize * 3/2))

laser = Skill('laser')
aura = Skill('aura')
shield = Skill('shield') 



class Planet(pygame.sprite.Sprite): 
    def __init__(self):
        super(Planet, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load("./assets/planet.png"), (playerSize, playerSize)) 
        self.rd() 

    def rd(self): 
        r = random.randint(1, 4) 
        if (r == 1): 
            self.px = random.randint(0, screen_width) 
            self.py = -playerSize
            self.pd = 1 
        elif (r == 2): 
            self.px = screen_width 
            self.py = random.randint(0, screen_height)
            self.pd = 4 
        elif (r == 3): 
            self.px = random.randint(0, screen_width) 
            self.py = screen_height 
            self.pd = 2 
        elif (r == 4): 
            self.px = -playerSize
            self.py = random.randint(0, screen_height)
            self.pd = 3 

    def flying(self): 
        global laserTime, shieldTime, planetAct
        if (self.pd == 1): 
            if self.py < screen_height: 
                self.py += 1; 
            else: 
                self.rd() 
                plantAct = False; 
        elif (self.pd == 2): 
            if self.py > 0: 
                self.py -= 1; 
            else: 
                self.rd() 
                plantAct = False; 
        elif (self.pd == 3): 
            if self.px < screen_width: 
                self.px += 1; 
            else: 
                self.rd() 
                plantAct = False; 
        elif (self.pd == 4):  
            if self.px > 0: 
                self.px -= 1;
            else: 
                self.rd() 
                plantAct = False; 
        
        if collision(self.px, self.py, posx, posy, playerSize): 
            r = random.randint(1, 2) 
            if r == 1: 
                laserTime += random.randint(1, 5) 
            elif r == 2: 
                shieldTime += random.randint(1, 3) 
            
            self.rd() 
            planetAct = False 

planet = Planet() 



font = pygame.font.SysFont('Arial', 20) 

def infoText(): 
    padding = 10 

    scoreImg = font.render(f'Score: {score}', True, 'white') 
    screen.blit(scoreImg, (padding, 10)) 
    padding += scoreImg.get_width() + 20

    lvImg = font.render(f'Level: {lv}', True, 'white')
    screen.blit(lvImg, (padding, 10))
    padding += lvImg.get_width() + 20 

    laserImg = font.render(f'Laser (L): {laserTime}', True, 'white')
    screen.blit(laserImg, (padding, 10))
    padding += laserImg.get_width() + 20
    
    shieldImg = font.render(f'Shield (J): {shieldTime}', True, 'white') 
    screen.blit(shieldImg, (padding, 10))
    padding += shieldImg.get_width() + 20 

    bulletImg = font.render('Bullet (K): 1', True, 'white') 
    screen.blit(bulletImg, (padding, 10))


    
#stop all the activities 
def gameOver(): 
    overImg = font.render(f'GAMEOVER!', True, 'white') 
    screen.blit(overImg, (screen_width / 2, screen_height / 2))



def collision(x1, y1, x2, y2, ok): 
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2)) 
    if (distance < ok): return True; 
    else: return False; 



def render(): 
    global direction, mx, my, md, fire, bx, by, directionBullet, score, lv 
    global meteorNumber, meteor, planetAct 
    global laserAct, laserUse, laserUsing, directionLaser, shieldAct, shieldTime

    screen.blit(background, (0, 0))

    screen.blit(main.surf, (posx, posy))  
    main.control() 

    infoText() 

    #bullet 

    attackImage = bulletImage

    if (directionBullet == 'up'): 
        attackImage = pygame.transform.rotate(bulletImage, 0) 
    elif (directionBullet == 'down'): 
        attackImage = pygame.transform.rotate(bulletImage, 180)
    elif (directionBullet == 'right'): 
        attackImage = pygame.transform.rotate(bulletImage, 270)
    elif (directionBullet == 'left'): 
        attackImage = pygame.transform.rotate(bulletImage, 90)


    if fire: 
        if (directionBullet == 'up'): 
            if (by > 0): by -= bs; 
            else: 
                by = posy + playerSize / 4
                fire = False 
        elif (directionBullet == 'down'): 
            if (by < screen_height - playerSize): by += bs; 
            else: 
                by = posy + playerSize / 4
                fire = False 
        elif (directionBullet == 'right'): 
            if (bx < screen_width - playerSize): bx += bs; 
            else: 
                bx = posx + playerSize / 4
                fire = False 
        elif (directionBullet == 'left'): 
            if (bx > 0): bx -= bs; 
            else: 
                bx = posx + playerSize / 4
                fire = False 

        screen.blit(attackImage, (bx, by))

    else: 
        directionBullet = direction
        bx = posx + playerSize / 4
        by = posy + playerSize / 4

    #meteor 

    if (score > lv * 100): 
        lv += 1
        meteorNumber += 1 
        planetAct = True; 

    for i in range (meteorNumber - len(meteor)): 
        x = Meteor(random.randint(1, 3)) 
        meteor.append(x) 


    for i in meteor: 
        check = False; 

        i.flying() 
        
        screen.blit(i.surf, (i.m_x, i.m_y))

        if collision(i.m_x, i.m_y, bx, by, playerSize): 
            if fire == True: 
                fire = False; 
                i.hp -= 1 
                if (i.hp == 1): 
                    i.surf = pygame.transform.scale(pygame.image.load('./assets/meteor.png'), (playerSize, playerSize))
                elif (i.hp == 0): 
                    if (i.type == 1): score += 10; 
                    elif (i.type == 2): score += 20; 
                    elif (i.type == 3): score += 20; 
                    check = True; 

        #end game 
        if collision(i.m_x, i.m_y, posx, posy, playerSize): 
            print("Score: ", score)  
            print("Level: ", lv)  
            exit() 

        if laserAct: 
            if directionLaser == 'up': 
                if i.m_x > posx - playerSize * 3/2 and i.m_x < posx + playerSize * 2 and i.m_y > -playerSize and i.m_y < posy: 
                    if (i.type == 1): score += 10; 
                    elif (i.type == 2): score += 20; 
                    elif (i.type == 3): score += 20; 
                    check = True; 
            elif directionLaser == 'down': 
                if i.m_x > posx - playerSize * 3/2 and i.m_x < posx + playerSize * 2 and i.m_y > posy + playerSize and i.m_y < screen_height + playerSize: 
                    if (i.type == 1): score += 10; 
                    elif (i.type == 2): score += 20; 
                    elif (i.type == 3): score += 20; 
                    check = True; 
            elif directionLaser == 'right': 
                if i.m_x > posx + playerSize and i.m_x < screen_width + playerSize and i.m_y > posy - playerSize * 3/2 and i.m_y < posy + playerSize * 2: 
                    if (i.type == 1): score += 10; 
                    elif (i.type == 2): score += 20; 
                    elif (i.type == 3): score += 20; 
                    check = True; 
            elif directionLaser == 'left': 
                if i.m_x > -playerSize and i.m_x < posx and i.m_y > posy - playerSize * 3/2 and i.m_y < posy + playerSize * 2: 
                    if (i.type == 1): score += 10; 
                    elif (i.type == 2): score += 20; 
                    elif (i.type == 3): score += 20; 
                    check = True; 

        if shieldAct: 
            if collision(i.m_x, i.m_y, posx - playerSize / 4, posy - playerSize / 4, playerSize * 3/2): 
                shieldAct = False; 
                if (i.type == 1): score += 10; 
                elif (i.type == 2): score += 20; 
                elif (i.type == 3): score += 20; 
                check = True; 

        if check: meteor.remove(i); 
                


    #skill - laser 

    if laserAct: 
        if laserUsing: 
            laserUse = time.time() 
            laserUsing = False 
        endLaser = time.time() 
        if endLaser < laserUse + 0.3: 
            if directionLaser == 'up': 
                screen.blit(laser.surf, (posx - playerSize / 2, posy - laserDistance))
                screen.blit(aura.surf, (posx, posy))
            elif directionLaser == 'down': 
                screen.blit(pygame.transform.rotate(laser.surf, 180), (posx - playerSize / 2, posy + playerSize))
                screen.blit(pygame.transform.rotate(aura.surf, 180), (posx, posy))
            elif directionLaser == 'right': 
                screen.blit(pygame.transform.rotate(laser.surf, 270), (posx + playerSize, posy - playerSize / 2))
                screen.blit(pygame.transform.rotate(aura.surf, 270), (posx, posy))
            elif directionLaser == 'left': 
                screen.blit(pygame.transform.rotate(laser.surf, 90), (posx - laserDistance, posy - playerSize / 2))
                screen.blit(pygame.transform.rotate(aura.surf, 90), (posx, posy))
        else: laserAct = False; 
    else: directionLaser = direction; 

    #skill - shield 

    if shieldAct: 
        screen.blit(shield.surf, (posx - playerSize / 4, posy - playerSize / 4))

    #planet 

    if planetAct: 
        planet.flying() 
        screen.blit(planet.surf, (planet.px, planet.py))



# play 

playing = False 
running = True 

while running: 
    clock.tick(60) 

    for event in pygame.event.get(): 
        if event.type == KEYDOWN: 
            if event.key == K_SPACE: 
                if playing: playing = False 
                else: playing = True
            elif event.key == K_ESCAPE: 
                running = False 
            elif event.key == K_k: 
                if fire == False: 
                    fire = True 
                    directionBullet = direction
            elif event.key == K_l: 
                if laserTime > 0: 
                    laserTime -= 1; 
                    laserAct = True; 
                    laserUsing = True; 
            elif event.key == K_j: 
                if shieldTime > 0 and shieldAct == False: 
                    shieldTime -= 1; 
                    shieldAct = True; 
        elif event.type == QUIT: 
            running = False 
        
    if playing: render() 
    else: 
        startImg = font.render('Press spacebar to start/pause', True, 'white') 
        screen.blit(startImg, (screen_width // 2 - 110, screen_height // 2)) 

    pygame.display.update() 



