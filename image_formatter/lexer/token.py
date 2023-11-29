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
    T_IMAGE_URL_WITH_PROPERTIES = 6
    T_EOF = 7


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

    def __eq__(self, other):
        if other.__class__ != self.__class__:
            return False

        return (self.position == other.position) and (self.string == other.string)


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


class TagToken(Token):
    """
    Class representing token of type tag.
    """

    def __init__(self, type: TokenType, position: Position, string: str = "", tag_character: str = ""):
        """
        Args:
            type: type of the token
            position: position of the first character of the token
            string: final version of token's text
            tag_character: characteristic character for the tag
        """
        super(TagToken, self).__init__(type, position, string)
        self.tag_character = tag_character
