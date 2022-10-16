import random
import time

import pygame
from pygame import mixer

pygame.init()  # Init pygame(khởi tạo tất cả các module cần thiết cho PyGame)
# Đặt fps
FPS = 60
fpsClock = pygame.time.Clock()

# Các đường dẫn
linkBackGround = './data/background 1.jpg'  # Đường dẫn ảnh background
linkLogo = './data/space_invaders_logo.png'  # Đường dẫn ảnh logo
linkEnemy = './data/ship/enemy.png'  # Đường dẫn ảnh Enemy
linkPlane = './data/ship/player.png'  # Đường dẫn ảnh Player's plane
linkPlayerBullet = './data/bullet/bullet.png'  # Đường dẫn ảnh
linkLeftBullet = './data/bullet/bullet left.png'
linkRightBullet = './data/bullet/bullet right.png'
linkSemicircularBullet = './data/bullet/semicircular bullet 0.png'
linkSemicircularBullet1 = './data/bullet/semicircular bullet 1.png'
linkSemicircularBullet2 = './data/bullet/semicircular bullet 2.png'
linkEnemyBullet_default = './data/bullet/enemy bullet.png'
linkExplode = ['./data/explode 5.png',
               './data/explode 6.png',
               './data/explode 7.png',
               './data/explode 1.png',
               './data/explode 4.png']  # Đường dẫn ảnh vụ nổ

linkBLUE_LASER = './data/bullet/BLUE_LASER.png'
linkGREEN_LASER = './data/bullet/GREEN_LASER.png'
linkRED_LASER = './data/bullet/RED_LASER.png'
linkBLUE_SPACE_SHIP = './data/ship/BLUE_SPACE_SHIP.png'
linkGREEN_SPACE_SHIP = './data/ship/GREEN_SPACE_SHIP.png'
linkRED_SPACE_SHIP = './data/ship/RED_SPACE_SHIP.png'

# âm thanh
musicBullet = mixer.Sound('./data/sound/laser.wav')
musicBackground = mixer.Sound('./data/sound/Victory.mp3')
musicBackground.set_volume(0.5)
musicMenu = mixer.Sound('./data/sound/musicmenu.wav')
musicMenu.set_volume(0.3)
musicEnd = mixer.Sound('./data/sound/musicend.mp3')
explodeSound = mixer.Sound('./data/sound/boom.wav')
congratulationsSound = mixer.Sound('./data/sound/congratulations.wav')

player_ship = pygame.image.load(linkPlane)
player_laser = pygame.image.load(linkPlayerBullet)
player_left_laser = pygame.image.load(linkLeftBullet)
player_right_laser = pygame.image.load(linkRightBullet)
player_semicircular_laser = pygame.image.load(linkSemicircularBullet)
player_semicircular_laser1 = pygame.image.load(linkSemicircularBullet1)
player_semicircular_laser2 = pygame.image.load(linkSemicircularBullet2)
enemy_ship = pygame.image.load(linkEnemy)
enemy_laser = pygame.image.load(linkEnemyBullet_default)

BLUE_LASER = pygame.image.load(linkBLUE_LASER)
GREEN_LASER = pygame.image.load(linkGREEN_LASER)
RED_LASER = pygame.image.load(linkRED_LASER)
BLUE_SPACE_SHIP = pygame.image.load(linkBLUE_SPACE_SHIP)
GREEN_SPACE_SHIP = pygame.image.load(linkGREEN_SPACE_SHIP)
RED_SPACE_SHIP = pygame.image.load(linkRED_SPACE_SHIP)

xScreen, yScreen = 627, 705  # Screen create
VPlayer = 8  # Tốc độ Planes
VEnemy = 2  # Tốc độ Enemy
VBulletEnemy = 10
scores = 0  # Điểm số
level = 0
coins = 0
listEnemy = []
wave_length = 5
lives = 5
lost = False
semicircular_id = 0

screen = pygame.display.set_mode((xScreen, yScreen))
pygame.display.set_caption("Group 15 - Space Invaders")
background = pygame.transform.scale(pygame.image.load(linkBackGround), (xScreen, yScreen))
logo_img = pygame.image.load(linkLogo)

explode_img = []
for item in linkExplode:
    explode_img.append(pygame.transform.scale(pygame.image.load(item), (60, 60)))

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.SysFont("comicsanms", 32)
# Menu
button_1_x = xScreen / 2 - 100
button_1_y = yScreen / 2 - 25
button_2_x = xScreen / 2 - 100
button_2_y = yScreen / 2 + 75
button_3_x = xScreen / 2 - 100
button_3_y = yScreen / 2 + 175
button_continue_x = xScreen / 2 - 100
button_continue_y = yScreen - 60
button_1 = pygame.Rect(button_1_x, button_1_y, 200, 50)
button_2 = pygame.Rect(button_2_x, button_2_y, 200, 50)
button_3 = pygame.Rect(button_3_x, button_3_y, 200, 50)
button_continue = pygame.Rect(button_continue_x, button_continue_y, 200, 50)
paused = False
gameRunning = False
tutor_run = False
hs_run = False
yes_box = False
no_box = False
gameContinue = False

# Tutorial
WASD_key = pygame.image.load('./data/tutorial/WASD - quality.png')
Arrow_key = pygame.image.load('./data/tutorial/Arrow - quality.png')
Esc_key = pygame.image.load('./data/tutorial/Esc - quality.png')
Space_key = pygame.image.load('./data/tutorial/Space - quality.png')
Exit_key = pygame.image.load('./data/tutorial/Exit - quality.png')


class Laser:
    def __init__(self, img, x, y, width=25, height=60):
        self.x = x
        self.y = y
        self.y_start = y
        self.img = pygame.transform.scale(img, (width, height))  # change size image
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def moveClusterLeft(self, vel):  # di chuyển đạn chùm bên trái
        self.y += vel
        self.x += int(vel / 2)

    def moveClusterRight(self, vel):  # di chuyển đạn chùm bên phải
        self.y += vel
        self.x -= int(vel / 2)

    def off_screen(self, height):
        return self.y > height or self.y < -80

    def collision(self, obj):
        return collide(self, obj)


