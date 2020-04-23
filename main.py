"""
    2048GAME Python Version
    Written in python=3.7
    Core Version=3
    Copyright @ JSY 2019-2020. All rights reserved.
    2020.3.7    13:50   V4.0.0
                15:53   V4.0.1
"""
import copy
import msvcrt
import os
import random
import time

CORE_VERSION = 3
LEFT = 1
RIGHT = 4
UP = 2
DOWN = 3
VOID = 0
ERROR = -1


class Board:
    __board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    __emptyCoorNum = 16
    __emptyCoorList = []
    __score = 0
    __max = 0
    __steps = 0

    def clear(self):
        self.__board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.__score = self.__max = self.__steps = 0
        self.__emptyCoorNum = 16
        self.__emptyCoorList = []
        for i in range(4):
            for j in range(4):
                self.__emptyCoorList.append([i, j])

    def initialize(self):
        self.addNum()
        self.addNum()

    def gameOver(self):
        if self.__emptyCoorNum:
            return False
        else:
            for i in range(3):
                for j in range(3):
                    if self.__board[i][j] == self.__board[i][j + 1] \
                            and self.__board[i][j] == self.__board[i + 1][j]:
                        return False
            for i in range(3):
                if self.__board[i][3] == self.__board[i + 1][3]:
                    return False
            for j in range(3):
                if self.__board[3][j] == self.__board[3][j + 1]:
                    return False
        return True

    def move(self, dir):
        isValidMove = False
        preboard = copy.deepcopy(self.__board)
        if dir == b'a':
            for i in range(4):
                self.__board[i] = self.__move(self.__board[i])
        elif dir == b'd':
            for i in range(4):
                b = self.__board[i].copy()
                b.reverse()
                b = self.__move(b)
                b.reverse()
                self.__board[i] = b
        elif dir == b'w':
            a = []
            for i in range(4):
                a.append(self.__move(
                    [self.__board[0][i], self.__board[1][i], self.__board[2][i], self.__board[3][i]]))
            for i in range(4):
                for j in range(4):
                    self.__board[j][i] = a[i][j]
        elif dir == b's':
            a = []
            for i in range(4):
                b = self.__move([self.__board[3][i], self.__board[2][i], self.__board[1][i], self.__board[0][i]])
                b.reverse()
                a.append(b)
            for i in range(4):
                for j in range(4):
                    self.__board[j][i] = a[i][j]

        for i in range(4):
            for j in range(4):
                if preboard[i][j] != self.__board[i][j]:
                    isValidMove = True
                    break
            if isValidMove:
                break

        if isValidMove:
            self.__steps += 1
            self.__emptyCoorList.clear()
            self.__emptyCoorNum = 0
            for i in range(4):
                for j in range(4):
                    if not self.__board[i][j]:
                        self.__emptyCoorList.append([i, j])
                        self.__emptyCoorNum += 1
        return isValidMove

    def __move(self, arr):
        # This is the core of the moving algorithm. Version=3
        # ----------------Move----------------
        for j in range(3):
            if not arr[j]:
                k = p = 1
                while k + j < 4:
                    if not arr[k + j]:
                        p += 1
                    else:
                        break
                    k += 1
                if p + j == 4:
                    break
                for k in range(j + p, 4):
                    arr[k - p] = arr[k]
                for k in range(p, 0, -1):
                    arr[4 - k] = 0
        # ----------------Merge----------------
        for j in range(3):
            if arr[j] and arr[j] == arr[j + 1]:
                arr[j] += 1
                self.__score += self.__getRealValue(arr[j])
                if arr[j] > self.__max:
                    self.__max = arr[j]
                for k in range(j + 2, 4):
                    arr[k - 1] = arr[k]
                arr[3] = 0
        return arr

    def addNum(self):
        rand_num = random.randint(0, self.__emptyCoorNum - 1)
        c = self.__emptyCoorList[rand_num]
        self.__board[c[0]][c[1]] = 1 if random.randint(0, 9) < 9 else 2
        self.__emptyCoorNum -= 1
        self.__emptyCoorList.pop(rand_num)

    def printBoard(self):  # print
        for i in range(4):
            for j in range(4):
                if self.__board[i][j]:
                    print("|%6d|" % (self.__getRealValue(self.__board[i][j])), end='')
                else:
                    print("|      |", end='')
            print()
        print("steps=%6d     score=%8d" % (self.__steps, self.__score))

    def __getRealValue(self, i):
        return 1 << i if i else 0


random.seed(time.process_time())
b = Board()
while True:
    b.clear()
    b.initialize()
    b.printBoard()
    while not b.gameOver():
        if b.move(msvcrt.getch()):
            os.system('cls')
            b.addNum()
            b.printBoard()
        else:
            print("VOID!")
