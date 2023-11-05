from enum import Enum


class TokenType(Enum):
    """
    Class representing available token types.
    """

    T_LITERAL = 0
    T_IMAGE_URL = 1
    T_IMAGE_SIZE_TAG = 2
    T_CHAR = 3
    T_INTEGER = 4
    T_EOF = 5


class Token:
    """
    Class representing token.
    """

    def __init__(self, type: TokenType, string: str = ""):
        """
        Args:
            type: type of the token
            string: final version of token's text (additional characters e.g. '@' from tag is removed)
        """
        self.type = type
        self.string = string


class IntegerToken(Token):
    """
    Class representing token of type int.
    """

    def __init__(self, type: TokenType, integer: int):
        super(IntegerToken, self).__init__(type, str(integer))
        self.integer = integer