class Explode:
    def __init__(self):
        self.explode_image = explode_img[0]
        if player.straight:
            self.explode_image = explode_img[2]
        if player.cluster:
            self.explode_image = explode_img[1]
        if player.semicircular:
            self.explode_image = explode_img[3]

    def boom(self, x, y):
        # hiệu ứng tiếng nổ
        mixer.Sound(explodeSound).set_volume(0.1)
        mixer.Channel(2).play(mixer.Sound(explodeSound))

        # hiển thị vụ nổ
        screen.blit(self.explode_image, (x, y))
        pygame.display.flip()
        pygame.event.pump()
        pygame.time.delay(20)


class Ship:

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.width = None
        self.height = None
        self.health = health
        self.shootSpeed = 2
        self.COOLDOWN = FPS / self.shootSpeed
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.dame = None
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw()

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(yScreen):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= self.dame
                if obj.health == 0:
                    # cho obj phát nổ
                    crash = Explode()
                    crash.boom(obj.x, obj.y)
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            soundBullet = mixer.Sound(musicBullet)
            soundBullet.set_volume(0.5)
            mixer.Channel(1).play(soundBullet)
            laser = Laser(self.laser_img, self.x + int(self.get_width() / 2) - 12, self.y - 30, 25, 60)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, width, height, health=100):
        super().__init__(x, y, health)
        self.ship_img = pygame.transform.scale(player_ship, (width, height))  # change size image
        self.laser_img = player_laser
        self.left_laser_img = pygame.transform.scale(player_left_laser, (25, 60))
        self.right_laser_img = pygame.transform.scale(player_right_laser, (25, 60))
        self.semicircular_laser_img = player_semicircular_laser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.straight = False
        self.cluster = False
        self.semicircular = False
        self.straightLasers = []
        self.leftLasers = []
        self.rightLasers = []
        self.semicircularLasers = []
        self.max_health = health
        self.bloodSteal = 0
        self.continuous = 1
        self.dame = 100
        self.bullet_speed = 5

    def move_lasers(self, vel, objs):
        global scores
        global coins
        self.cooldown()
        for laser in self.lasers:  # di chuyển đạn trong lasers
            laser.move(vel)
            if laser.off_screen(yScreen):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.health -= self.dame
                        if obj.health <= 0:
                            # cho obj phát nổ
                            crash = Explode()
                            crash.boom(obj.x, obj.y)
                            objs.remove(obj)
                            scores += 100
                            coins += obj.coin
                            if self.health + self.bloodSteal < self.max_health:
                                self.health += self.bloodSteal
                            else:
                                self.health = self.max_health
                        if laser in self.lasers:
                            self.lasers.remove(laser)
        for laser in self.straightLasers:  # di chuyển đạn trong straightLasers
            laser.move(vel)
            if laser.off_screen(yScreen):
                self.straightLasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.health -= self.dame
                        if obj.health <= 0:
                            # cho obj phát nổ
                            crash = Explode()
                            crash.boom(obj.x, obj.y)
                            objs.remove(obj)
                            scores += 100
                            coins += obj.coin
                            if self.health + self.bloodSteal < self.max_health:
                                self.health += self.bloodSteal
                            else:
                                self.health = self.max_health
                        if laser in self.straightLasers:
                            self.straightLasers.remove(laser)
        for laser in self.semicircularLasers:  # di chuyển đạn trong semicircularLasers
            laser.move(vel)
            if laser.off_screen(yScreen):
                self.semicircularLasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.health -= self.dame
                        if obj.health <= 0:
                            # cho obj phát nổ
                            crash = Explode()
                            crash.boom(obj.x, obj.y)
                            objs.remove(obj)
                            scores += 100
                            coins += obj.coin
                            if self.health + self.bloodSteal < self.max_health:
                                self.health += self.bloodSteal
                            else:
                                self.health = self.max_health
        for laser in self.leftLasers:  # di chuyển đạn trong leftLasers
            laser.moveClusterLeft(vel)
            if laser.off_screen(yScreen):
                self.leftLasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.health -= self.dame
                        if obj.health <= 0:
                            # cho obj phát nổ
                            crash = Explode()
                            crash.boom(obj.x, obj.y)
                            objs.remove(obj)
                            scores += 100
                            coins += obj.coin
                            if self.health + self.bloodSteal < self.max_health:
                                self.health += self.bloodSteal
                            else:
                                self.health = self.max_health
                        if laser in self.leftLasers:
                            self.leftLasers.remove(laser)
        for laser in self.rightLasers:  # di chuyển đạn trong rightLasers
            laser.moveClusterRight(vel)
            if laser.off_screen(yScreen):
                self.rightLasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.health -= self.dame
                        if obj.health <= 0:
                            # cho obj phát nổ
                            crash = Explode()
                            crash.boom(obj.x, obj.y)
                            objs.remove(obj)
                            scores += 100
                            coins += obj.coin
                            if self.health + self.bloodSteal < self.max_health:
                                self.health += self.bloodSteal
                            else:
                                self.health = self.max_health
                        if laser in self.rightLasers:
                            self.rightLasers.remove(laser)

    def clusterShoot(self):  # bắn đạn chùm
        for i in range(0, self.continuous):
            leftLaser = Laser(self.left_laser_img, self.x + int(self.get_width() / 2) - 18 - i * 14,
                              self.y - 30 - i * 20, 30,
                              40)
            rightLaser = Laser(self.right_laser_img, self.x + int(self.get_width() / 2) - 18 + i * 14,
                               self.y - 30 - i * 20, 30,
                               40)
            self.leftLasers.append(leftLaser)
            self.rightLasers.append(rightLaser)

    def straightShoot(self):  # bắn đạn đôi
        for i in range(0, self.continuous):
            laser = Laser(self.laser_img, self.x + int(self.get_width() / 2) - 17, self.y - 30 - i * 50, 25, 60)
            self.lasers.append(laser)
            laser = Laser(self.laser_img, self.x + int(self.get_width() / 2) - 5, self.y - 30 - i * 50, 25, 60)
            self.straightLasers.append(laser)

    def semicularShoot(self):  # bắn đạn bán nguyệt
        if semicircular_id == 1:
            laser = Laser(self.semicircular_laser_img, self.x - 10, self.y - 30, 100, 67)
        elif semicircular_id == 2:
            laser = Laser(player_semicircular_laser1, self.x - 60, self.y - 30, 200, 133)
        elif semicircular_id == 3:
            laser = Laser(player_semicircular_laser2, self.x - 110, self.y - 50, 300, 200)
        self.semicircularLasers.append(laser)

    def shoot(self):
        if self.cool_down_counter == 0:
            soundBullet = mixer.Sound(musicBullet)
            soundBullet.set_volume(0.2)
            mixer.Channel(1).play(soundBullet)
            if not self.straight and not self.semicircular:
                for i in range(0, self.continuous):
                    laser = Laser(self.laser_img, self.x + int(self.get_width() / 2) - 12, self.y - 30 - i * 50, 25, 60)
                    self.lasers.append(laser)
            elif not self.semicircular:
                self.straightShoot()
            if self.cluster and not self.semicircular:
                self.clusterShoot()
            if self.semicircular:
                self.semicularShoot()
            self.cool_down_counter = 1

    def draw(self, window):
        super().draw(window)
        if self.cluster:
            self.drawCluster()
        if self.straight:
            self.drawStraight()
        if self.semicircular:
            self.drawSemicircular()
        self.healthbar(window)
        font = pygame.font.SysFont("comicsansms", 12)
        text = font.render(str(self.health), True, (255, 0, 0))
        screen.blit(text, (
            self.x + self.ship_img.get_width() / 2 - text.get_width() / 2, self.y + self.ship_img.get_height() + 6))

    def drawStraight(self):
        for laser in self.straightLasers:
            laser.draw()

    def drawCluster(self):
        for laser in self.leftLasers:
            laser.draw()
        for laser in self.rightLasers:
            laser.draw()

    def drawSemicircular(self):
        for laser in self.semicircularLasers:
            laser.draw()

    def healthbar(self, window):
        pygame.draw.rect(window, (0, 0, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 12))
        pygame.draw.rect(window, (0, 255, 0), (
            self.x, self.y + self.ship_img.get_height() + 10,
            self.ship_img.get_width() * (self.health / self.max_health),
            12))


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
        "default": (enemy_ship, enemy_laser)
    }

    def __init__(self, x, y, color, width, height, vel):
        super().__init__(x, y,
                         health=(100 + (level - 1) * 100 if not player.semicircular else 100 + (level - 1) * 2000))
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.ship_img = pygame.transform.scale(self.ship_img, (width, height))
        self.max_health = 100 + (level - 1) * 100 if not player.semicircular else 100 + (level - 1) * 2000
        self.laser_vel = vel
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.dame = 10 + (level - 1) * 5
        self.coin = 10 + (level - 1) * 20
        self.direction = random.choice((True, False))
        if color == 'red':
            self.max_health = 100 + (level - 1) * 250 if not player.semicircular else 100 + (level - 1) * 2000
            self.health = 100 + (level - 1) * 250 if not player.semicircular else 100 + (level - 1) * 2000
            self.coin = 40 + (level - 1) * 20
        if color == 'blue':
            self.max_health = 100 + (level - 1) * 200 if not player.semicircular else 100 + (level - 1) * 2000
            self.health = 100 + (level - 1) * 200 if not player.semicircular else 100 + (level - 1) * 2000
            self.coin = 30 + (level - 1) * 20
        if color == 'green':
            self.max_health = 100 + (level - 1) * 150 if not player.semicircular else 100 + (level - 1) * 2000
            self.health = 100 + (level - 1) * 150 if not player.semicircular else 100 + (level - 1) * 2000
            self.coin = 20 + (level - 1) * 20

    def move(self, vel):
        if self.x < 0 or self.x > xScreen - self.get_width():
            self.direction = not self.direction
        self.x = self.x + (- vel if self.direction else vel)
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.laser_img, self.x + int(self.get_width() / 2) - 5, self.y + self.get_height() - 12, 10,
                          30)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
        font = pygame.font.SysFont("comicsansms", 12)
        text = font.render(str(self.health), True, (0, 102, 0))
        screen.blit(text, (
            self.x + self.ship_img.get_width() / 2 - text.get_width() / 2, self.y - 3))

    def healthbar(self, window):
        pygame.draw.rect(window, (0, 0, 0),
                         (self.x, self.y, self.ship_img.get_width(), 12))
        pygame.draw.rect(window, (255, 0, 0), (
            self.x, self.y, self.ship_img.get_width() * (self.health / self.max_health), 12))


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def update(self):
        # Thay đổi kích thước hộp nếu văn bản quá dài.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


