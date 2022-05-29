import pygame
import random
import math

pygame.init() #Инициализация библиотеки пайгейм

screen = pygame.display.set_mode((1000, 800)) #Создание экрана
background = pygame.image.load('Resources/Background.png') #Загружаем картинку задника
Player = pygame.transform.scale(pygame.image.load('Resources/Player.png'), (150, 150)) #Загрузка текстуры игрока
Bullet = pygame.transform.scale(pygame.image.load('Resources/Bullet.png'), (50, 50)) #Загрузка текстуры залпа
Piy = pygame.mixer.Sound('Resources/Sound_laser.ogg')
Piy.set_volume(0.5)
Bah = pygame.mixer.Sound('Resources/Sound_bah.ogg')
Bah.set_volume(0.1)
#Music = pygame.mixer.Sound('Resources/Music.mp3')
#Music.set_volume(0.6)
pygame.mixer.music.load('Resources/Music.mp3')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.6)
font = pygame.font.Font('Resources/font.ttf', 32) #Шрифт для счета в углу
gameover_font = pygame.font.Font('Resources/font.ttf', 94) #Шрифт для надписи в конце
score_font = pygame.font.Font('Resources/font.ttf', 64) #Шрифт для финального счета

pygame.display.set_caption("The Little defender of Space") #Название игры
pygame.display.set_icon(pygame.image.load('Resources/Icon.bmp')) #Иконка окна


playerX, playerY = 450, 650 #Позиция игрока по X и Y
playerXchange = 0 #Смещение по X (для реализации движения)
enemyDisplay = [] #Массив изображения противника
enemyX, enemyY = [], [] #Массив координат противников
enemyX_change, enemyY_change = [], [] #Массив смещение координат противников
num_of_enemy = 20 #Количество противников
bulletX, bulletY = 0, 675 #Координата по X и Y
bulletXchange, bulletYchange = 0, 8 #Смещение
bullet_state = "готово" #Флаг проверки
textX, textY = 10, 10 #Координаты появления текста
score, scoreSum  = 0, 0 #Счетчик очков и финальная сумма
anim_background = -280
finish = False #Еще один флаг проверки
gatcha = True
difficulty = 3
speed = 2

for i in range(num_of_enemy): #Добавление противников в массив
    enemyDisplay.append(pygame.transform.scale(pygame.image.load('Resources/Enemy.png'), (120, 120))) #Добавление в массив картинку противника

    enemyX.append(random.randint(0, 885))  #Добавление координаты появление противника в массив
    enemyY.append(random.randint(30, 180)) #Добавление координаты появление противника в массив
    enemyX_change.append(1) #Добавление смещение по X в массив
    enemyY_change.append(20) #Добавление смещение по Y в массив

def calculation():
    global player, enemy, fire_bullet, show_score, gameover, collide

    def player(playerX, playerY):
        if finish == False:
            screen.blit(Player, (playerX, playerY))  # Отображение игрока
    def enemy(enemyX, enemyY, i):
        screen.blit(enemyDisplay[i], (enemyX, enemyY))  # Показ противников
    def fire_bullet(x, y):  # Отрисовка пули
        global bullet_state
        bullet_state = "залп" #Изменение флага
        screen.blit(Bullet, (x + 16, y + 10)) #отрисовка заряда 1
        screen.blit(Bullet, (x + 76, y + 10)) #отрисовка заряда 2
    def show_score(x, y):
        score = font.render("Счет: " + str(scoreSum), True, (255, 255, 255))  # Показ счетчика
        if finish == False: #проверка на финиш
            screen.blit(score, (x, y))
    def gameover():
        screen.fill((0,0,0)) #Заполнение черным
        score = score_font.render("Счет: " + str(scoreSum), True, (255, 255, 255)) # отображение счета
        gameover_text = gameover_font.render("КОНЕЦ ИГРЫ", True, (255, 255, 255))  # Экран конца игры
        screen.blit(gameover_text, (280, 300)) # Отображение
        screen.blit(score, (390, 400)) # Отображение
        pygame.mixer.music.pause()
    def collide(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt(math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)) #Просчет попадания
        if distance <= 52:
            return True
        else:
            return False

