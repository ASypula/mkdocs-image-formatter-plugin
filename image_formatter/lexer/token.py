from enum import Enum


class TokenType(Enum):
    T_LITERAL = 0
    T_IMAGE_URL = 1
    T_IMAGE_SIZE_TAG = 2
    T_EOF = 3


class Token:
    def __init__(self, type: TokenType, string: str = ""):
        self.type = type
        self.string = string
