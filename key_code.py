import pygame
import random
import math

pygame.init() 

screen = pygame.display.set_mode((1000, 800)) 
background = pygame.image.load('Resources/Background.png') 
Player = pygame.transform.scale(pygame.image.load('Resources/Player.png'), (150, 150))
Bullet = pygame.transform.scale(pygame.image.load('Resources/Bullet.png'), (50, 50)) 
Piy = pygame.mixer.Sound('Resources/Sound_laser.ogg')
Piy.set_volume(0.5)
Bah = pygame.mixer.Sound('Resources/Sound_bah.ogg')
Bah.set_volume(0.1)
#Music = pygame.mixer.Sound('Resources/Music.mp3')
#Music.set_volume(0.6)
pygame.mixer.music.load('Resources/Music.mp3')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.6)
font = pygame.font.Font('Resources/font.ttf', 32) 
gameover_font = pygame.font.Font('Resources/font.ttf', 94) 
score_font = pygame.font.Font('Resources/font.ttf', 64)

pygame.display.set_caption("The Little defender of Space") 
pygame.display.set_icon(pygame.image.load('Resources/Icon.bmp')) 


playerX, playerY = 450, 650 
playerXchange = 0 
enemyDisplay = [] 
enemyX, enemyY = [], [] 
enemyX_change, enemyY_change = [], [] 
num_of_enemy = 20 
bulletX, bulletY = 0, 675 
bulletXchange, bulletYchange = 0, 8 
bullet_state = "готово" 
textX, textY = 10, 10 
score, scoreSum  = 0, 0 
anim_background = -280
finish = False 
gatcha = True
difficulty = 3
speed = 2

for i in range(num_of_enemy):
    enemyDisplay.append(pygame.transform.scale(pygame.image.load('Resources/Enemy.png'), (120, 120)))

    enemyX.append(random.randint(0, 885))  
    enemyY.append(random.randint(30, 180)) 
    enemyX_change.append(1) 
    enemyY_change.append(20) 

def calculation():
    global player, enemy, fire_bullet, show_score, gameover, collide

    def player(playerX, playerY):
        if finish == False:
            screen.blit(Player, (playerX, playerY)) 
    def enemy(enemyX, enemyY, i):
        screen.blit(enemyDisplay[i], (enemyX, enemyY))  
    def fire_bullet(x, y):  
        global bullet_state
        bullet_state = "залп" 
        screen.blit(Bullet, (x + 16, y + 10)) 
        screen.blit(Bullet, (x + 76, y + 10)) 
    def show_score(x, y):
        score = font.render("Счет: " + str(scoreSum), True, (255, 255, 255))  
        if finish == False: 
            screen.blit(score, (x, y))
    def gameover():
        screen.fill((0,0,0)) 
        score = score_font.render("Счет: " + str(scoreSum), True, (255, 255, 255)) 
        gameover_text = gameover_font.render("КОНЕЦ ИГРЫ", True, (255, 255, 255))  
        screen.blit(gameover_text, (280, 300))
        screen.blit(score, (390, 400))
        pygame.mixer.music.pause()
    def collide(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt(math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)) 
        if distance <= 52:
            return True
        else:
            return False

calculation()
main_cycle = True 
while main_cycle:
    fps = pygame.time.Clock()
    #Music.play()
    screen.fill((0, 0, 0)) #
    screen.blit(background, (-400, anim_background))
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            main_cycle = False 

        if event.type == pygame.KEYDOWN and finish == False: 
            if event.key == pygame.K_d:
                playerXchange += speed 
            if event.key == pygame.K_a: 
                playerXchange -= speed 
            if event.key == pygame.K_SPACE:
                if bullet_state == "готово": 
                    Piy.play()
                    bulletX = playerX 
                    fire_bullet(bulletX, bulletY) 
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_a or event.key == pygame.K_d: 
                playerXchange = 0 

    playerX += playerXchange 
    enemyX += enemyX_change 
    if playerX <= -30: 
        playerX = -30
    elif playerX >= 890:
        playerX = 890

    for i in range(num_of_enemy):
        if enemyY[i] > 550: 
            for j in range(num_of_enemy):
                enemyY[j] = 2000 
            gameover() 
            finish = True
            break
        enemyX[i] += enemyX_change[i] 
        if enemyX[i] <= 0: 
            enemyX_change[i] = random.randint(1, difficulty)  
            enemyY[i] += enemyY_change[i] 
        elif enemyX[i] >= 885: 
            enemyX_change[i] = random.randint(-difficulty, -1)  
            enemyY[i] += enemyY_change[i] 
        collision = collide(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision: 
            bulletY = 675 
            bullet_state = "готово" 
            Bah.play()
            scoreSum += 1
            gatcha = True
            enemyX[i] = random.randint(0, 885)
            enemyY[i] = random.randint(30, 180)
            enemyX_change[i] = 1
        if (scoreSum % 10 == 0) and gatcha == True: #
            difficulty += 1 
            anim_background += 1 
            speed += 0.4 
            bulletYchange += 0.8 
            gatcha = False 
        enemy(enemyX[i], enemyY[i], i) 


    if bulletY <= 0: 
        bulletY = 675 
        bullet_state = "готово" 
    if bullet_state == "залп": 
        fire_bullet(bulletX, bulletY) 
        bulletY -= bulletYchange 


    show_score(textX, textY) 
    player(playerX, playerY) 
    fps.tick(144) 
    pygame.display.update() 
