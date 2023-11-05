from image_formatter.lexer.lexer import Lexer
from image_formatter.lexer.token import Token
from image_formatter.parser.parser import Parser


def get_all_tokens(lexer: Lexer) -> list[Token]:
    """
    Collects all tokens available from the lexer's stream.

    Args:
        lexer: Lexer to use

    Returns:
        list of tokens
    """
    tokens = []
    lexer.next_char()
    while lexer.running:
        if token := lexer.get_token():
            tokens.append(token)
    return tokens


def get_all_parser_results(parser: Parser, lexer_iterations: int) -> list[(str, str) or None]:
    """
    Collects all results returned by the function parse_image_link_tag.
    The parse function cannot be used in unit tests for parser as it uses the lexer.running attribute.

    Args:
        parser: Parser to use
        lexer_iterations: number of times to loop through the parse_image_link_tag

    Returns:
        list of tuples(str, str) with None
    """
    image_links = []
    for _ in range(lexer_iterations):
        image_links.append(parser.parse_image_link_tag())
    return image_links