def store_highscore_in_file(list, fn="./data/highscores.txt", top_n=0):
    """Lưu danh sách điểm cao vào file highscores.txt, chỉ lưu top_n điểm cao nhất"""
    with open(fn, "w") as f:
        for idx, (name, pts) in enumerate(sorted(list, key=lambda x: x[1], reverse=True)):
            f.write(f"{name}, {pts}\n")
            if top_n and idx == top_n - 1:
                break


def load_highscore_from_file(fn="./data/highscores.txt"):
    """Lấy danh sách từ file ra"""
    hs = []
    try:
        with open(fn, "r") as f:
            for line in f:
                name, _, points = line.partition(",")
                if name and points:
                    hs.append((str(name), int(points)))
    except FileNotFoundError:
        return []
    return hs


def show_texts(x, y, texts, size):  # In chữ
    font = pygame.font.SysFont("comicsansms", size)
    text = font.render(str(texts), True, (255, 255, 255))
    screen.blit(text, (x, y))


def show_texts_middle(y, texts, size):  # In chữ ở giữa
    font = pygame.font.SysFont("comicsansms", size)
    text = font.render(str(texts), True, (255, 255, 255))
    screen.blit(text, (xScreen / 2 - text.get_width() / 2, y))


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def show_text_menu(x, y, text, size):  # x,y là toạ độ tâm của hcn chứa text
    font = pygame.font.SysFont("comicsansms", size)
    text = font.render(text, True, (255, 255, 0))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


