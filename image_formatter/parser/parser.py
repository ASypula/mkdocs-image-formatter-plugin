from image_formatter.lexer.lexer import Lexer
from image_formatter.lexer.token import TokenType
from image_formatter.error_handler.error_handler import ErrorHandler
from image_formatter.error_handler.errors import UnexpectedTagException


class Parser:
    """
    Class parser responsible for parsing the code.
    Focuses only on the plugin's purpose - images with added size tags
    """

    def __init__(self, lex: Lexer, error_handler: ErrorHandler = ErrorHandler()):
        """
        Args:
            lex: lexer used for obtaining tokens
        """
        self.lexer = lex
        self.curr_token = lex.get_token()
        self.error_handler = error_handler

    def consume_if_token(self, token_type: TokenType) -> str or bool:
        """
        Gets next token from lexer if the token types are the same.

        Args:
            token_type: type of the token to be compared

        Returns:
            str: string from the token if the types are matching
            False: if the token types are different
        """
        while not self.curr_token:
            self.curr_token = self.lexer.get_token()
        if self.curr_token.type != token_type:
            return False
        string = self.curr_token.string
        self.curr_token = self.lexer.get_token()
        return string

    def parse_image_link_url(self, tag: str) -> (str, str) or bool:
        """
        Verify if image url can be created according to the:
        image_link = image_size_tag, image_url

        Args:
            tag: already found tag

        Returns:
            tuple(str, str): if successful, tag and url
            False: if image link cannot be created
        """
        if url := self.consume_if_token(TokenType.T_IMAGE_URL):
            return (tag, url)
        self.error_handler.handle(UnexpectedTagException(TokenType.T_IMAGE_URL, self.curr_token.type))
        return False

    def parse_image_link_tag(self) -> (str, str) or bool:
        """
        Tries to parse the first part of image link - the tag.
        image_link = image_size_tag, image_url

        Returns:
            tuple(str, str): if successful from the parse_image_link_url
            False: if image link tag cannot be created
        """
        if tag := self.consume_if_token(TokenType.T_IMAGE_SIZE_TAG):
            return self.parse_image_link_url(tag)
        return False

    def parse(self):
        """
        TODO
        """
        while self.lexer.running:
            if image_link_tag := self.parse_image_link_tag():
                yield image_link_tag
            else:
                self.curr_token = self.lexer.get_token()
