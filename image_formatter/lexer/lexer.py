from image_formatter.lexer.token import Token, TokenType, IntegerToken
from image_formatter.lexer.position import Position
from image_formatter.lexer.token_sequence import TokenSequence
import io
import sys
from mkdocs.plugins import get_plugin_logger
from copy import deepcopy

log = get_plugin_logger(__name__)


class Lexer(TokenSequence):
    """
    Class representing Lexer.
    Responsible for going through the characters from source input one by one and
    - returning valid tokens
    - omitting unimportant parts
    """

    def __init__(
        self,
        fp: io.TextIOWrapper,
        *,
        max_int: int = sys.maxsize,
        special_signs: tuple = ("-", "_"),
        tag: str = "@",
        newline_characters: tuple = ("\n", "\r"),
        additional_path_signs: tuple = ("/", "."),
    ):
        """
        Args:
            fp: file pointer to open file for reading

        Keyword Args:
            max_int: defines integer maximal value that the lexer can build
            special_signs: defines which special signs can be used in strings
            tag: defines character that is used to find image tags
            newline_characters: defines which characters should be treated as newlines
            additional_path_signs: defines which characters alongside letters could be used in url paths

        Attributes:
            running: defines if lexer should still go through the characters or EOF was encountered
        """
        self.fp = fp
        self.running = True
        self.current_char = ""
        self.current_position = Position(1, 1)
        self.max_int = max_int
        self.tag = tag
        self.special_signs = special_signs
        self.newline_characters = newline_characters  # @TODO add hypothesis tests
        self.additional_path_signs = additional_path_signs

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
        return self.current_char.isalnum() or self.current_char in self.special_signs

    def update_current_position(self) -> None:
        """
        Updates lexer position in the text / text stream.
        """
        if self.current_char:
            if self.current_char in self.newline_characters:
                self.current_position.move_to_next_line()
            else:
                self.current_position.move_right()

    def next_char(self) -> None:
        """
        Takes next character from the stream.
        If there are no more characters to read, the flag running is set to False -
        lexer finished all work.
        """
        self.update_current_position()
        self.current_char = self.fp.read(1)
        if not self.current_char:
            self.running = False

    def build_char(self) -> Token or None:
        """
        Tries to build a character token.
        It includes all characters and only whitespaces are omitted.

        Returns:
            Appropriate token of type T_CHAR if completed successfully,
            None if the whitespace is encountered
        """
        if self.is_current_char_white():
            return None
        char = self.current_char
        position = deepcopy(self.current_position)
        self.next_char()
        return Token(TokenType.T_CHAR, position, char)

    def build_white_char(self) -> Token or None:
        if not self.is_current_char_white():
            return None
        char = self.current_char
        position = deepcopy(self.current_position)
        self.next_char()
        return Token(TokenType.T_WHITE_CHAR, position, char)

    def is_current_char_white(self):
        return self.current_char.isspace() or self.current_char in self.newline_characters

    def build_literal(self) -> Token or None:
        """
        Tries to build a literal token according to:
        ```
        literal = letter, { letter | literal_special_sign | digit }
        ```

        Returns:
            Appropriate token of type T_LITERAL if completed successfully,
            Otherwise the return from build_char
        """
        if not self.current_char.isalpha():
            return self.build_char()
        literal = self.current_char
        position = deepcopy(self.current_position)
        self.next_char()
        while self.is_character():
            literal += self.current_char
            self.next_char()
        return Token(TokenType.T_LITERAL, position, literal)

    def build_integer(self) -> IntegerToken or None:
        """
        Tries to build an integer token according to:
        ```
        integer         = zero_digit | (non_zero_digit, { digit })
        digit           = zero_digit | non_zero_digit
        non_zero_digit  = 1..9
        zero_digit      = 0
        ```

        Returns:
            Appropriate token of type T_INTEGER if completed successfully,
            Otherwise the returns None
        """
        log.info(f"{Lexer.name()}: Trying to build an integer.")
        if not self.current_char.isdigit():
            log.info(f"{Lexer.name()}: Failed to build an integer. No digit provided.")
            return None
        number = int(self.current_char)
        position = deepcopy(self.current_position)
        self.next_char()
        if number != 0:
            while self.current_char.isdigit() and self._is_number_in_range(number):
                number = number * 10 + int(self.current_char)
                self.next_char()
        log.info(f"{Lexer.name()}: Integer built successfully. Returning 'T_INTEGER' token.")
        return IntegerToken(TokenType.T_INTEGER, position, number)

    def _is_number_in_range(self, number):
        return number * 10 + int(self.current_char) <= self.max_int

    def build_tag(self) -> Token or None:
        """
        Tries to build an image tag token according to:
        ```
        image_size_tag = '@', literal
        ```

        Returns:
            Appropriate token of type T_IMAGE_SIZE_TAG if completed successfully,
            None if the tag cannot be built
        """
        log.info("Trying to build a tag.")
        if not self.current_char == self.tag:
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

    def get_url_ending(self, string: str) -> str or None:
        """
        Gets the remaining part of url after the first dot (dot is required at least once in a url)

        Args:
            string: first part of to-be url

        Returns:
            string: complete url
            None: in case url cannot be built
        """
        log.info(f"{Lexer.name()}: Trying to build a url ending.")
        if self.current_char != ".":
            log.info(f"{Lexer.name()}: Failed to build a url ending. Missing '.'.)")
            return None
        string += self.current_char
        self.next_char()
        while self.is_character() or self.current_char in self.additional_path_signs:  # @TODO add hypothesis tests
            string += self.current_char
            self.next_char()
        log.info(f"{Lexer.name()}: Url ending built successfully.")
        return string

    def build_url(self) -> Token or None:
        """
        Tries to build a url token according to:
        ```
        image_url = '(', { '/' | '.' | literal}, '.', literal, ')'
        ```

        Returns:
            Appropriate token of type T_IMAGE_URL if completed successfully,
            None if the url cannot be built
        """
        log.info(f"{Lexer.name()}: Trying to build a url.")
        if not self.current_char == "(":
            log.info(f"{Lexer.name()}: Failed to build a url. Missing '('.)")
            return None
        position = deepcopy(self.current_position)
        string = self.current_char
        self.next_char()
        while self.is_character() or self.current_char == "/":
            string += self.current_char
            self.next_char()
        if not (string := self.get_url_ending(string)):
            log.info(f"{Lexer.name()}: Failed to build a url. Missing url ending.)")
            return None
        if not self.current_char == ")":
            log.info(f"{Lexer.name()}: Failed to build a url. Missing ')'.)")
            return None
        string += self.current_char
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
                or (token := self.build_white_char())
            ):
                log.info(f"{Lexer.name()}: Token {token.type} returned with content: '{token.string}'.")
                return token
        else:
            log.info(f"{Lexer.name()}: Lexer finished work. Returning 'T_EOF' token.")
            return Token(TokenType.T_EOF, self.current_position)
