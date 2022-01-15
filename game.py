import pygame
import random
import numpy as np
import copy
from rectangle_recognition import Get_rectangle
from enum import Enum

black = (0, 0, 0)
white = (250, 240, 250)
riverBlue = '#104BEF'
colors = [
    '#D9534F', '#072227', '#35858B',
    '#1F9960', '#557C55', '#CA5F6A',
    '#FFC900', '#086E7D', '#4A5F7A',
    '#A267AC', '#4C0027', '#B3541E',
    '#4FBDBA', '#CE7BB0', '#7A9EBC',
    '#2F3A8F', '#6867AC', '#72A9DD',
    '#9B0000', '#98AE0D', '#EF2F88',
]


class GameState(Enum):
    SELECT_RECTANGLE = 1
    SELECT_STRATEGY = 2
    GAME_OVER = 3


SQUARE_SIZE = 50
MARGIN = 3
SIZE = 10
DICE_MARGIN = SQUARE_SIZE

pygame.init()
font = pygame.font.SysFont('Arial', 15)
large = pygame.font.SysFont('Arial', 30)
bold = pygame.font.SysFont('Arial', 30, bold=True, italic=True)

TREE = 'TR'
FOX = 'FX'
BIRD = 'BD'
TWIG = 'TW'
SNOW = 'SN'
ICE = 'IC'
LEAF = 'LE'
ELK = 'EL'
FLOWER = 'FL'

enumerate


