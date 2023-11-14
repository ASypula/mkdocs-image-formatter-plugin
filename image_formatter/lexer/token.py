from enum import Enum

from image_formatter.lexer.position import Position


class TokenType(Enum):
    """
    Class representing available token types.
    """

    T_LITERAL = 0
    T_IMAGE_URL = 1
    T_IMAGE_SIZE_TAG = 2
    T_CHAR = 3
    T_INTEGER = 4
    T_WHITE_CHAR = 5
    T_EOF = 6


class Token:
    """
    Class representing token.
    """

    def __init__(self, type: TokenType, position: Position, string: str = ""):
        """
        Args:
            type: type of the token
            position: position of the first character of the token
            string: final version of token's text (additional characters e.g. '@' from tag is removed)
        """
        self.type = type
        self.position = position
        self.string = string


class IntegerToken(Token):
    """
    Class representing token of type int.
    """

    def __init__(self, type: TokenType, position: Position, integer: int):
        """
        Args:
            type: type of the token
            position: position of the first character of the token
            integer: int value of the token
        """
        super(IntegerToken, self).__init__(type, position, str(integer))
        self.integer = integer
