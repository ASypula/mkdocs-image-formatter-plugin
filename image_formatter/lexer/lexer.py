from image_formatter.lexer.token import Token, TokenType, IntegerToken, TagToken
from image_formatter.lexer.position import Position
from image_formatter.lexer.token_stream_processor import TokenStreamProcessor
from image_formatter.error_handler.errors import InvalidConfigCharacterError
import io
import sys
from mkdocs.plugins import get_plugin_logger
from copy import deepcopy
from typing import Tuple, List

log = get_plugin_logger(__name__)


class Lexer(TokenStreamProcessor):
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
        special_signs: Tuple[str] = ("-", "_"),
        tag: str = "@",
        newline_characters: Tuple[str] = ("\n", "\r"),
        additional_path_signs: Tuple[str] = ("/", "."),
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
        Lexer.verify_config(special_signs, tag, newline_characters, additional_path_signs)
        self.fp = fp
        self.running = True
        self.current_char = ""
        self.current_position = Position(1, 1)
        self.max_int = max_int
        self.tag = tag
        self.special_signs = special_signs
        self.newline_characters = newline_characters
        self.additional_path_signs = additional_path_signs

    @classmethod
    def name(cls) -> str:
        return cls.__name__

    @classmethod
    def verify_config(
        cls,
        special_signs: Tuple[str],
        tag: str,
        newline_characters: Tuple[str],
        additional_path_signs: Tuple[str],
    ) -> bool:
        """
        Verifies if provided to Lexer configuration is valid. Upon failure on any of the verification steps, the function returns immediately with fail reason.

        Returns:
            True when configuration is valid
        Raises:
            InvalidConfigCharacterError: when invalid character is found
            Exception: when there is different reason of validation fail
        """
        # configurations must be mutually exclusive
        flat_list = [*set(special_signs), tag, *set(newline_characters), *set(additional_path_signs)]
        if len(flat_list) != len(set(flat_list)):
            raise Exception("Characters cannot repeat across configuration options")

        Lexer.verify_special_signs(special_signs)
        Lexer.verify_tag(tag)
        Lexer.verify_newline_characters(newline_characters)
        Lexer.verify_additional_path_signs(additional_path_signs)

    @staticmethod
    def find_invalid_char(valid_chars: List[str], check_chars: Tuple[str]) -> str:
        invalid_char = next(filter(lambda x: x not in valid_chars, check_chars), None)
        return invalid_char

    @classmethod
    def verify_special_signs(cls, signs: Tuple[str]) -> bool:
        """
        Verifies if all characters in the list are valid special signs characters

        Returns:
            True when configuration is valid
        Raises:
            InvalidConfigCharacterError: when invalid character is found
        """
        invalid_chars = [" ", "(", ")"]
        if any([sign in invalid_chars for sign in signs]):
            raise InvalidConfigCharacterError("<space>", [])
        return True

    @classmethod
    def verify_tag(cls, tag: str) -> bool:
        """
        Verifies if tag is valid

        Returns:
            True when tag is valid
        Raises:
            InvalidConfigCharacterError: when invalid character is found
        """
        valid_tags = "@#$%&~>?+=:"
        invalid_char = Lexer.find_invalid_char(valid_tags, (tag))
        if invalid_char:
            raise InvalidConfigCharacterError(invalid_char, valid_tags)
        return True

    @classmethod
    def verify_newline_characters(cls, chars: Tuple[str]) -> bool:
        """
        Verifies if all characters in the list are valid new line characters

        Returns:
            True when configuration is valid
        Raises:
            InvalidConfigCharacterError: when invalid character is found
        """
        valid_newline_chars = ["\n", "\r", "\r\n", "\x0b", "\v", "\f"]
        invalid_char = Lexer.find_invalid_char(valid_newline_chars, chars)
        if invalid_char:
            raise InvalidConfigCharacterError(invalid_char, valid_newline_chars)
        return True

    @classmethod
    def verify_additional_path_signs(cls, signs: Tuple[str]) -> bool:
        """
        Verifies if all characters in the list are valid additional path signs

        Returns:
            True when configuration is valid
        Raises:
            InvalidConfigCharacterError: when invalid character is found
        """
        valid_additional_path_signs = "-_.~:/?#[]@!$&'()*+,;=%"
        invalid_char = Lexer.find_invalid_char(valid_additional_path_signs, signs)
        if invalid_char:
            raise InvalidConfigCharacterError(invalid_char, valid_additional_path_signs)
        return True

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

    def build_tag(self) -> TagToken or None:
        """
        Tries to build an image tag token according to:
        ```
        image_size_tag = tag_character, literal
        tag_character by default is '@'
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
        return TagToken(TokenType.T_IMAGE_SIZE_TAG, position, token.string, self.tag)

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
        while self.is_character() or self.current_char in self.additional_path_signs:
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