class BlaetterrauschenGame:
    def __init__(self, w=640, h=480):
        self.w = SIZE*SQUARE_SIZE + (SIZE+1) * MARGIN
        self.h = SIZE*SQUARE_SIZE + (SIZE+1) * MARGIN + 200
        # init display
        self.scr = pygame.display.set_mode((self.w, self.h + DICE_MARGIN))
        pygame.display.set_caption('Blätterrauschen')
        self.clock = pygame.time.Clock()

        self.columnStart = None
        self.columnEnd = None
        self.rowStart = None
        self.rowEnd = None

        # init game state
        self.done = False
        self.startPoint = random.randint(1, 6)
        self.grid = [
            # row 1
            [[ELK, 0, 0], [TREE, 0, 0], [TREE, 0, 0], [SNOW, 0, 0], [TREE, 0, 0], [
                ICE, 0, 0], [FLOWER, 0, 0], [ELK, 0, 0], [LEAF, 0, 0], [ICE, 0, 0]],
            # row 2
            [[TWIG, 0, 0], [1, int(1 == self.startPoint), 0], [TREE, 0, 0], [FOX, 0, 0], [BIRD, 0, 0], [
                TREE, 0, 0], [TREE, 0, 0], [TREE, 0, 0], [4, int(4 == self.startPoint), 0], [FLOWER, 0, 0]],
            # row 3
            [[TREE, 0, 0], [ELK, 0, 0], [FOX, 0, 0], [FLOWER, 0, 0], [FLOWER, 0, 0], [
                ELK, 0, 0], [SNOW, 0, 0], [TREE, 0, 0], [LEAF, 0, 0], [TREE, 0, 0]],
            # row 4
            [[ICE, 0, 0], [BIRD, 0, 0], [TREE, 0, 0], [ELK, 0, 0], [ICE, 0, 0], [
                FOX, 0, 0], [TWIG, 0, 0], [ICE, 0, 0], [ELK, 0, 0], [LEAF, 0, 0]],
            # row 5
            [[TREE, 0, 0], [LEAF, 0, 0], [2, int(2 == self.startPoint), 0], [TREE, 0, 0], [FOX, 0, 0], [
                ICE, 0, 0], [LEAF, 0, 0], [5, int(5 == self.startPoint), 0], [BIRD, 0, 0], [SNOW, 0, 0]],
            # row 6
            [[SNOW, 0, 0], [FLOWER, 0, 0], [SNOW, 0, 0], [FOX, 0, 0], [FLOWER, 0, 0], [
                LEAF, 0, 0], [FOX, 0, 0], [TREE, 0, 0], [FLOWER, 0, 0], [TREE, 0, 0]],
            # row 7
            [[TREE, 0, 0], [ELK, 0, 0], [TREE, 0, 0], [TWIG, 0, 0], [TREE, 0, 0], [
                LEAF, 0, 0], [FOX, 0, 0], [FLOWER, 0, 0], [ICE, 0, 0], [TWIG, 0, 0]],
            # row 8
            [[ICE, 0, 0], [BIRD, 0, 0], [SNOW, 0, 0], [TREE, 0, 0], [TREE, 0, 0], [
                FOX, 0, 0], [TREE, 0, 0], [BIRD, 0, 0], [TREE, 0, 0], [ELK, 0, 0]],
            # row 9
            [[TREE, 0, 0], [3, int(3 == self.startPoint), 0], [ICE, 0, 0], [TREE, 0, 0], [FOX, 0, 0], [
                ELK, 0, 0], [FOX, 0, 0], [TREE, 0, 0], [6, int(6 == self.startPoint), 0], [TWIG, 0, 0]],
            # row 10
            [[ELK, 0, 0], [ICE, 0, 0], [FLOWER, 0, 0], [LEAF, 0, 0], [TREE, 0, 0], [
                TREE, 0, 0], [SNOW, 0, 0], [TREE, 0, 0], [FLOWER, 0, 0], [SNOW, 0, 0]]
        ]

        self.n_round = 0
        self.n_cloud = 0
        self.strategies = []
        self.state = GameState.SELECT_RECTANGLE
        self.leaf_dice_result = None

        self.score = {key: 0 for key in (
            TREE, FOX, BIRD, ICE, LEAF, ELK, FLOWER, 'RIVER', 'SKIP')}
        self.counters = {key: 0 for key in (
            TREE, FOX, BIRD, TWIG, ICE, LEAF, ELK, FLOWER, ELK, 'RIVER')}
        self.hasUsedJoker = False

        self.turn()

    def rollDice(self):
        result = ((random.randint(1, 6)) % 4) + 1
        if result == 2:
            self.n_cloud += random.randint(0, 1)
        return result

    def drawUi(self):
        self.scr.fill(black)
        for row in range(10):
            for column in range(10):
                color = colors[self.grid[row][column][1] % len(
                    colors)] if self.grid[row][column][1] != 0 else white
                pygame.draw.rect(self.scr,
                                 color,
                                 [(MARGIN + SQUARE_SIZE) * column + MARGIN,
                                  (MARGIN + SQUARE_SIZE) *
                                  row + MARGIN + DICE_MARGIN,
                                  SQUARE_SIZE,
                                  SQUARE_SIZE])
                textColor = white if self.grid[row][column][1] > 0 else black
                text = large.render(str(self.grid[row][column][0]), True, textColor) if self.grid[row][column][2] == 0 else bold.render(
                    str(self.grid[row][column][0]), True, textColor)
                self.scr.blit(text, [(MARGIN + SQUARE_SIZE) * column +
                                     MARGIN, (MARGIN + SQUARE_SIZE) * row + MARGIN + DICE_MARGIN])

        txt = str(self.diceResult) if self.state != GameState.GAME_OVER else 'Dice result for leaf score: ' + \
            str(self.leaf_dice_result)
        self.scr.blit(font.render(txt, True, white),
                      [0 + DICE_MARGIN / 5, 0 + DICE_MARGIN / 5])
        self.scr.blit(font.render('Round: ' + str(self.n_round), True, white),
                      [0 + DICE_MARGIN / 5, 0 + DICE_MARGIN / 1.6])
        if self.state != GameState.GAME_OVER:
            self.scr.blit(font.render(str(self.state), True, white),
                          [70, 0 + DICE_MARGIN / 5])
        if self.state == GameState.GAME_OVER:
            self.scr.blit(font.render('Score: ' + str(sum(self.score.values())), True, white),
                          [self.w - 120, 0 + DICE_MARGIN / 5])

        # render points
        h = (200 - 3 * MARGIN) / 3
        w = 2 * SQUARE_SIZE + MARGIN

        pygame.draw.rect(self.scr, white, [
                         MARGIN, self.h - 200 + SQUARE_SIZE, w, h])
        self.scr.blit(font.render(TREE + ': ' + str(self.counters[TREE]), True, black),
                      [2 * MARGIN, self.h - 200 + SQUARE_SIZE + h / 6])
        self.scr.blit(font.render('Score: ' + str(self.score[TREE]), True, black),
                      [2 * MARGIN, self.h - 200 + SQUARE_SIZE + h / 2])
        pygame.draw.rect(self.scr, white, [
                         MARGIN, self.h - 200 + h + MARGIN + SQUARE_SIZE, w, h])
        self.scr.blit(font.render(FOX + ': ' + str(self.counters[FOX]), True, black),
                      [2 * MARGIN, self.h - 200 + h + MARGIN + SQUARE_SIZE + h / 6])
        self.scr.blit(font.render('Score: ' + str(self.score[FOX]), True, black),
                      [2 * MARGIN, self.h - 200 + h + MARGIN + SQUARE_SIZE + h / 2])
        pygame.draw.rect(self.scr, white, [
                         MARGIN, self.h - 200 + 2 * (h + MARGIN) + SQUARE_SIZE, w, h])
        self.scr.blit(font.render(BIRD + '/' + TWIG + ': ' + str(self.counters[BIRD]) + '/' + str(self.counters[TWIG]), True, black),
                      [2 * MARGIN, self.h - 200 + 2 * (h + MARGIN) + SQUARE_SIZE + h / 6])
        self.scr.blit(font.render('Score: ' + str(self.score[BIRD]), True, black),
                      [2 * MARGIN, self.h - 200 + 2 * (h + MARGIN) + SQUARE_SIZE + h / 2])

        pygame.draw.rect(self.scr, white, [
                         w + 2 * MARGIN, self.h - 200 + SQUARE_SIZE, w, h])
        self.scr.blit(font.render(ICE + ': ' + str(self.counters[ICE]), True, black),
                      [w + 3 * MARGIN, self.h - 200 + SQUARE_SIZE + h / 6])
        self.scr.blit(font.render('Score: ' + str(self.score[ICE]), True, black),
                      [w + 3 * MARGIN, self.h - 200 + SQUARE_SIZE + h / 2])
        pygame.draw.rect(self.scr, white, [
                         w + 2 * MARGIN, self.h - 200 + h + MARGIN + SQUARE_SIZE, w, h])
        self.scr.blit(font.render(LEAF + ': ' + str(self.counters[LEAF]), True, black),
                      [w + 3 * MARGIN, self.h - 200 + h + MARGIN + SQUARE_SIZE + h / 6])
        self.scr.blit(font.render('Score: ' + str(self.score[LEAF]), True, black),
                      [w + 3 * MARGIN, self.h - 200 + h + MARGIN + SQUARE_SIZE + h / 2])
        pygame.draw.rect(self.scr, white, [
                         w + 2 * MARGIN, self.h - 200 + 2 * (h + MARGIN) + SQUARE_SIZE, w, h])
        self.scr.blit(font.render(ELK + ': ' + str(self.counters[ELK]) + ' of 10', True, black),
                      [w + 3 * MARGIN, self.h - 200 + 2 * (h + MARGIN) + SQUARE_SIZE + h / 6])
        self.scr.blit(font.render('Score: ' + str(self.score[ELK]), True, black),
                      [w + 3 * MARGIN, self.h - 200 + 2 * (h + MARGIN) + SQUARE_SIZE + h / 2])

        pygame.draw.rect(self.scr, white, [
                         2 * w + 3 * MARGIN, self.h - 200 + SQUARE_SIZE, w, h])
        self.scr.blit(font.render(FLOWER + ': ' + str(self.counters[FLOWER]), True, black),
                      [2 * w + 4 * MARGIN, self.h - 200 + SQUARE_SIZE + h / 6])
        self.scr.blit(font.render('Score: ' + str(self.score[FLOWER]), True, black),
                      [2 * w + 4 * MARGIN, self.h - 200 + SQUARE_SIZE + h / 2])
        pygame.draw.rect(self.scr, white, [
                         2 * w + 3 * MARGIN, self.h - 200 + h + MARGIN + SQUARE_SIZE, w, h])
        self.scr.blit(font.render('Clouds: ' + str(self.n_cloud), True, black),
                      [2 * w + 4 * MARGIN, self.h - 200 + h + MARGIN + SQUARE_SIZE + h / 6])
        pygame.draw.rect(self.scr, white, [
                         2 * w + 3 * MARGIN, self.h - 200 + 2 * (h + MARGIN) + SQUARE_SIZE, w, h])
        self.scr.blit(font.render('River: ' + str(self.counters['RIVER']), True, black),
                      [2 * w + 4 * MARGIN, self.h - 200 + 2 * (h + MARGIN) + SQUARE_SIZE + h / 6])
        self.scr.blit(font.render('Score: ' + str(self.score['RIVER']), True, black),
                      [2 * w + 4 * MARGIN, self.h - 200 + 2 * (h + MARGIN) + SQUARE_SIZE + h / 2])

        pygame.draw.rect(self.scr, white, [
                         3 * w + 4 * MARGIN, self.h - 200 + SQUARE_SIZE, w * 2 + MARGIN, h])
        self.scr.blit(font.render('Skip penalty: ' + str(self.score['SKIP']), True, black),
                      [3 * w + 5 * MARGIN, self.h - 200 + SQUARE_SIZE + h / 6])
        pygame.draw.rect(self.scr, white, [
                         3 * w + 4 * MARGIN, self.h - 200 + 2 * (h + MARGIN) + SQUARE_SIZE, w * 2 + MARGIN, h])
        self.scr.blit(font.render('Joker used: ' + str(self.hasUsedJoker), True, black),
                      [3 * w + 5 * MARGIN, self.h - 200 + 2 * (h + MARGIN) + SQUARE_SIZE + h / 6])

        pygame.draw.rect(self.scr, white, [
                         3 * w + 4 * MARGIN, self.h - 200 + h + MARGIN + SQUARE_SIZE, w * 2 + MARGIN, h])

        # draw river
        pygame.draw.rect(self.scr, riverBlue, [
            4 * (SQUARE_SIZE + MARGIN) - MARGIN / 1.5, DICE_MARGIN + MARGIN, 2 * MARGIN, 5 * (SQUARE_SIZE + MARGIN)])
        pygame.draw.rect(self.scr, riverBlue, [
            4 * (SQUARE_SIZE + MARGIN), DICE_MARGIN + MARGIN + 5 * (SQUARE_SIZE + MARGIN) - MARGIN / 1.5, 2 * (SQUARE_SIZE + MARGIN), 2 * MARGIN])
        pygame.draw.rect(self.scr, riverBlue, [
            6 * (SQUARE_SIZE + MARGIN) - MARGIN / 1.5, DICE_MARGIN + MARGIN + 5 * (SQUARE_SIZE + MARGIN), 2 * MARGIN, 5 * (SQUARE_SIZE + MARGIN)])

        self.clock.tick(50)
        pygame.display.flip()

    def turn(self, skipTurn=False):
        if skipTurn:
            if self.hasUsedJoker:
                self.score['SKIP'] -= 3
            else:
                self.hasUsedJoker = True
        self.n_round += 1

        self.diceResult = [self.rollDice(), self.rollDice()]
        self.state = GameState.SELECT_RECTANGLE
        self.drawUi()

    def calcScore(self):
        n_elk_total = 0
        n_ice_total = 0
        n_leaf_total = 0
        n_flower_total = 0
        for strategy, rows, columns in self.strategies:
            counts = {key: 0 for key in (
                TREE, SNOW, FOX, BIRD, TWIG, ICE, LEAF, FLOWER, ELK)}
            for x in range(min(rows), max(rows) + 1):
                for y in range(min(columns), max(columns) + 1):
                    cell = self.grid[x][y]
                    if cell[0] in counts.keys():
                        counts[cell[0]] += 1

            n_elk_total += counts[ELK]
            if strategy == FOX and counts[FOX] == 1:
                self.score[FOX] += 3
            elif strategy == TREE and counts[SNOW] >= 1:
                self.score[TREE] += counts[TREE]
            elif strategy == BIRD:
                self.score[BIRD] += min(counts[BIRD], counts[TWIG]) * 5
            elif strategy == LEAF:
                n_leaf_total += counts[LEAF]
            elif strategy == ICE:
                n_ice_total += counts[ICE]
            elif strategy == FLOWER:
                n_flower_total += counts[FLOWER]

        if n_ice_total == 5:
            self.score[ICE] += 15
        if n_flower_total >= self.n_cloud:
            self.score[FLOWER] += 3 * n_flower_total
        if n_elk_total == 10:
            self.score[ELK] += 12

        self.leaf_dice_result = random.randint(1, 4)
        self.score[LEAF] += n_leaf_total * self.leaf_dice_result

    def selectRect(self):
        # check if rectangle is of the correct size
        selectedRectSize = (abs(self.columnStart - self.columnEnd) +
                            1) * (abs(self.rowStart - self.rowEnd) + 1)
        expectedRectSize = np.prod(self.diceResult)
        if selectedRectSize != expectedRectSize:
            return

        gridCopy = copy.deepcopy(self.grid)
        isFirstRound = self.n_round == 1
        includesStartPoint = False
        for x in range(min(self.rowStart, self.rowEnd), max(self.rowStart, self.rowEnd) + 1):
            for y in range(min(self.columnStart, self.columnEnd), max(self.columnStart, self.columnEnd) + 1):
                cell = gridCopy[x][y]
                isStartPoint = isFirstRound and cell[0] == self.startPoint
                includesStartPoint = includesStartPoint or isStartPoint

                # check if the rectangle overlaps with others
                if cell[1] != 0 and not isStartPoint:
                    return

                cell[1] = self.n_round

        if isFirstRound and not includesStartPoint:
            return
        self.grid = gridCopy
        if self.isCrossingRiver():
            self.counters['RIVER'] += 1
        self.state = GameState.SELECT_STRATEGY
        self.drawUi()

    def selectStrategy(self, strategy):
        validStrategies = [TREE, FOX, FLOWER, ICE, BIRD, TWIG, LEAF]
        if strategy not in validStrategies:
            hasValidStrategies = False
            for x in range(min(self.rowStart, self.rowEnd), max(self.rowStart, self.rowEnd) + 1):
                for y in range(min(self.columnStart, self.columnEnd), max(self.columnStart, self.columnEnd) + 1):
                    cell = self.grid[x][y]
                    if cell[0] in validStrategies:
                        hasValidStrategies = True
            if hasValidStrategies:
                return

        self.strategies.append([strategy, [self.rowStart, self.rowEnd], [
                               self.columnStart, self.columnEnd]])
        for x in range(min(self.rowStart, self.rowEnd), max(self.rowStart, self.rowEnd) + 1):
            for y in range(min(self.columnStart, self.columnEnd), max(self.columnStart, self.columnEnd) + 1):
                cell = self.grid[x][y]
                if cell[0] in [strategy, ELK]:
                    cell[2] = 1
                    self.counters[cell[0]] += 1
                if cell[0] == SNOW and strategy == TREE:
                    cell[2] = 1
        self.turn()

    def isCrossingRiver(self):
        isCrossingTop = (min(self.columnStart, self.columnEnd) <= 3 < max(
            self.columnStart, self.columnEnd) and min(self.rowStart, self.rowEnd) <= 4)
        if isCrossingTop:
            return True
        isCrossingBottom = (min(self.columnStart, self.columnEnd) <= 5 < max(
            self.columnStart, self.columnEnd) and max(self.rowStart, self.rowEnd) > 4)
        if isCrossingBottom:
            return True
        isCrossingCenter = (min(self.rowStart, self.rowEnd) <= 4 < max(
            self.rowStart, self.rowEnd) and 4 <= min(self.columnStart, self.columnEnd) <= 5)
        if isCrossingCenter:
            return True
        return False


