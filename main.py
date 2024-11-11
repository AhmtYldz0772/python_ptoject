import pgzrun
import random
from pygame import Rect
from math import sqrt

# Ekran boyutları
WIDTH = 800
HEIGHT = 600

# Oyun durumu değişkenleri
game_state = "menu"
music_on = True

# Menüdeki seçenekler
menu_options = ["Start Game", "Toggle Music", "Exit"]
selected_option = 0

# Oyuncu ve düşman sınıfları
class Player:
    def __init__(self, pos):
        self.rect = Rect(pos[0], pos[1], 32, 32)
        self.speed = 4
        self.image = "player_idle"
        self.direction = "down"

    def move(self, keys):
        if keys["left"]:
            self.rect.x -= self.speed
            self.direction = "left"
        if keys["right"]:
            self.rect.x += self.speed
            self.direction = "right"
        if keys["up"]:
            self.rect.y -= self.speed
            self.direction = "up"
        if keys["down"]:
            self.rect.y += self.speed
            self.direction = "down"

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Enemy:
    def __init__(self, pos):
        self.rect = Rect(pos[0], pos[1], 32, 32)
        self.speed = 2
        self.direction = random.choice(["left", "right", "up", "down"])
        self.image = "enemy_idle"

    def move(self):
        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed

        # Duvarlara çarpma kontrolü
        if self.rect.left < 0 or self.rect.right > WIDTH or self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.direction = random.choice(["left", "right", "up", "down"])

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


# Oyuncu ve düşman nesneleri
player = Player((100, 100))
enemies = [Enemy((random.randint(50, 750), random.randint(50, 550))) for _ in range(3)]

# Ana menü çizim fonksiyonu
def draw_menu():
    screen.clear()
    screen.draw.text("Roguelike Game", center=(WIDTH // 2, 100), fontsize=50, color="white")
    for index, option in enumerate(menu_options):
        color = "yellow" if index == selected_option else "white"
        screen.draw.text(option, center=(WIDTH // 2, 200 + index * 50), fontsize=40, color=color)

# Oyun ekranı çizim fonksiyonu
def draw_game():
    screen.clear()
    player.draw()
    for enemy in enemies:
        enemy.draw()

# Ana çizim fonksiyonu
def draw():
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        draw_game()

# Menü kontrolü
def handle_menu_input():
    global selected_option, game_state, music_on
    if keyboard.up:
        selected_option = (selected_option - 1) % len(menu_options)
    elif keyboard.down:
        selected_option = (selected_option + 1) % len(menu_options)
    elif keyboard.enter:
        if menu_options[selected_option] == "Start Game":
            game_state = "playing"
        elif menu_options[selected_option] == "Toggle Music":
            music_on = not music_on
        elif menu_options[selected_option] == "Exit":
            exit()

# Oyun güncelleme fonksiyonu
def update():
    global game_state
    if game_state == "menu":
        handle_menu_input()
    elif game_state == "playing":
        player.move({
            "left": keyboard.left,
            "right": keyboard.right,
            "up": keyboard.up,
            "down": keyboard.down
        })
        for enemy in enemies:
            enemy.move()

# Arka plan müziği
if music_on:
    music.play("background_music")

pgzrun.go()