prohibit = False


def show_text_prohibit(x, y, text, size):  # x,y là toạ độ tâm của hcn chứa text
    font = pygame.font.SysFont("comicsansms", size)
    text = font.render(text, True, (255, 0, 0))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


player = Player(280, 600, 80, 80)


def main_menu():
    global gameRunning
    global gameContinue
    global hs_run
    global tutor_run
    menu_run = True
    if not gameContinue:
        musicMenu.play(10000)
    while menu_run:
        screen.blit(background, (0, 0))
        screen.blit(logo_img, (0, 0))

        pygame.draw.rect(screen, (0, 0, 0), button_1)
        pygame.draw.rect(screen, (0, 0, 0), button_2)
        pygame.draw.rect(screen, (0, 0, 0), button_3)
        if gameContinue:
            show_text_menu(xScreen / 2, button_1_y + (button_1.height / 2), "Continue", 25)
        else:
            show_text_menu(xScreen / 2, button_1_y + (button_1.height / 2), "Start", 25)
        show_text_menu(xScreen / 2, button_2_y + (button_2.height / 2), "High scores", 25)
        show_text_menu(xScreen / 2, button_3_y + (button_3.height / 2), "Tutorial", 25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    if button_1.collidepoint((mx, my)):
                        gameRunning = True
                        mixer.stop()
                        run()
                        continue
                    if button_2.collidepoint((mx, my)):
                        hs_run = True
                        highScores()
                        continue
                    if button_3.collidepoint((mx, my)):
                        tutor_run = True
                        tutorial()
                        continue
        pygame.display.update()  # Update
    pygame.display.update()  # Update
    # Khởi tạo màn hình


def run():
    global gameRunning
    global gameContinue
    global paused
    global scores
    global level
    global coins
    global player
    global semicircular_id
    global bloodSteal_coin
    global hpUp_coin
    global heal_coin
    global dameUp_coin
    global shootSpeedUp_coin
    global bulletSpeedUp_coin
    global straightLaser_coin
    global clusterLaser_coin
    global semicircularLaser_coin
    global continuousShooting_coin
    global listEnemy
    global wave_length
    global level
    global lives
    global coins
    global lost

    musicBackground.play(10000)
    i = 0
    while gameRunning:
        fpsClock.tick(FPS)
        screen.blit(background, [0, i])  # tạo cuộn dọc(nền chuyển động)
        screen.blit(background, [0, -yScreen + i])
        if i == yScreen:
            i = 0
        i += 1
        show_texts(10, 10, f"Scores: {scores}", 30)
        show_texts(10, 50, f"Lives: {lives}", 30)
        show_texts(xScreen - 180, 10, f"Level: {level}", 30)
        show_texts(xScreen - 180, 40, f"Coins: {coins}", 30)
        show_texts(xScreen - 180, 70, f"Enemies left:{len(listEnemy)}", 20)
        for enemy in listEnemy:
            enemy.draw(screen)

        player.draw(screen)
        pygame.display.update()  # Update

        if lives <= 0 or player.health <= 0:
            lost = True

        if len(listEnemy) == 0:
            lives = 5
            level += 1
            wave_length += 1
            show_texts_middle(yScreen / 2 - 100, f"Level: {level}", 100)
            pygame.display.update()
            time.sleep(0.7)
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, xScreen - 100), random.randrange(-1500, -100),
                              random.choice(list(Enemy.COLOR_MAP)), 80, 80, VBulletEnemy)
                listEnemy.append(enemy)

        for event in pygame.event.get():  # Bắt các sự kiện
            if event.type == pygame.QUIT:  # sự kiện nhấn thoát
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:  # sự kiện có phím nhấn xuống
                if event.key == pygame.K_ESCAPE:
                    paused = True
                    pause()
                    continue

        keys = pygame.key.get_pressed()  # sự kiện đè phím
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.x - VPlayer > 0:
            player.x -= VPlayer
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.x + VPlayer + player.get_width() < xScreen:
            player.x += VPlayer
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and player.y - VPlayer > 0:
            player.y -= VPlayer
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player.y + VPlayer + player.get_height() < yScreen - 20:
            player.y += VPlayer
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in listEnemy[:]:  # Địch di chuyển và bắn
            enemy.move(VEnemy)
            enemy.move_lasers(enemy.laser_vel, player)

            if random.randrange(0, 2 * FPS) == 1:  # bắn ngẫu nhiên 1 lần trong mỗi 2s
                enemy.shoot()

            if collide(enemy, player):  # xử lý khi va chạm với địch
                player.health -= enemy.dame
                # cho obj phát nổ
                crash = Explode()
                crash.boom(enemy.x, enemy.y)
                listEnemy.remove(enemy)
            elif enemy.y + enemy.get_height() > yScreen:
                lives -= 1
                listEnemy.remove(enemy)

        player.move_lasers(-player.bullet_speed, listEnemy)

        if lost:  # Nếu thua
            hs = load_highscore_from_file()
            newGame = False
            mixer.stop()
            if len(hs) == 0 or hs[len(hs) - 1][1] < scores:
                congratulationsSound.play()
            else:
                musicEnd.play(10000)
            while True:
                for event in pygame.event.get():  # Nếu nhấn
                    if event.type == pygame.QUIT:  # Thoát
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        gameRunning = False
                        mixer.stop()
                global yes_box
                global no_box
                input_box = InputBox(200, yScreen / 2 + 100, 200, 32)
                if (len(hs) < 10 or hs[len(hs) - 1][1] < scores) and not yes_box and not no_box:
                    screen.blit(background, (0, 0))  # vẽ lại background
                    show_texts_middle(yScreen / 2 - 150, f"Scores:{scores}", 60)  # In điểm
                    show_texts_middle(yScreen / 2 - 70, "Congratulations! You are in top high scores!", 30)
                    show_texts_middle(100, "GAME OVER", 70)  # In Thông báo thua
                    show_texts_middle(yScreen / 2, "Do you want to save your scores?", 30)
                    button_yes = pygame.Rect((xScreen / 2 - 150, yScreen / 2 + 100, 120, 50))
                    button_no = pygame.Rect((xScreen / 2 + 30, yScreen / 2 + 100, 120, 50))
                    pygame.draw.rect(screen, (51, 153, 255), button_yes)
                    pygame.draw.rect(screen, (255, 77, 77), button_no)
                    show_text_menu(xScreen / 2 - 90, yScreen / 2 + 100 + 25, "Yes", 25)
                    show_text_menu(xScreen / 2 + 90, yScreen / 2 + 100 + 25, "No", 25)
                    for event in pygame.event.get():  # Nếu nhấn
                        if event.type == pygame.QUIT:  # Thoát
                            pygame.quit()
                            quit()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            gameRunning = False
                            mixer.stop()
                            break
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                mx, my = pygame.mouse.get_pos()
                                if button_yes.collidepoint((mx, my)):  # Nếu người dùng nhấp chuột vào hộp yes
                                    yes_box = True
                                    break
                                if button_no.collidepoint((mx, my)):  # Nếu người dùng nhấp chuột vào hộp no
                                    no_box = True
                                    break
                elif yes_box:
                    done = False
                    while not done:
                        screen.blit(background, (0, 0))  # vẽ lại background
                        show_texts_middle(yScreen / 2 - 150, f"Scores:{scores}", 60)
                        show_texts_middle(yScreen / 2 - 70, "Congratulations! You are in top high scores!", 30)
                        show_texts_middle(100, "GAME OVER", 70)
                        show_texts_middle(yScreen / 2, "Please enter your name", 40)
                        input_box.draw(screen)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:  # Thoát
                                pygame.quit()
                                quit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                # Nếu người dùng nhấp chuột vào hộp input_box.
                                if input_box.rect.collidepoint(event.pos):
                                    input_box.active = not input_box.active
                                else:
                                    input_box.active = False
                                # Đổi màu của hộp input box.
                                input_box.color = COLOR_ACTIVE if input_box.active else COLOR_INACTIVE
                            if event.type == pygame.KEYDOWN:
                                if input_box.active:
                                    if event.key == pygame.K_RETURN:
                                        hs.append((str(input_box.text), scores))
                                        store_highscore_in_file(hs, top_n=10)
                                        done = True
                                        gameRunning = False
                                        mixer.stop()
                                        break
                                    elif event.key == pygame.K_BACKSPACE:
                                        input_box.text = input_box.text[:-1]
                                    elif event.key == pygame.K_SPACE:
                                        input_box.text += " "
                                    else:
                                        input_box.text += event.unicode
                                    # render lại văn bản
                                    input_box.txt_surface = FONT.render(input_box.text, True, input_box.color)

                                if event.key == pygame.K_ESCAPE:
                                    done = True
                                    gameRunning = False
                                    mixer.stop()
                                    break
                        input_box.update()
                        pygame.display.update()
                elif no_box:
                    screen.blit(background, (0, 0))  # vẽ lại background
                    show_texts_middle(yScreen / 2 - 150, f"Scores:{scores}", 60)
                    show_texts_middle(yScreen / 2 - 70, "Congratulations! You are in top high scores!", 30)
                    show_texts_middle(100, "GAME OVER", 70)
                    show_texts_middle(yScreen / 2, "Press Space to play again", 40)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:  # Thoát
                            pygame.quit()
                            quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                newGame = True
                                mixer.stop()
                                musicBackground.play(10000)
                                break
                            if event.key == pygame.K_ESCAPE:
                                gameRunning = False
                                mixer.stop()
                                break
                else:
                    screen.blit(background, (0, 0))  # vẽ lại background
                    show_texts_middle(yScreen / 2 - 170, f"Scores:{scores}", 60)
                    show_texts_middle(100, "GAME OVER", 70)
                    show_texts_middle(yScreen / 2, "Press Space to play again", 40)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:  # Thoát
                            pygame.quit()
                            quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                newGame = True
                                mixer.stop()
                                musicBackground.play(10000)
                                break
                            if event.key == pygame.K_ESCAPE:
                                gameRunning = False
                                mixer.stop()
                                break
                pygame.display.update()
                if newGame or not gameRunning:  # Thoát vòng while để vào game mới
                    break

            scores = 0  # Trả các biến về giá trị ban đầu
            listEnemy = []
            wave_length = 5
            level = 0
            lives = 5
            coins = 0
            semicircular_id = 0
            lost = False
            yes_box = False
            no_box = False
            gameContinue = False
            player = Player(280, 600, 80, 80)
            bloodSteal_coin = 50
            hpUp_coin = 50
            heal_coin = 50
            dameUp_coin = 50
            shootSpeedUp_coin = 50
            bulletSpeedUp_coin = 50
            straightLaser_coin = 5000
            clusterLaser_coin = 5000
            semicircularLaser_coin = 10000
            continuousShooting_coin = 10000
    if not gameContinue:
        musicMenu.play(10000)


