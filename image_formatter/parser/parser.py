from image_formatter.lexer.lexer import Lexer
from image_formatter.lexer.token import Token, TokenType

class Parser:
    """
    Class parser responsible for parsing the code.
    Focuses only on the plugin's purpose - images with added size tags
    """

    def __init__(self, lex: Lexer):
        """
        Args:
            lex: lexer used for obtaining tokens
        """
        self.lexer = lex
        self.curr_token = lex.get_token()

    def consume_if_token(self, token_type: TokenType) -> bool:
        """
        Get next token from lexer If the token types are the same.

        Args:
            token_type: type of the token to be compared

        Returns:
            True: If the types are matching
            False: If the token types are different
        """
        if self.curr_token and self.curr_token.type != token_type:
            return False
        self.curr_token = self.lexer.get_token()
        return True

    def parse_image_link_url(self):
        #TODO: return None or 0?
        """
        Verify If image url can be created according to the: 
        image_link = image_size_tag, image_url
        """
        if self.consume_if_token(TokenType.T_IMAGE_URL):
            return "Image link found! :)"
        return None

    def parse_image_link_tag(self):
        """
        Tries to parse the first part of image link - the tag.
        image_link = image_size_tag, image_url
        """
        if self.consume_if_token(TokenType.T_IMAGE_SIZE_TAG):
            return self.parse_image_link_url()
        return None

    def parse(self):
        """
        TODO
        """
        while self.lexer.running:
            x = self.parse_image_link_tag()
            print(x)

