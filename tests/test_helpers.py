from image_formatter.lexer.lexer import Lexer
from image_formatter.lexer.token import Token

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
        else:
            lexer.next_char()
    return tokens