calculation()
main_cycle = True #Бегунок
while main_cycle:
    fps = pygame.time.Clock()
    #Music.play()
    screen.fill((0, 0, 0)) #Заполнение черным
    screen.blit(background, (-400, anim_background)) #Размещение задника
    for event in pygame.event.get(): #Пока очередь
        if event.type == pygame.QUIT: #Если игра закрывается
            main_cycle = False #Выход из цикла

        if event.type == pygame.KEYDOWN and finish == False: #Если нажата кнопка
            if event.key == pygame.K_d: #Если нажата кнопка вправо
                playerXchange += speed #Прибовление скорости смещение
            if event.key == pygame.K_a: #Если нажата кнопка влево
                playerXchange -= speed #Снижение скорости смещение
            if event.key == pygame.K_SPACE: #Если нажата кнопка пробел
                if bullet_state == "готово": #Проеврка на флаг выстрела
                    Piy.play()
                    bulletX = playerX #Берется координата игрока
                    fire_bullet(bulletX, bulletY) #Запуск снаряда
        if event.type == pygame.KEYUP: #Если кнопка отпущена
            if event.key == pygame.K_a or event.key == pygame.K_d: #Если отпущены a или d
                playerXchange = 0 #обнуление

    playerX += playerXchange #Смещение игрока по числу
    enemyX += enemyX_change #Смещение противника
    if playerX <= -30: #Ограничители игрового пространства
        playerX = -30
    elif playerX >= 890: #Ограничители игрового пространства
        playerX = 890

    for i in range(num_of_enemy):
        if enemyY[i] > 550: #Если координата проивника достигла значения
            for j in range(num_of_enemy):
                enemyY[j] = 2000 #Телепорт за границу экрана
            gameover() #Запуск функции конца игры
            finish = True
            break
        enemyX[i] += enemyX_change[i] #Смещение противника
        if enemyX[i] <= 0: #Проверка на контакт с границей экрана
            enemyX_change[i] = random.randint(1, difficulty)  # Присвоение смещению значение
            enemyY[i] += enemyY_change[i] #Смещение по Y
        elif enemyX[i] >= 885: #Проверка на контакт с границей экрана
            enemyX_change[i] = random.randint(-difficulty, -1)  # Присвоение смещению значение
            enemyY[i] += enemyY_change[i] #Смещение по Y
        collision = collide(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision: #Если расчет возвращает правду
            bulletY = 675 #Снаряд перемещается на координату
            bullet_state = "готово" #Меняется флаг
            Bah.play()
            scoreSum += 1 #Прибавляется счет
            gatcha = True
            enemyX[i] = random.randint(0, 885) #Записывается в массив информация о перемещении врага
            enemyY[i] = random.randint(30, 180)
            enemyX_change[i] = 1
        if (scoreSum % 10 == 0) and gatcha == True: #
            difficulty += 1 #Ускорение противника
            anim_background += 1 #Движение заднего фона
            speed += 0.4 #Ускорение игрока
            bulletYchange += 0.8 #Ускорение снаряда
            gatcha = False #смена флага
        enemy(enemyX[i], enemyY[i], i) #Создается враг


    if bulletY <= 0: #Если заряд улетает выше нуля
        bulletY = 675 #Перемащается на координату
        bullet_state = "готово" #Флаг меняется
    if bullet_state == "залп": #Если заряд выстрелен
        fire_bullet(bulletX, bulletY) #Вызывается функция залпа
        bulletY -= bulletYchange #Начинается смещение


    show_score(textX, textY) #Отображение счета
    player(playerX, playerY) #Отображение игрока
    fps.tick(144) #Огранечение кадров
    pygame.display.update() #Обновление кадра
