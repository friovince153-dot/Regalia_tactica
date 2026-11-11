import math
import pygame 
import os, sys
from characters import Bandit, MageHealer 
from combat import Battle

# ---------- MAIN MENU THEME ----------
menu_dark = (18, 14, 24)
menu_parchment = (232, 205, 160)
menu_gold = (212, 175, 55)
menu_ember = (255, 120, 40)
menu_dim = (120, 100, 90)

title_font = pygame.font.SysFont('Times New Roman', 68, bold=True)
menu_font = pygame.font.SysFont('Times New Roman', 32, bold=True)
small_font = pygame.font.SysFont('Times New Roman', 20)

menu_options = ["Start Battle", "Quit"]
selected_option = 0
in_menu = True
menu_time = 0

def draw_menu_button(text, x, y, width, height, selected):
    mouse_pos = pygame.mouse.get_pos()
    hovered = pygame.Rect(x, y, width, height).collidepoint(mouse_pos)

    if selected or hovered:
        border_color = menu_ember
        fill_color = (48, 30, 24)
        text_color = menu_parchment
    else:
        border_color = menu_gold
        fill_color = (28, 22, 32)
        text_color = menu_dim

    pygame.draw.rect(screen, fill_color, (x, y, width, height), border_radius=12)
    pygame.draw.rect(screen, border_color, (x, y, width, height), 3, border_radius=12)

    label = menu_font.render(text, True, text_color)
    label_rect = label.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(label, label_rect)

    return pygame.Rect(x, y, width, height)

def draw_main_menu():
    global menu_time
    menu_time += 1

    # Dark atmospheric background
    screen.fill(menu_dark)

    # Subtle vignette / glowing ember effect
    glow_radius = 260 + int(18 * math.sin(menu_time * 0.03))
    glow = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    pygame.draw.circle(
        glow,
        (255, 110, 30, 28),
        (screen_width // 2, screen_height // 2 - 40),
        glow_radius
    )
    screen.blit(glow, (0, 0))

    # Title
    title = title_font.render("REGALIA TACTICA", True, menu_parchment)
    title_shadow = title_font.render("REGALIA TACTICA", True, (0, 0, 0))
    title_rect = title.get_rect(center=(screen_width // 2, 125))

    screen.blit(title_shadow, (title_rect.x + 4, title_rect.y + 5))
    screen.blit(title, title_rect)

    pygame.draw.line(
        screen,
        menu_gold,
        (screen_width // 2 - 230, 180),
        (screen_width // 2 + 230, 180),
        3
    )

    subtitle = small_font.render("A Tactical Fantasy Battle", True, menu_gold)
    screen.blit(
        subtitle,
        subtitle.get_rect(center=(screen_width // 2, 210))
    )

    # Buttons
    button_width = 320
    button_height = 64
    button_x = (screen_width - button_width) // 2

    rects = []
    for index, option in enumerate(menu_options):
        y = 300 + index * 95
        rect = draw_menu_button(option, button_x, y, button_width, button_height, index == selected_option)
        rects.append(rect)

    hint = small_font.render("Use Up / Down and Enter, or click a button", True, (170, 150, 130))
    screen.blit(hint, hint.get_rect(center=(screen_width // 2, screen_height - 45)))

    return rects

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)   # point relative paths at the unpacked bundle
    
pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
bottom_panel = 150
screen_width = 800
screen_height =  450 + bottom_panel     
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Regalia Tactica")

#font
font = pygame.font.SysFont('Times New Roman', 26)

#font color
rust_red = (183, 65, 14)
green = (0, 255, 0)
red = (255, 0, 0)


#load images
#background image
background = pygame.image.load('image/background/forest.png').convert_alpha()
#panel image
panel_img = pygame.image.load('image/ui/panel.png').convert_alpha()

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg():
    screen.blit(background, (0, 0))

class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        #update with new health
        self.hp = hp
        #calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))
        

mage = MageHealer(200, 446, "Sage", max_hp=30, strength=5,
                magic=8, speed=10, resistance=8)

bandit1 = Bandit(542, 442, "Bandit", max_hp=20, strength=10,
                 magic=0, speed=12, resistance=5)

bandit2 = Bandit(692, 442, "Bandit", max_hp=20, strength=10,
                 magic=0, speed=12, resistance=5)

top = screen_height - bottom_panel
Sage_health_bar = HealthBar(100, top + 45, mage.hp, mage.max_hp)
Bandit1_health_bar = HealthBar(550, top + 45, bandit1.hp, bandit1.max_hp)
Bandit2_health_bar = HealthBar(550, top + 110, bandit2.hp, bandit2.max_hp)

battle = Battle(players=[mage], enemies=[bandit1, bandit2])

def draw_panel():
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    draw_text(f'{mage.name} HP: {mage.hp}', font, green, 100, screen_height - bottom_panel + 15)
    for count, i in enumerate([bandit1, bandit2]):
        draw_text(f'{i.name} HP: {i.hp}', font, rust_red, 550, screen_height - bottom_panel + 15 + count * 60)
    Sage_health_bar.draw(mage.hp)
    Bandit1_health_bar.draw(bandit1.hp)
    Bandit2_health_bar.draw(bandit2.hp)

run = True
while run:
    clock.tick(fps)

    clicked = False
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if in_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        in_menu = False
                    elif selected_option == 1:
                        run = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True

    if in_menu:
        menu_buttons = draw_main_menu()

        for index, rect in enumerate(menu_buttons):
            if rect.collidepoint(mouse_pos):
                selected_option = index
                if clicked:
                    if index == 0:
                        in_menu = False
                    elif index == 1:
                        run = False

        pygame.display.update()
        continue

    battle.update(mouse_pos, clicked)  # updates every fighter, so no f.update() calls

    draw_bg()
    for f in (mage, bandit1, bandit2):
        f.draw(screen)
    draw_panel()
    battle.draw(screen)

    pygame.display.update()

pygame.quit()
