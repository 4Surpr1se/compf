#!/usr/bin/env python3

import re
from stack import Stack


class Compf:
    """
    Стековый компилятор формул преобразует правильные
    арифметические формулы (цепочки языка, задаваемого
    грамматикой G0) в программы для стекового калькулятора
    (цепочки языка, определяемого грамматикой Gs):

    G0:
        F  ->  T  |  F+T  |  F-T
        T  ->  M  |  T*M  |  T/M
        M  -> (F) |   V
        V  ->  a  |   b   |   c   |  ...  |    z

    Gs:
        e  ->  e e + | e e - | e e * | e e / |
                     | a | b | ... | z
    В качестве операндов в формулах допустимы только
    однобуквенные имена переменных [a-z]
    """

    SYMBOLS = re.compile("[a-z]")

    def __init__(self):
        # Создание стека отложенных операций
        self.s = Stack()
        # Создание списка с результатом компиляции
        self.data = []

    def compile(self, str):
        self.data.clear()
        # Последовательный вызов для всех символов
        # взятой в скобки формулы метода process_symbol
        for c in '[' + str + ']':  # Добавляем специальные скобки в начале и конце,
            # не используем ( или <, потому что иначе будет ошибка подниматься в is_precedes, добавить отдельные скобки,
            # для которых не будет проверки на миссматч, самое простое решение этой проблемы
            self.process_symbol(c)
        return " ".join(self.data)

    # Обработка символа
    def process_symbol(self, c):
        """
        Здесь просто добавляем в пул скобок угловые и квадратные,
        проверку на соответсвие кругловых и угловых будет происходить в is_precedes,
        """
        if c in "(<[":
            self.s.push(c)
        elif c in ")>]":
            self.process_suspended_operators(c)
            self.s.pop()
        elif c in "+-*/":
            self.process_suspended_operators(c)
            self.s.push(c)
        else:
            self.check_symbol(c)
            self.process_value(c)

    # Обработка отложенных операций
    def process_suspended_operators(self, c):
        while not self.s.is_empty() and self.is_precedes(self.s.top(), c):
            self.process_oper(self.s.pop())

    # Обработка имени переменной
    def process_value(self, c):
        self.data.append(c)

    # Обработка символа операции
    def process_oper(self, c):
        self.data.append(c)

    # Проверка допустимости символа
    @classmethod
    def check_symbol(self, c):
        if not self.SYMBOLS.match(c):
            raise Exception(f"Недопустимый символ '{c}'")

    # Определение приоритета операции
    @staticmethod
    def priority(c):
        return 1 if (c == "+" or c == "-") else 2

    # Определение отношения предшествования
    @staticmethod
    def is_precedes(a, b):
        """
        Добавили простую проверку на миссматч скобок.
        По итогу поведение угловых скобок полностью копирует поведение круглых,
        просто добавляем проверку на не совпадение
        """
        if (a == '(' and b == '>') or (a == '<' and b == ')'):
            raise Exception(f'Mismatch between {a} and {b}')
        if a in "(<[":
            return False
        elif b in ")>]":
            return True
        else:
            return Compf.priority(a) >= Compf.priority(b)


if __name__ == "__main__":
    c = Compf()
    while True:
        str = input("Арифметическая  формула: ")
        print(f"Результат её компиляции: {c.compile(str)}")
        print()
