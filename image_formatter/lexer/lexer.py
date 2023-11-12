from image_formatter.lexer.token import Token, TokenType, IntegerToken
from image_formatter.lexer.position import Position
import io
import sys
from mkdocs.plugins import get_plugin_logger
from copy import deepcopy

log = get_plugin_logger(__name__)


class Lexer:
    """
    Class representing Lexer.
    Responsible for going through the characters from source input one by one and
    - returning valid tokens
    - omitting unimportant parts
    """

    curr_char = ""

    def __init__(
        self,
        fp: io.TextIOWrapper,
        *,
        max_int: int = sys.maxsize,
        special_signs: tuple = ("-", "_"),
        tag: str = "@",
        newline_characters: tuple = ("\n", "\r"),
    ):
        """
        Args:
            fp: file pointer to open file for reading
        Kwargs:
            max_int: defines integer maximal value that the lexer can build
            special_signs: defines which special signs can be used in strings
            tag: defines character that is used to find image tags
            newline_characters: defines which characters should be treated as newlines

        running: defines if lexer should still go through the characters or EOF was encountered
        """
        self.fp = fp
        self.running = True
        self.current_position = Position(1, 0)
        self.max_int = max_int
        self.tag = tag
        self.special_signs = special_signs
        self.newline_characters = newline_characters

    @staticmethod
    def name() -> str:
        return __class__.__name__

    def is_character(self) -> bool:
        """
        Checks for valid character in literal

        Returns:
            True if the string is alphanumeric or among the valid special signs
            False otherwise
        """
        return self.curr_char.isalnum() or self.curr_char in self.special_signs

    def next_char(self) -> None:
        """
        Takes next character from the stream.
        If there are no more characters to read, the flag running is set to False -
        lexer finished all work.
        """
        self.curr_char = self.fp.read(1)
        self._update_current_position()
        if not self.curr_char:
            self.running = False

    def _update_current_position(self) -> None:
        """
        Updates lexer position in the text / text stream.
        """
        if self.curr_char in self.newline_characters:
            self.current_position.move_to_next_line()
        else:
            self.current_position.move_right()

    def build_char(self) -> Token | None:
        """
        Tries to build a character token.
        It includes all characters and only whitespaces are omitted.

        Returns:
            Appropriate token of type T_CHAR if completed successfully,
            None if the whitespace is encountered
        """
        if self.curr_char.isspace():
            self.next_char()
            return None
        char = self.curr_char
        position = deepcopy(self.current_position)
        self.next_char()
        return Token(TokenType.T_CHAR, position, char)

    def build_literal(self) -> Token | None:
        """
        Tries to build a literal token according to:
        literal = letter, { letter | literal_special_sign | digit }

        Returns:
            Appropriate token of type T_LITERAL if completed successfully,
            Otherwise the return from build_char
        """
        if not self.curr_char.isalpha():
            return self.build_char()
        literal = self.curr_char
        position = deepcopy(self.current_position)
        self.next_char()
        while self.is_character():
            literal += self.curr_char
            self.next_char()
        return Token(TokenType.T_LITERAL, position, literal)

    def build_integer(self) -> IntegerToken | None:
        """
        Tries to build an integer token according to:
        integer         = zero_digit | (non_zero_digit, { digit })
        digit           = zero_digit | non_zero_digit
        non_zero_digit  = 1..9
        zero_digit      = 0

        Returns:
            Appropriate token of type T_INTEGER if completed successfully,
            Otherwise the returns None
        """
        log.info(f"{Lexer.name()}: Trying to build an integer.")
        if not self.curr_char.isdigit():
            log.info(f"{Lexer.name()}: Failed to build an integer. No digit provided.")
            return None
        number = int(self.curr_char)
        position = deepcopy(self.current_position)
        self.next_char()
        if number != 0:
            while self.curr_char.isdigit() and self._is_number_in_range(number):
                number = number * 10 + int(self.curr_char)
                self.next_char()
        log.info(f"{Lexer.name()}: Integer built successfully. Returning 'T_INTEGER' token.")
        return IntegerToken(TokenType.T_INTEGER, position, number)

    def _is_number_in_range(self, number):
        return number * 10 + int(self.curr_char) <= self.max_int

    def build_tag(self) -> Token | None:
        """
        Tries to build an image tag token according to:
        image_size_tag = '@', literal

        Returns:
            Appropriate token of type T_IMAGE_SIZE_TAG if completed successfully,
            None if the tag cannot be built
        """
        log.info("Trying to build a tag.")
        if not self.curr_char == self.tag:
            log.info(f"{Lexer.name()}: Failed to build a tag. Missing '{self.tag}'.")
            return None
        position = deepcopy(self.current_position)
        self.next_char()
        token = self.build_literal()
        if token.type != TokenType.T_LITERAL:
            log.info(f"{Lexer.name()}: Failed to build a tag. Missing token 'T_LITERAL'.")
            return None
        log.info(f"{Lexer.name()}: Tag built successfully. Returning 'T_IMAGE_SIZE_TAG' token.")
        return Token(TokenType.T_IMAGE_SIZE_TAG, position, token.string)

    def get_url_ending(self, string: str) -> str | None:
        """
        Gets the remaining part of url after the first dot (dot is required at least once in an url)

        Args:
            string: first part of to-be url

        Returns:
            string: complete url
            None: in case url cannot be built
        """
        log.info(f"{Lexer.name()}: Trying to build an url ending.")
        if self.curr_char != ".":
            log.info(f"{Lexer.name()}: Failed to build an url ending. Missing '.'.)")
            return None
        string += self.curr_char
        self.next_char()
        while self.is_character() or self.curr_char in ["/", "."]:
            string += self.curr_char
            self.next_char()
        log.info(f"{Lexer.name()}: Url ending built successfully.")
        return string

    def build_url(self) -> Token | None:
        """
        Tries to build an url token according to:
        image_url = '(', { '/' | '.' | literal}, '.', literal, ')'

        Returns:
            Appropriate token of type T_IMAGE_URL if completed successfully,
            None if the url cannot be built
        """
        log.info(f"{Lexer.name()}: Trying to build an url.")
        if not self.curr_char == "(":
            log.info(f"{Lexer.name()}: Failed to build an url. Missing '('.)")
            return None
        position = deepcopy(self.current_position)
        self.next_char()
        string = ""
        while self.is_character() or self.curr_char == "/":
            string += self.curr_char
            self.next_char()
        if not (string := self.get_url_ending(string)):
            log.info(f"{Lexer.name()}: Failed to build an url. Missing url ending.)")
            return None
        if not self.curr_char == ")":
            log.info(f"{Lexer.name()}: Failed to build an url. Missing ')'.)")
            return None
        self.next_char()
        log.info(f"{Lexer.name()}: Image url built successfully. Returning 'T_IMAGE_URL' token.")
        return Token(TokenType.T_IMAGE_URL, position, string)

    def get_token(self) -> Token:
        """
        Gets next token.
        If the end of file was encountered (running is False) will return EOF token.

        Returns:
            Appropriate token
        """
        if self.running:
            # watch out, the below works starting Python 3.8
            log.info(f"{Lexer.name()}: Fetching next token.")
            if (
                (token := self.build_tag())
                or (token := self.build_url())
                or (token := self.build_integer())
                or (token := self.build_literal())
            ):
                log.info(f"{Lexer.name()}: Token {token.type} returned with content: '{token.string}'.")
                return token
        else:
            log.info(f"{Lexer.name()}: Lexer finished work. Returning 'T_EOF' token.")
            return Token(TokenType.T_EOF, self.current_position)
