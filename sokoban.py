# 'w' - стена
# ' ' - pол
# 'p' - персонаж
# 'b' - коробка
# 'd' - место коробки
# 'i' - коробка на месте
# 'o' - персонаж на месте коробки
import pygame
import os
import time
import sqlite3


class Sokoban:
    def __init__(self, level):
        self.levels = level

    def character_position(self):
        x, y = 0, 0
        for line in self.levels:
            for view in line:
                if view == 'p' or view == 'o':
                    return [x, y, view]
                x += 1
            y += 1
            x = 0

    def can_move(self, x, y):
        if self.levels[self.character_position()[1] + y][self.character_position()[0] + x] not in ['i', 'b', 'w']:
            return True
        else:
            return False

    def can_shift(self, x, y):
        if self.levels[self.character_position()[1] + y][self.character_position()[0] + x] in ['i', 'b'] and \
                self.levels[self.character_position()[1] + y + y][self.character_position()[0] + x + x] in ['d', ' ']:
            return True
        else:
            return False

    def map_update(self, x, y, object):
        self.levels[y][x] = object

    def move_character(self, x, y):
        character = self.character_position()
        element = self.levels[self.character_position()[1] + y][self.character_position()[0] + x]
        if self.can_move(x, y):
            if character[2] == 'p' and element == ' ':
                self.map_update(character[0] + x, character[1] + y, 'p')
                self.map_update(character[0], character[1], ' ')
            if character[2] == 'p' and element == 'd':
                self.map_update(character[0] + x, character[1] + y, 'o')
                self.map_update(character[0], character[1], ' ')
            if character[2] == 'o' and element == ' ':
                self.map_update(character[0] + x, character[1] + y, 'p')
                self.map_update(character[0], character[1], 'd')
            if character[2] == 'o' and element == 'd':
                self.map_update(character[0] + x, character[1] + y, 'o')
                self.map_update(character[0], character[1], 'd')
        elif self.can_shift(x, y):
            element_next = self.levels[self.character_position()[1] + y + y][self.character_position()[0] + x + x]
            if character[2] == 'p' and element == 'b' and element_next == ' ':
                self.map_update(character[0] + x + x, character[1] + y + y, 'b')
                self.map_update(character[0] + x, character[1] + y, 'p')
                self.map_update(character[0], character[1], ' ')
            if character[2] == 'p' and element == 'b' and element_next == 'd':
                self.map_update(character[0] + x + x, character[1] + y + y, 'i')
                self.map_update(character[0] + x, character[1] + y, 'p')
                self.map_update(character[0], character[1], ' ')
            if character[2] == 'p' and element == 'i' and element_next == ' ':
                self.map_update(character[0] + x + x, character[1] + y + y, 'b')
                self.map_update(character[0] + x, character[1] + y, 'o')
                self.map_update(character[0], character[1], ' ')
            if character[2] == 'p' and element == 'i' and element_next == 'd':
                self.map_update(character[0] + x + x, character[1] + y + y, 'i')
                self.map_update(character[0] + x, character[1] + y, 'o')
                self.map_update(character[0], character[1], ' ')
            if character[2] == 'o' and element == 'b' and element_next == ' ':
                self.map_update(character[0] + x + x, character[1] + y + y, 'b')
                self.map_update(character[0] + x, character[1] + y, 'p')
                self.map_update(character[0], character[1], 'd')
            if character[2] == 'o' and element == 'b' and element_next == 'd':
                self.map_update(character[0] + x + x, character[1] + y + y, 'i')
                self.map_update(character[0] + x, character[1] + y, 'p')
                self.map_update(character[0], character[1], 'd')
            if character[2] == 'o' and element == 'i' and element_next == ' ':
                self.map_update(character[0] + x + x, character[1] + y + y, 'b')
                self.map_update(character[0] + x, character[1] + y, 'o')
                self.map_update(character[0], character[1], 'd')
            if character[2] == 'o' and element == 'i' and element_next == 'd':
                self.map_update(character[0] + x + x, character[1] + y + y, 'i')
                self.map_update(character[0] + x, character[1] + y, 'o')
                self.map_update(character[0], character[1], 'd')

    def level_reset(self, a):
        for y in range(len(self.levels)):
            for x in range(len(self.levels[y])):
                self.levels[y][x] = a[y][x]

    def level_complet(self):
        for row in self.levels:
            for el in row:
                if el == 'b':
                    return False
        return True


