import pygame
import os
from hexagon import Hexagon
def dostupnie_hexagones(now, n, hexagons):
    allowed_hexagons = []
    res = set([hexagons.index(now)])  # Шоб не повторялись
    for _ in range(n):
        new_res = set()
        for num in res:
            if num == 15 or num == 30 or num == 45 or num == 60 or num == 75 or num == 90 or num == 105 or num == 120 or num == 135 or num == 150 :
                new_res.add(num + 1)
            elif num == 14 or num == 29 or num == 44 or num == 59 or num == 74 or num == 89 or num == 104 or num == 119 or num == 134 or num == 149 or num == 164:
                new_res.add(num - 1)
            else:
                new_res.add(num - 1)
                new_res.add(num + 1)
            if num // 15 % 2 == 1:
                if num == 15 or num == 45 or num == 75 or num == 105 or num == 135:
                    new_res.add(num + 15)
                    new_res.add(num - 15)
                else:
                    new_res.add(num - 15)
                    new_res.add(num - 16)
                    new_res.add(num + 14)
                    new_res.add(num + 15)
            else:
                if num == 14 or num == 44 or num == 74 or num == 104 or num == 134 or num == 164:
                    new_res.add(num + 15)
                    new_res.add(num - 15)
                else:
                    new_res.add(num - 14)
                    new_res.add(num - 15)
                    new_res.add(num + 15)
                    new_res.add(num + 16)
        ubrat_otric = []
        for num in new_res:
            if 0 <= num <= 164:
                ubrat_otric.append(num)
        res = ubrat_otric
    res = list(res)
    res.sort()
    for i in res:
        allowed_hexagons.append(hexagons[i])
    return allowed_hexagons

