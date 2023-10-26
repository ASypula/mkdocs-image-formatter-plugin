from image_formatter.lexer.token import Token, TokenType

SPECIAL_SIGNS = ["-", "_"]
TAG_CHAR = "@"


class Lexer:
    curr_char = ""

    def __init__(self, fp):
        self.fp = fp
        self.running = True

    @staticmethod
    def is_character(char: str) -> bool:
        return char.isalnum() or char in SPECIAL_SIGNS

    # TODO: a better way of taking next characters?
    def next_char(self) -> str:
        self.curr_char = self.fp.read(1)
        if not self.curr_char:
            self.running = False

    def build_literal(self):
        if not self.curr_char.isalpha():
            return 0
        literal = self.curr_char
        self.next_char()
        while Lexer.is_character(self.curr_char):
            literal += self.curr_char
            self.next_char()
        return Token(TokenType.T_LITERAL, literal)

    def build_tag(self):
        if not self.curr_char == TAG_CHAR:
            return 0
        self.next_char()
        token = self.build_literal()
        if token.type != TokenType.T_LITERAL:
            return 0
        return Token(TokenType.T_IMAGE_SIZE_TAG, token.string)

    def get_url_ending(self, string):
        if self.curr_char != ".":
            return 0
        string += self.curr_char
        self.next_char()
        while Lexer.is_character(self.curr_char) or self.curr_char in ["/", "."]:
            string += self.curr_char
            self.next_char()
        return string

    def build_url(self):
        if not self.curr_char == "(":
            return 0
        self.next_char()
        string = ""
        while Lexer.is_character(self.curr_char) or self.curr_char == "/":
            string += self.curr_char
            self.next_char()
        if not (string := self.get_url_ending(string)):
            return 0
        if not self.curr_char == ")":
            return 0
        self.next_char()
        return Token(TokenType.T_IMAGE_URL, string)

    def get_token(self):
        if self.running:
            # watch out, the below works starting Python 3.8
            if (
                (token := self.build_tag())
                or (token := self.build_url())
                or (token := self.build_literal())
            ):
                return token
        else:
            return Token(TokenType.T_EOF)