button_bloodSteal_x = 375
button_bloodSteal_y = 100
button_hpUp_x = 50
button_hpUp_y = 200
button_heal_x = 50
button_heal_y = 100
button_dameUp_x = 50
button_dameUp_y = 300
button_shootSpeedUp_x = 375
button_shootSpeedUp_y = 200
button_bulletSpeedUp_x = 375
button_bulletSpeedUp_y = 300
button_straightLaser_x = 375
button_straightLaser_y = 500
button_clusterLaser_x = 375
button_clusterLaser_y = 400
button_semicircularLaser_x = 50
button_semicircularLaser_y = 500
button_continuousShooting_x = 50
button_continuousShooting_y = 400

button_bloodSteal = pygame.Rect(button_bloodSteal_x, button_bloodSteal_y, 200, 50)
button_hpUp = pygame.Rect(button_hpUp_x, button_hpUp_y, 200, 50)
button_heal = pygame.Rect(button_heal_x, button_heal_y, 200, 50)
button_dameUp = pygame.Rect(button_dameUp_x, button_dameUp_y, 200, 50)
button_shootSpeedUp = pygame.Rect(button_shootSpeedUp_x, button_shootSpeedUp_y, 200, 50)
button_bulletSpeedUp = pygame.Rect(button_bulletSpeedUp_x, button_bulletSpeedUp_y, 200, 50)
button_straightLaser = pygame.Rect(button_straightLaser_x, button_straightLaser_y, 200, 50)
button_clusterLaser = pygame.Rect(button_clusterLaser_x, button_clusterLaser_y, 200, 50)
button_semicircularLaser = pygame.Rect(button_semicircularLaser_x, button_semicircularLaser_y, 200, 50)
button_continuousShooting = pygame.Rect(button_continuousShooting_x, button_continuousShooting_y, 200, 50)