class Unit:
    def __init__(self, image_path, hexagon, current_player):
        self.image = pygame.image.load(image_path)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        hexagon_center = (sum(point[0] for point in hexagon.points) // 6, sum(point[1] for point in hexagon.points) // 6)
        self.x = hexagon_center[0] - self.width // 2
        self.y = hexagon_center[1] - self.height // 2
        self.is_selected = False
        self.is_targeting = False
        self.is_targeting_for_fire = False
        self.is_selected_for_fire = False
        self.target_hexagon = hexagon
        self.previous_hexagon = self.target_hexagon
        self.previous_x = self.x
        self.previous_y = self.y
        self.current_player = current_player
        self.dlina_xoda = 0
        self.fire_range = 0
        self.hp = 0
        self.damage = 0
        self.name = ""
        self.attack_animation = None
        self.gameover = False


    def get_pos(self):
        return(self.target_hexagon)
    def get_dliny(self):
        return(self.dlina_xoda)

    def shoot(self, x, y):
        line_color = (255, 0, 0)
        line_width = 5
        start_x, start_y = self.x, self.y
        end_x, end_y = x, y
        dx = end_x - start_x
        dy = end_y - start_y
        steps = max(abs(dx), abs(dy))
        x_step = dx / steps
        y_step = dy / steps
        current_x = start_x
        current_y = start_y
        line_segments = []
        for _ in range(steps):
            line_segments.append((current_x + 45, current_y + 35))
            current_x += x_step
            current_y += y_step
        pygame.draw.aalines(screen, line_color, False, line_segments, line_width)
        pygame.display.flip()
    def babax(self):
        clock = pygame.time.Clock()
        image_path = os.path.join("images", "babax.gif")
        animation = pygame.image.load(image_path)
        screen.blit(animation, (self.x, self.y - 15))  # Отображение гиф-анимации в левом верхнем углу
        pygame.display.flip()  # Обновление экрана
        clock.tick(1)  # Ограничение FPS до 60

    def stats(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:  # Щелчок средней кнопки мыши
                mouse_pos = pygame.mouse.get_pos()
                if self.image.get_rect(x=self.x, y=self.y).collidepoint(mouse_pos):
                    mouse_pos = pygame.mouse.get_pos()
                    x, y = mouse_pos
                    window_width, window_height = 260, 155  # Размеры окна

                    if x + window_width > screen.get_width():
                        x -= window_width  # Сдвигаем окно влево, если оно выходит за пределы экрана по горизонтали
                    if y - window_height < 0:
                        y += window_height  # Сдвигаем окно вниз, если оно выходит за пределы экрана по вертикали

                    pygame.draw.rect(screen, (0, 0, 0),(x, y - window_height, window_width, window_height))  # Рисуем черный квадрат

                    # Вывод информации о свойствах объекта
                    info_font = pygame.font.SysFont("Arial", 20)
                    name = info_font.render(f"Название: {self.name}", True, (255, 255, 255))
                    dlina_xoda_text = info_font.render(f"Движение: {self.dlina_xoda}", True, (255, 255, 255))
                    fire_range_text = info_font.render(f"Дальнобойность: {self.fire_range}", True, (255, 255, 255))
                    hp_text = info_font.render(f"Здоровье: {self.hp}", True, (255, 255, 255))
                    damage_text = info_font.render(f"Урон: {self.damage}", True, (255, 255, 255))

                    # Отображение текста в черном квадрате
                    screen.blit(name, (x + 10, y - window_height + 10))
                    screen.blit(dlina_xoda_text, (x + 10, y - window_height + 40))
                    screen.blit(fire_range_text, (x + 10, y - window_height + 70))
                    screen.blit(hp_text, (x + 10, y - window_height + 100))
                    screen.blit(damage_text, (x + 10, y - window_height + 130))

                    pygame.display.flip()

    def fire(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Щелчок правой кнопки мыши
                mouse_pos = pygame.mouse.get_pos()
                if self.image.get_rect(x=self.x, y=self.y).collidepoint(mouse_pos):
                    if not self.is_selected_for_fire:
                        self.is_selected_for_fire = True
                        self.is_targeting_for_fire = False
                    else:
                        self.is_targeting_for_fire = True
                        self.is_selected_for_fire = False
                elif self.is_selected_for_fire and not self.is_targeting_for_fire:
                    mouse_pos = pygame.mouse.get_pos()
                    hexagon_clicked = None
                    new_hexagons = dostupnie_hexagones(self.target_hexagon, self.fire_range, hexagons)
                    for hexagon in new_hexagons:
                        if hexagon.contains_point(mouse_pos):
                            hexagon_clicked = hexagon
                            break
                    if hexagon_clicked is not None:
                        #Если кликнули именно на гекс
                        if self.current_player == player1:
                            enemy_units = player2_units
                        else:
                            enemy_units = player1_units
                        for unit in enemy_units:
                            if unit.target_hexagon is hexagon_clicked:
                                self.shoot(unit.x, unit.y)
                                unit.hp -= self.damage
                                if self.current_player == player1:
                                    if unit.hp <= 0:
                                        player2_units.remove(unit)
                                        unit.babax()
                                        if not player2_units:
                                            self.gameover = True
                                        if isinstance(unit, Team):
                                            self.gameover = True
                                    current_player[0] = player2
                                else:
                                    if unit.hp <= 0:
                                        player1_units.remove(unit)
                                        unit.babax()
                                        if not player1_units:
                                            self.gameover = True
                                        if isinstance(unit, Team):
                                            self.gameover = True
                                    current_player[0] = player1
                    self.is_selected_for_fire = False
                    self.is_targeting_for_fire = False

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Щелчок левой кнопкой мыши
                mouse_pos = pygame.mouse.get_pos()
                if self.image.get_rect(x=self.x, y=self.y).collidepoint(mouse_pos):
                    if not self.is_selected:
                        self.is_selected = True
                    else:
                        self.is_targeting = True
        elif event.type == pygame.MOUSEMOTION:
            if self.is_selected and not self.is_targeting:
                mouse_pos = pygame.mouse.get_pos()
                self.x = max(0, min(mouse_pos[0] - self.width // 2, SCREEN_WIDTH - self.width))
                self.y = max(0, min(mouse_pos[1] - self.height // 2, SCREEN_HEIGHT - self.height))
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Отпускание левой кнопки мыши
                if self.is_targeting:
                    mouse_pos = pygame.mouse.get_pos()
                    hexagon_clicked = None
                    new_hexagons = dostupnie_hexagones(self.target_hexagon, self.dlina_xoda, hexagons)
                    for hexagon in new_hexagons:
                        if hexagon.contains_point(mouse_pos):
                            hexagon_clicked = hexagon
                            break
                    if hexagon_clicked is not None:
                        # Проверяем, что шестиугольник не занят другим юнитом
                        is_hexagon_occupied = False
                        for unit in player1_units + player2_units:
                            if unit is not self and unit.target_hexagon is hexagon_clicked:
                                is_hexagon_occupied = True
                                break
                        if not is_hexagon_occupied:
                            hexagon_center = (sum(point[0] for point in hexagon_clicked.points) // 6,sum(point[1] for point in hexagon_clicked.points) // 6)
                            self.previous_x = self.x  # Сохраняем предыдущие координаты x
                            self.previous_y = self.y  # Сохраняем предыдущие координаты y
                            self.previous_hexagon = self.target_hexagon
                            self.x = hexagon_center[0] - self.width // 2
                            self.y = hexagon_center[1] - self.height // 2
                            self.target_hexagon = hexagon_clicked
                        else:
                            # Если шестиугольник занят, вернуть юнит в предыдущие координаты
                            self.x = self.previous_x
                            self.y = self.previous_y
                            hexagon_center = (sum(point[0] for point in self.target_hexagon.points) // 6, sum(point[1] for point in self.target_hexagon.points) // 6)
                            self.x = hexagon_center[0] - self.width // 2
                            self.y = hexagon_center[1] - self.height // 2
                    elif hexagon_clicked is None:
                        self.target_hexagon = self.previous_hexagon
                        hexagon_center = (sum(point[0] for point in self.target_hexagon.points) // 6,sum(point[1] for point in self.target_hexagon.points) // 6)
                        self.x = hexagon_center[0] - self.width // 2
                        self.y = hexagon_center[1] - self.height // 2
                    elif self.target_hexagon is not None:
                        hexagon_center = (sum(point[0] for point in self.target_hexagon.points) // 6,sum(point[1] for point in self.target_hexagon.points) // 6)
                        self.x = hexagon_center[0] - self.width // 2
                        self.y = hexagon_center[1] - self.height // 2
                        self.previous_hexagon = self.target_hexagon
                    else:
                        # Если нет целевого шестиугольника, сбросить позицию в предыдущие координаты
                        self.x = self.previous_x
                        self.y = self.previous_y
                        self.target_hexagon = self.previous_hexagon
                    if  self.target_hexagon != self.previous_hexagon:
                        # Позиция юнита изменилась
                        if self.current_player == player1:
                            current_player[0] = player2
                            self.previous_hexagon = self.target_hexagon
                        else:
                            current_player[0] = player1
                            self.previous_hexagon = self.target_hexagon
                    self.is_selected = False
                    self.is_targeting = False

class Scout(Unit):
    def __init__(self, image_path, hexagon, current_player):
        super().__init__(image_path, hexagon, current_player)
        self.dlina_xoda = 6
        self.fire_range = 2
        self.hp = 2
        self.damage = 1
        self.name = "Скаут"

class Serafim(Unit):
    def __init__(self, image_path, hexagon, current_player):
        super().__init__(image_path, hexagon, current_player)
        self.dlina_xoda = 2
        self.fire_range = 4
        self.hp = 8
        self.damage = 3
        self.name = "Серафим"

class Istebitel(Unit):
    def __init__(self, image_path, hexagon, current_player):
        super().__init__(image_path, hexagon, current_player)
        self.dlina_xoda = 4
        self.fire_range = 4
        self.hp = 3
        self.damage = 5
        self.name = "Истребитель"

class Team(Unit):
    def __init__(self, image_path, hexagon, current_player):
        super().__init__(image_path, hexagon, current_player)
        self.dlina_xoda = 4
        self.fire_range = 0
        self.hp = 10
        self.damage = 0
        self.name = "Командный корабль"


# Инициализация Pygame
pygame.init()

game_state = "start_menu"

# Получение разрешения экрана
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

# Создание полноэкранного окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Звёздный адмирал")

# Загрузка изображений
start = pygame.image.load("images/start.png")
rules = pygame.image.load("images/rules.png")
exit = pygame.image.load("images/exit.png")
fon = pygame.image.load("images/fon.png")
red_win = pygame.image.load("images/red_win.png")
blue_win = pygame.image.load("images/blue_win.png")
fonrules = pygame.image.load("images/text.png")
gameboard = pygame.image.load("images/gameboard.jpg")
gameboard = pygame.transform.scale(gameboard, (SCREEN_WIDTH, SCREEN_HEIGHT - 100))  # Изменение размера
gameboard_rect = gameboard.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image

image = load_image("cursor.png")

fon = pygame.transform.scale(fon, (SCREEN_WIDTH, SCREEN_HEIGHT))
fonrules = pygame.transform.scale(fonrules, (SCREEN_WIDTH, SCREEN_HEIGHT))
# Создание шестиугольников
hexagon_points = [
    [(100, 102), (150, 122), (150, 163), (100, 183), (50, 163), (50, 122)],
    [(51, 163), (100, 184), (100, 224), (51, 244), (0, 224), (0, 184)],
    [(100, 224), (150, 244), (150, 286), (100, 305), (50, 286), (50, 244)],
    [(51, 285), (100, 306), (100, 347), (51, 366), (0, 347), (0, 306)],
    [(100, 346), (150, 366), (150, 409), (100, 427), (50, 409), (50, 366)],
    [(51, 407), (100, 428), (100, 470), (51, 488), (0, 470), (0, 428)],
    [(100, 468), (150, 488), (150, 532), (100, 549), (50, 532), (50, 488)],
    [(51, 529), (100, 550), (100, 593), (51, 610), (0, 593), (0, 550)],
    [(100, 590), (150, 610), (150, 655), (100, 671), (50, 655), (50, 610)],
    [(51, 651), (100, 672), (100, 716), (51, 732), (0, 716), (0, 672)],
    [(100, 712), (150, 732), (150, 778), (100, 793), (50, 778), (50, 732)],
]
# Создание новых шестиугольников с увеличением шага вправо на 125 пикселей
new_hexagon_points = []
for hexagon in hexagon_points:
    for _ in range(15):
        new_hexagon_points.append(hexagon)
        hexagon = [(x + 99, y) for x, y in hexagon]

# Создание объектов Hexagon на основе обновленных координат
hexagons = [Hexagon(points) for points in new_hexagon_points]

player1 = "d1pty"
player2 = "kendor"
current_player = [player1]

# Создание юнитов
player1_units = [
    Scout("images/ccs.png", hexagons[0], player1),
    Serafim("images/sir.png", hexagons[30], player1),
    Istebitel("images/istr.png", hexagons[60], player1),
    Team("images/commands.png", hexagons[90], player1),
    Istebitel("images/istr.png", hexagons[120], player1),
    Scout("images/ccs.png",hexagons[150], player1)
]

player2_units = [
    Scout("images/ccs2.png", hexagons[14], player2),
    Serafim("images/sir2.png", hexagons[44], player2),
    Istebitel("images/istr2.png", hexagons[74], player2),
    Team("images/commands2.png", hexagons[104], player2),
    Istebitel("images/istr2.png", hexagons[134], player2),
    Scout("images/ccs2.png", hexagons[164], player2)
]
obresc = 0
# Основной игровой цикл
pygame.mixer.music.load("images/menu.mp3")
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play(-1) # -1 бесконечное повторение
running = True
while running:
    keys = pygame.key.get_pressed()
    if game_state == "start_menu":  # Загрузка игрового меню
        screen.blit(fon, (0, 0))

        # Создание кнопок
        button_start = pygame.Rect(100, 560, 320, 80)
        button_rules = pygame.Rect(100, 630, 320, 80)
        button_exit = pygame.Rect(100, 700, 320, 80)

        screen.blit(start, button_start)
        screen.blit(rules, button_rules)
        screen.blit(exit, button_exit)
    if game_state == "rules":
        screen.blit(fonrules, (0, 0))
        if keys[pygame.K_ESCAPE]:
            game_state = "start_menu"
    if game_state == "game_over_1":
        screen.fill((0, 0, 0))

        # Размещение надписи по центру экрана
        font = pygame.font.Font(None, 200)
        text_surface = font.render("Победил красный", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=screen.get_rect().center)
        text_rect.centery += 100
        screen.blit(text_surface, text_rect)

        # Размещение картинки над надписью
        red_win_rect = red_win.get_rect(center=(text_rect.centerx, text_rect.centery - 250))
        screen.blit(red_win, red_win_rect)

        pygame.display.flip()
        player1_units = [
            Scout("images/ccs.png", hexagons[0], player1),
            Serafim("images/sir.png", hexagons[30], player1),
            Istebitel("images/istr.png", hexagons[60], player1),
            Team("images/commands.png", hexagons[90], player1),
            Istebitel("images/istr.png", hexagons[120], player1),
            Scout("images/ccs.png", hexagons[150], player1)
        ]
        player2_units = [
            Scout("images/ccs2.png", hexagons[14], player2),
            Serafim("images/sir2.png", hexagons[44], player2),
            Istebitel("images/istr2.png", hexagons[74], player2),
            Team("images/commands2.png", hexagons[104], player2),
            Istebitel("images/istr2.png", hexagons[134], player2),
            Scout("images/ccs2.png", hexagons[164], player2)
        ]
        current_player = [player1]
        if keys[pygame.K_ESCAPE]:
            game_state = "start_menu"
            pygame.display.update()
    if game_state == "game_over_2":
        screen.fill((0, 0, 0))

        # Размещение надписи по центру экрана
        font = pygame.font.Font(None, 200)
        text_surface = font.render("Победил синий", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=screen.get_rect().center)
        text_rect.centery += 100
        screen.blit(text_surface, text_rect)

        # Размещение картинки над надписью
        red_win_rect = blue_win.get_rect(center=(text_rect.centerx, text_rect.centery - 250))
        screen.blit(blue_win, red_win_rect)

        pygame.display.flip()
        player1_units = [
            Scout("images/ccs.png", hexagons[0], player1),
            Serafim("images/sir.png", hexagons[30], player1),
            Istebitel("images/istr.png", hexagons[60], player1),
            Team("images/commands.png", hexagons[90], player1),
            Istebitel("images/istr.png", hexagons[120], player1),
            Scout("images/ccs.png", hexagons[150], player1)
        ]
        player2_units = [
            Scout("images/ccs2.png", hexagons[14], player2),
            Serafim("images/sir2.png", hexagons[44], player2),
            Istebitel("images/istr2.png", hexagons[74], player2),
            Team("images/commands2.png", hexagons[104], player2),
            Istebitel("images/istr2.png", hexagons[134], player2),
            Scout("images/ccs2.png", hexagons[164], player2)
        ]
        current_player = [player1]
        if keys[pygame.K_ESCAPE]:
            game_state = "start_menu"
            pygame.display.update()
    if game_state == "game":
        if keys[pygame.K_ESCAPE]:
            game_state = "start_menu"
            pygame.display.update()
        else:

            # Заполнение экрана черным фоном
            screen.fill((0, 0, 0))

            # Отрисовка игрового поля
            screen.blit(gameboard, gameboard_rect)
            # Отрисовка юнитов
            for unit in player1_units + player2_units:
                unit.draw(screen)


    for event in pygame.event.get():
        move_hexagons = []
        fire_hexagons = []
        if current_player[0] == player1:
            for unit in player1_units:
                unit.stats(event)
                unit.handle_event(event)
                unit.fire(event)
                if unit.gameover:
                    game_state = "game_over_1"
                    break
                if unit.is_selected_for_fire and not unit.is_targeting_for_fire:
                    fire_hexagons = dostupnie_hexagones(unit.target_hexagon, unit.fire_range, hexagons)
                    for hexagon in fire_hexagons:
                        hexagon.draw_fire(screen)
                if unit.is_selected and not unit.is_targeting:
                    move_hexagons = dostupnie_hexagones(unit.target_hexagon, unit.dlina_xoda, hexagons)
                    for hexagon in move_hexagons:
                        hexagon.draw_move(screen)
        else:
            for unit in player2_units:
                unit.stats(event)
                unit.handle_event(event)
                unit.fire(event)
                if unit.gameover:
                    game_state = "game_over_2"
                    break
                if unit.is_selected_for_fire and not unit.is_targeting_for_fire:
                    fire_hexagons = dostupnie_hexagones(unit.target_hexagon, unit.fire_range, hexagons)
                    for hexagon in fire_hexagons:
                        hexagon.draw_fire(screen)
                if unit.is_selected and not unit.is_targeting:
                    move_hexagons = dostupnie_hexagones(unit.target_hexagon, unit.dlina_xoda, hexagons)
                    for hexagon in move_hexagons:
                        hexagon.draw_move(screen)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
            screen.blit(image, event.pos)
            pygame.mouse.set_visible(False)
            pygame.display.flip()
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:  # Щелчок левой кнопкой мыши
                mouse_pos = pygame.mouse.get_pos()
                if button_start.collidepoint(mouse_pos):
                    game_state = "game"
                elif game_state=="game":
                    pass
                elif button_rules.collidepoint(mouse_pos):
                    game_state = "rules"
                elif button_exit.collidepoint(mouse_pos):
                    running = False

    if game_state == "rules":
        #screen.blit(fonrules, (0, 0))
        if keys[pygame.K_ESCAPE]:
            game_state = "start_menu"

    # Завершение работы Pygame
pygame.quit()