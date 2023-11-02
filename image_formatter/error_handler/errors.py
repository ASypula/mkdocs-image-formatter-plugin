from image_formatter.lexer.token import TokenType


class UnexpectedTagException(Exception):
    def __init__(self, expected: TokenType, actual: TokenType):
        super(UnexpectedTagException, self)
        self.expected = expected
        self.actual = actual

    def __str__(self):
        return f"{self.__class__}: expected token of type {self.expected} but received {self.actual}"

    def __eq__(self, other):
        if other.__class__ != self.__class__:
            return False

        if (self.expected == other.expected) and (self.actual == other.actual):
            return True
        return False