straight_activate = True
cluster_active = True
semicircularLaser_active = True

bloodSteal_coin = 50
hpUp_coin = 50
heal_coin = 50
dameUp_coin = 50
shootSpeedUp_coin = 50
bulletSpeedUp_coin = 50
straightLaser_coin = 0 #5000
clusterLaser_coin = 0 #5000
semicircularLaser_coin = 0#10000
continuousShooting_coin = 0#10000


def pause():  # store
    global paused
    global gameRunning
    global gameContinue
    global coins
    global player
    global semicircular_id
    global straight_activate
    global cluster_active
    global semicircularLaser_active
    global bloodSteal_coin
    global hpUp_coin
    global heal_coin
    global dameUp_coin
    global shootSpeedUp_coin
    global bulletSpeedUp_coin
    global straightLaser_coin
    global clusterLaser_coin
    global semicircularLaser_coin
    global continuousShooting_coin
    while paused:
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), button_continue)
        show_text_menu(xScreen / 2, button_continue_y + button_continue.height / 2, "Continue", 25)

        """Vẽ nút Blood steal"""
        pygame.draw.rect(screen, (0, 0, 0), button_bloodSteal)
        show_text_menu(button_bloodSteal_x + button_bloodSteal.width / 2,
                       button_bloodSteal_y + button_bloodSteal.height / 2, "Blood steal +", 25)
        show_texts(button_bloodSteal_x - 70, button_bloodSteal_y + button_bloodSteal.height,
                   f"Steal {player.bloodSteal + 10} hp each time killing an enemy", 18)
        show_texts(button_bloodSteal_x + 35, button_bloodSteal_y + button_bloodSteal.height + 25,
                   f"Cost: {bloodSteal_coin} coins", 18)

        """ Vẽ nút Hp up """
        pygame.draw.rect(screen, (0, 0, 0), button_hpUp)
        show_text_menu(button_hpUp_x + button_hpUp.width / 2, button_hpUp_y + button_hpUp.height / 2, "Hp +", 25)
        show_texts(button_hpUp_x, button_hpUp_y + button_hpUp.height, "Your plane's max hp + 100", 18)
        show_texts(button_hpUp_x + 35, button_hpUp_y + button_hpUp.height + 25, f"Cost: {hpUp_coin} coins", 18)

        """ Vẽ nút Heal """
        pygame.draw.rect(screen, (0, 0, 0), button_heal)
        show_text_menu(button_heal_x + button_heal.width / 2, button_heal_y + button_heal.height / 2, "Heal", 25)
        show_texts(button_heal_x - 10, button_heal_y + button_heal.height, "Heal half of your plane's hp", 18)
        show_texts(button_heal_x + 35, button_heal_y + button_heal.height + 25, f"Cost: {heal_coin} coins", 18)

        """ Vẽ nút Dame up """
        pygame.draw.rect(screen, (0, 0, 0), button_dameUp)
        show_text_menu(button_dameUp_x + button_dameUp.width / 2, button_dameUp_y + button_dameUp.height / 2,
                       "Dame +",
                       25)
        show_texts(button_dameUp_x, button_dameUp_y + button_dameUp.height, "Your plane's damage + 100", 18)
        show_texts(button_dameUp_x + 35, button_dameUp_y + button_dameUp.height + 25, f"Cost: {dameUp_coin} coins",
                   18)

        """ Vẽ nút Shoot speed up """
        pygame.draw.rect(screen, (0, 0, 0), button_shootSpeedUp)
        if player.shootSpeed + 1 == FPS:
            show_text_prohibit(button_shootSpeedUp_x + button_shootSpeedUp.width / 2,
                               button_shootSpeedUp_y + button_shootSpeedUp.height / 2, "Shoot speed MAX", 25)
        else:
            show_text_menu(button_shootSpeedUp_x + button_shootSpeedUp.width / 2,
                           button_shootSpeedUp_y + button_shootSpeedUp.height / 2, "Shoot speed +", 25)
        show_texts(button_shootSpeedUp_x - 40, button_shootSpeedUp_y + button_shootSpeedUp.height,
                   "Increase your plane's shoot speed", 18)
        show_texts(button_shootSpeedUp_x + 35, button_shootSpeedUp_y + button_shootSpeedUp.height + 25,
                   f"Cost: {shootSpeedUp_coin} coins", 18)

        """ Vẽ nút Bullet speed up """
        pygame.draw.rect(screen, (0, 0, 0), button_bulletSpeedUp)
        show_text_menu(button_bulletSpeedUp_x + button_bulletSpeedUp.width / 2,
                       button_bulletSpeedUp_y + button_bulletSpeedUp.height / 2, "Bullet speed +", 25)
        show_texts(button_bulletSpeedUp_x - 40, button_bulletSpeedUp_y + button_bulletSpeedUp.height,
                   "Increase your plane's bullet speed", 18)
        show_texts(button_bulletSpeedUp_x + 35, button_bulletSpeedUp_y + button_bulletSpeedUp.height + 25,
                   f"Cost: {bulletSpeedUp_coin} coins", 18)

        """ Vẽ nút Straight Laser """
        pygame.draw.rect(screen, (0, 0, 0), button_straightLaser)
        if straight_activate:
            show_text_menu(button_straightLaser_x + button_straightLaser.width / 2,
                           button_straightLaser_y + button_straightLaser.height / 2, "Straight Laser", 20)
        else:
            show_text_prohibit(button_straightLaser_x + button_straightLaser.width / 2,
                               button_straightLaser_y + button_straightLaser.height / 2, "Straight Laser", 20)
        show_texts(button_straightLaser_x, button_straightLaser_y + button_straightLaser.height,
                   "Fire one more straight laser", 18)
        show_texts(button_straightLaser_x + 35, button_straightLaser_y + button_straightLaser.height + 25,
                   f"Cost: {straightLaser_coin} coins", 18)

        """ Vẽ nút Cluster Laser """
        pygame.draw.rect(screen, (0, 0, 0), button_clusterLaser)
        if cluster_active:
            show_text_menu(button_clusterLaser_x + button_clusterLaser.width / 2,
                           button_clusterLaser_y + button_clusterLaser.height / 2, "Cluster Laser", 20)
        else:
            show_text_prohibit(button_clusterLaser_x + button_clusterLaser.width / 2,
                               button_clusterLaser_y + button_clusterLaser.height / 2, "Cluster Laser", 20)
        show_texts(button_clusterLaser_x - 80, button_clusterLaser_y + button_clusterLaser.height,
                   "Fire one more left laser and right laser", 18)
        show_texts(button_clusterLaser_x + 45, button_clusterLaser_y + button_clusterLaser.height + 25,
                   f"Cost: {clusterLaser_coin} coins", 18)

        """ Vẽ nút Semicircular Laser """
        pygame.draw.rect(screen, (0, 0, 0), button_semicircularLaser)
        if semicircularLaser_active:
            show_text_menu(button_semicircularLaser_x + button_semicircularLaser.width / 2,
                           button_semicircularLaser_y + button_semicircularLaser.height / 2,
                           f"Semicircular Laser NO.{semicircular_id}",
                           16)
        else:
            show_text_prohibit(button_semicircularLaser_x + button_semicircularLaser.width / 2,
                               button_semicircularLaser_y + button_semicircularLaser.height / 2,
                               "Semicircular Laser MAX",
                               16)
        if semicircular_id == 0:
            show_texts(button_semicircularLaser_x - 50, button_semicircularLaser_y + button_semicircularLaser.height,
                       "This laser is not disappear if collide enemy", 18)
        elif semicircular_id < 6:
            show_texts(button_semicircularLaser_x, button_semicircularLaser_y + button_semicircularLaser.height,
                       "Your laser become bigger", 18)
        else:
            show_texts(button_semicircularLaser_x - 50, button_semicircularLaser_y + button_semicircularLaser.height,
                       "You have unleashed all the power of this laser", 17)
        show_texts(button_semicircularLaser_x + 35,
                   button_semicircularLaser_y + button_semicircularLaser.height + 25,
                   f"Cost: {semicircularLaser_coin} coins", 18)

        """ Vẽ nút Continuous Shooting """
        pygame.draw.rect(screen, (0, 0, 0), button_continuousShooting)
        if semicircular_id == 0:
            show_text_menu(button_continuousShooting_x + button_continuousShooting.width / 2,
                           button_continuousShooting_y + button_continuousShooting.height / 2, "Continuous Shooting +1",
                           18)
        else:
            show_text_prohibit(button_continuousShooting_x + button_continuousShooting.width / 2,
                               button_continuousShooting_y + button_continuousShooting.height / 2,
                               "Continuous Shooting +1", 18)
        show_texts(button_continuousShooting_x + 25, button_continuousShooting_y + button_continuousShooting.height,
                   "Fire one more time", 18)
        show_texts(button_continuousShooting_x + 35,
                   button_continuousShooting_y + button_continuousShooting.height + 25,
                   f"Cost: {continuousShooting_coin} coins", 18)
        show_text_menu(xScreen / 2, 25, "Space Store", 30)
        show_texts(xScreen - 180, 40, f"Coins: {coins}", 30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = False
                gameRunning = False
                gameContinue = True
                continue
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    if button_continue.collidepoint((mx, my)):
                        paused = False
                        continue
                    if button_bloodSteal.collidepoint((mx, my)):
                        if coins >= bloodSteal_coin:
                            show_text_prohibit(button_bloodSteal_x + button_bloodSteal.width / 2,
                                               button_bloodSteal_y + button_bloodSteal.height / 2,
                                               "Blood steal +", 25)
                            coins -= bloodSteal_coin
                            bloodSteal_coin += 50
                            player.bloodSteal += 10
                        break
                    if button_heal.collidepoint((mx, my)):
                        if coins >= heal_coin:
                            show_text_prohibit(button_heal_x + button_heal.width / 2,
                                               button_heal_y + button_heal.height / 2,
                                               "Heal", 25)
                            coins -= heal_coin
                            heal_coin += 50
                            player.health += int(player.max_health / 2)
                        break
                    if button_hpUp.collidepoint((mx, my)):
                        if coins >= hpUp_coin:
                            show_text_prohibit(button_hpUp_x + button_hpUp.width / 2,
                                               button_hpUp_y + button_hpUp.height / 2, "Hp +", 25)
                            coins -= hpUp_coin
                            hpUp_coin += 50
                            player.max_health += 100
                            player.health += 100
                        break
                    if button_shootSpeedUp.collidepoint((mx, my)):
                        if coins >= shootSpeedUp_coin and player.shootSpeed + 1 < FPS:
                            show_text_prohibit(button_shootSpeedUp_x + button_shootSpeedUp.width / 2,
                                               button_shootSpeedUp_y + button_shootSpeedUp.height / 2, "Shoot speed +",
                                               25)
                            coins -= shootSpeedUp_coin
                            shootSpeedUp_coin += 50
                            player.shootSpeed += 2
                        break
                    if button_dameUp.collidepoint((mx, my)):
                        if coins >= dameUp_coin:
                            show_text_prohibit(button_dameUp_x + button_dameUp.width / 2,
                                               button_dameUp_y + button_dameUp.height / 2, "Dame +",
                                               25)
                            coins -= dameUp_coin
                            dameUp_coin += 50
                            player.dame += 100
                        break
                    if button_bulletSpeedUp.collidepoint((mx, my)):
                        if coins >= bulletSpeedUp_coin:
                            show_text_prohibit(button_bulletSpeedUp_x + button_bulletSpeedUp.width / 2,
                                               button_bulletSpeedUp_y + button_bulletSpeedUp.height / 2,
                                               "Bullet speed +",
                                               25)
                            coins -= bulletSpeedUp_coin
                            bulletSpeedUp_coin += 50
                            player.bullet_speed += 5
                        break
                    if button_clusterLaser.collidepoint((mx, my)) and cluster_active and semicircular_id == 0:
                        if coins >= clusterLaser_coin:
                            coins -= clusterLaser_coin
                            player.cluster = True
                            cluster_active = False
                        break
                    if button_straightLaser.collidepoint((mx, my)) and straight_activate and semicircular_id == 0:
                        if coins >= straightLaser_coin:
                            coins -= straightLaser_coin
                            player.straight = True
                            straight_activate = False
                        break
                    if button_semicircularLaser.collidepoint((mx, my)) and semicircularLaser_active:
                        if coins >= semicircularLaser_coin:
                            show_text_prohibit(button_semicircularLaser_x + button_semicircularLaser.width / 2,
                                               button_semicircularLaser_y + button_semicircularLaser.height / 2,
                                               f"Semicircular Laser NO.{semicircular_id}",
                                               16)
                            coins -= semicircularLaser_coin
                            semicircularLaser_coin += 10000
                            player.semicircular = True
                            player.cluster = False
                            player.straight = False
                            player.continuous = 1
                            cluster_active = False
                            straight_activate = False
                            semicircular_id += 1
                            if semicircular_id == 3:
                                semicircularLaser_active = False
                        break
                    if button_continuousShooting.collidepoint((mx, my)) and semicircular_id == 0:
                        if coins >= continuousShooting_coin:
                            show_text_prohibit(button_continuousShooting_x + button_continuousShooting.width / 2,
                                               button_continuousShooting_y + button_continuousShooting.height / 2,
                                               "Continuous Shooting +1", 18)
                            coins -= continuousShooting_coin
                            continuousShooting_coin *= 2
                            player.continuous += 1
                        break
        pygame.display.update()  # Update


def highScores():
    global hs_run
    hs = load_highscore_from_file()
    while hs_run:
        screen.blit(background, (0, 0))
        show_texts_middle(0, "Leader Board", 100)
        for index, sc in enumerate(hs):
            show_texts(200, 200 + index * 50, f"{index + 1}.     {sc[0]}    {sc[1]}", 25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    hs_run = False
        pygame.display.update()  # Update


def tutorial():
    global tutor_run
    while tutor_run:
        screen.blit(background, (0, 0))
        show_texts_middle(0, "Tutorial", 100)

        screen.blit(WASD_key, (50, 150))
        screen.blit(Arrow_key, (200, 150))
        show_text_menu(185, 175, "or", 20)
        show_texts(xScreen / 2 + 30, 160, ": Control your plane", 25)

        screen.blit(Space_key, (130, 225))
        show_texts(xScreen / 2 + 30, 245, ": Hold to shoot", 25)

        screen.blit(Esc_key, (135, 275))
        show_texts(xScreen / 2 + 30, 295, ": Back (can use ingame)", 25)

        screen.blit(Exit_key, (135, 325))
        show_texts(xScreen / 2 + 30, 345, ": Exit without saving", 25)

        show_texts_middle(380, "Space store", 40)
        show_texts(20, 430, "- You can buy items in space store by using coin from game.", 20)
        show_texts(20, 460, "- Destroy enemy ship by your bullet will get you coins.", 20)
        show_texts(20, 490, "- Different enemy earn different coins.", 20)
        show_texts(20, 520, "- Semicircular bullets is too powerful so you can shoot only", 20)
        show_texts(20, 545, "  1 bullet at a time", 20)
        show_texts(20, 575, "- You can crash enemies to kill them instantly but earn no coins", 20)
        show_texts(20, 600, "- You can press Esc while playing to pause and enter Space Store.", 20)
        show_texts(20, 630, "- Lives will be reset to 5 when level up.", 20)
        show_texts(20, 660, "- You MUST press the continue button to return to the game.", 20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    tutor_run = False
        pygame.display.update()  # Update


if __name__ == "__main__":
    main_menu()
