from enum import Enum


class TokenType(Enum):
    """
    Class representing available token types.
    """

    T_LITERAL = 0
    T_IMAGE_URL = 1
    T_IMAGE_SIZE_TAG = 2
    T_EOF = 3


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
