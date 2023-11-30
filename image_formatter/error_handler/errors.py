from image_formatter.lexer.token import TokenType
from typing import List


class UnexpectedTagException(Exception):
    def __init__(self, expected: TokenType, actual: TokenType):
        super().__init__()
        self.expected = expected
        self.actual = actual

    def __str__(self):
        return f"{self.__class__}: expected token of type {self.expected} but received {self.actual}"

    def __eq__(self, other):
        if other.__class__ != self.__class__:
            return False

        return (self.expected == other.expected) and (self.actual == other.actual)


class InvalidConfigCharacterError(Exception):
    def __init__(self, invalid_char: str, valid_chars: List[str]):
        super().__init__()
        self.invalid_char = invalid_char
        self.valid_chars = valid_chars

    def __str__(self):
        return f"{self.__class__}: invalid character found: {self.invalid_char} when list of valid chars is: {self.valid_chars}"

    def __eq__(self, other):
        if other.__class__ != self.__class__:
            return False

        return (set(self.valid_chars == other.valid_chars)) and set((self.invalid_char == other.invalid_char))
