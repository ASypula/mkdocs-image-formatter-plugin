from image_formatter.lexer.token import Token


class TokenStreamProcessor:
    """
    Base class for tokens stream processing.
    """

    def get_token(self) -> Token:
        """
        Returns Token.
        """
        raise NotImplementedError