class Game:
    def __init__(self, parent):

        def window_size(level):
            y = len(level)
            x = len(level[0])
            return [x * 64, y * 64]

        def load_level(level_number, filename):
            nonlocal tic
            pygame.mixer.music.play(-1)
            tic = time.perf_counter()
            file = open(filename, 'r')
            levels = list()
            found = False
            for line in file:
                if not found:
                    if f'level {str(level_number)}' == line.strip():
                        found = True
                else:
                    if line.strip() != '':
                        row = list()
                        for el in line:
                            if el != '\n':
                                row.append(el)
                            elif el == '\n':
                                continue
                        levels.append(row)
                    else:
                        return levels

        def draw_map(level, screen):
            x, y = 0, 0
            for row in level:
                for el in row:
                    if el == ' ':
                        screen.blit(floor, (x, y))
                    elif el == 'w':
                        screen.blit(wall, (x, y))
                    elif el == 'b':
                        screen.blit(box, (x, y))
                    elif el == 'p':
                        screen.blit(charecter, (x, y))
                    elif el == 'd':
                        screen.blit(dock, (x, y))
                    elif el == 'i':
                        screen.blit(box_in_dock, (x, y))
                    elif el == 'o':
                        screen.blit(charecter_on_dock, (x, y))
                    x += 64
                y += 64
                x = 0

        def draw_game_over(old_time, new_time):
            img = pygame.image.load('data/game_over.jpg')
            screen = pygame.display.set_mode([500, 200])
            font = pygame.font.SysFont("kacstbook", 25)
            text_o_t = font.render(f"лучшее время: {old_time} секунд", True, (0, 0, 255))
            text_n_t = font.render(f"время прохождения: {new_time} секунд", True, (0, 0, 255))
            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                screen.fill((0, 0, 0))
                screen.blit(pygame.transform.scale(img, [500, 200]), [10, 10])
                screen.blit(text_o_t, (40, 90))
                screen.blit(text_n_t, (40, 120))
                pygame.display.update()

        parent.hide()
        tic = 0
        number = open('level_number.txt', 'r').readline()
        os.remove('level_number.txt')
        decor = open('decoration.txt', 'r').readline()
        os.remove('decoration.txt')
        name = 'levels.txt'
        if decor == '1':
            wall = pygame.image.load('data/wall.png')
            box = pygame.image.load('data/box.png')
            floor = pygame.image.load('data/floor.png')
            charecter = pygame.image.load('data/charecter.png')
            dock = pygame.image.load('data/dock.png')
            box_in_dock = pygame.image.load('data/box in dock.png')
            charecter_on_dock = pygame.image.load('data/charecter on dock.png')
        elif decor == '2':
            floor = pygame.image.load('data/floor_2.png')
            box = pygame.image.load('data/box_2.png')
            wall = pygame.image.load('data/wall_2.png')
            charecter = pygame.image.load('data/charecter_2.png')
            dock = pygame.image.load('data/dock_2.png')
            box_in_dock = pygame.image.load('data/box in dock_2.png')
            charecter_on_dock = pygame.image.load('data/charecter on dock_2.png')

        pygame.init()
        pygame.mixer.music.load('data/music_1.mp3')
        level = load_level(number, name)
        size = window_size(level)
        screen = pygame.display.set_mode(size)
        running = True
        while running:
            draw_map(Sokoban(level).levels, screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    parent.close()
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        Sokoban(level).move_character(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        Sokoban(level).move_character(1, 0)
                    elif event.key == pygame.K_UP:
                        Sokoban(level).move_character(0, -1)
                    elif event.key == pygame.K_DOWN:
                        Sokoban(level).move_character(0, 1)
                    elif event.key == pygame.K_r:
                        Sokoban(level).level_reset(load_level(number, name))
                    elif event.key == pygame.K_q:
                        running = False
                        parent.show()
            pygame.display.update()
            if Sokoban(level).level_complet():
                tac = time.perf_counter()
                print('level completed')
                new_time = float(f'{tac - tic:0.2f}')
                con = sqlite3.connect('records.sqlite')
                cur = con.cursor()
                old_time = cur.execute(f'''SELECT level_time FROM time WHERE id = "{number}"''').fetchone()[0]
                print(old_time)
                print(new_time)
                if old_time != '-':
                    if float(new_time) < float(old_time):
                        cur.execute('''UPDATE time SET level_time = ? WHERE id = ?''', (new_time, number))
                        draw_game_over(new_time, new_time)
                    else:
                        draw_game_over(old_time, new_time)
                else:
                    cur.execute('''UPDATE time SET level_time = ? WHERE id = ?''', (new_time, number))
                    draw_game_over('-', new_time)
                con.commit()
                pygame.mixer.music.pause()
                parent.show()
                running = False
        pygame.quit()
