import copy

from image_formatter.lexer.lexer import Lexer
from image_formatter.lexer.token import TokenType, Token
from image_formatter.lexer.token_stream_processor import TokenStreamProcessor
from image_formatter.error_handler.error_handler import ErrorHandler
from image_formatter.error_handler.errors import UnexpectedTagException
from mkdocs.plugins import get_plugin_logger

log = get_plugin_logger(__name__)


class ImagePropertiesTagReplacer(TokenStreamProcessor):
    """
    Class ImagePropertiesTagReplacer responsible for replacing image size tags with properties after the image URL.
    Focuses only on the plugin's purpose - images with added size tags
    """

    def __init__(self, lex: Lexer, image_tags_properties: dict, error_handler: ErrorHandler = ErrorHandler()):
        """
        Args:
            lex: lexer used for obtaining tokens
            image_tags_properties: properties to be added after tagged urls
            error_handler: used to register errors, takes care of error handling
        """
        self.lexer = lex
        self.curr_token = lex.get_token()
        self.image_tags_properties = image_tags_properties
        self.error_handler = error_handler

    @classmethod
    def name(cls) -> str:
        return cls.__name__

    def next_token(self):
        self.curr_token = self.lexer.get_token()

    def parse_image_link_url(self, tag_token: Token) -> Token:
        """
        Verify if image url can be created according to the:
        ```
        image_link = image_size_tag, image_url
        ```

        Args:
            tag_token: already found tag

        Returns:
            Token: of TokenType.T_IMAGE_URL_WITH_PROPERTIES if successful, otherwise of TokenType.T_IMAGE_SIZE_TAG
        """
        log.info(f"{ImagePropertiesTagReplacer.name()}: Trying to parse image link url.")
        if self.curr_token.type == TokenType.T_IMAGE_URL:
            log.info(f"{ImagePropertiesTagReplacer.name()}: Url tag found: {self.curr_token}")
            url_token = copy.deepcopy(self.curr_token)
            formatted_url = self.add_tag_properties_to_url(tag_token)
            self.next_token()
            return Token(TokenType.T_IMAGE_URL_WITH_PROPERTIES, url_token.position, formatted_url)
        else:
            log.error(f"{ImagePropertiesTagReplacer.name()}: Failed to parse image link url.")
            self.error_handler.handle(UnexpectedTagException(TokenType.T_IMAGE_URL, self.curr_token.type))
            return tag_token

    def add_tag_properties_to_url(self, tag_token: Token) -> str:
        """
        Formats properties for given tag_token to string in a CSS format.

        Args:
            tag_token: token used to mark a url

        Returns:
            str: image tag properties formatted to CSS
        """
        if tag_token.string not in self.image_tags_properties:
            log.info(f"{ImagePropertiesTagReplacer.name()}: {tag_token.string} is an unknown tag, removing formatting")
            return self.curr_token.string
        properties = '{: style="'
        pairs = ";".join([f"{key}:{value}" for key, value in self.image_tags_properties[tag_token.string].items()])
        properties = properties + pairs + '"}'
        formatted_url = self.curr_token.string + properties
        return formatted_url

    def parse_image_link_tag(self) -> Token or bool:
        """
        Tries to parse the first part of image link - the tag.
        image_link = image_size_tag, image_url

        Returns:
            Token: of TokenType.T_IMAGE_URL_WITH_PROPERTIES if successful
            False: if image link tag cannot be created
        """
        log.info(f"{ImagePropertiesTagReplacer.name()}: Trying to parse image link tag.")
        if self.curr_token.type == TokenType.T_IMAGE_SIZE_TAG:
            log.info(f"{ImagePropertiesTagReplacer.name()}: Image size tag found: {self.curr_token}")
            tag_token = copy.deepcopy(self.curr_token)
            self.next_token()
            return self.parse_image_link_url(tag_token)
        log.info(f"{ImagePropertiesTagReplacer.name()}: Failed to parse image link tag.")
        return False

    def get_token(self):
        """
        Replaces image size tags with properties after the url
        """
        while self.curr_token.type != TokenType.T_EOF:
            if image_link_token := self.parse_image_link_tag():
                log.info(
                    f"{ImagePropertiesTagReplacer.name()}: Returning image link token with properties: '{image_link_token.string}'."
                )
                yield image_link_token
            else:
                yield self.curr_token
                self.next_token()