if __name__ == '__main__':
    game = BlaetterrauschenGame()

    # game loop
    while not game.done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.done = True
            elif event.type == pygame.MOUSEBUTTONDOWN and game.state == GameState.SELECT_RECTANGLE:
                pos = pygame.mouse.get_pos()
                game.columnStart = pos[0] // (SQUARE_SIZE + MARGIN)
                game.rowStart = ((pos[1]-DICE_MARGIN) //
                                 (SQUARE_SIZE + MARGIN))
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (SQUARE_SIZE + MARGIN)
                row = ((pos[1]-DICE_MARGIN) // (SQUARE_SIZE + MARGIN))

                if game.state == GameState.SELECT_RECTANGLE:
                    game.columnEnd = column
                    game.rowEnd = row
                    game.selectRect()
                elif game.state == GameState.SELECT_STRATEGY:
                    isRowInRange = row in range(
                        min(game.rowStart, game.rowEnd), max(game.rowStart, game.rowEnd) + 1)
                    isColumnInRange = column in range(min(game.columnStart, game.columnEnd), max(
                        game.columnStart, game.columnEnd) + 1)
                    if isRowInRange and isColumnInRange:
                        game.selectStrategy(game.grid[row][column][0])

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    game.turn(True)

                elif event.key == pygame.K_o:
                    print('game over')
                    game.calcScore()
                    game.state = GameState.GAME_OVER
                    game.drawUi()

    pygame.quit()
