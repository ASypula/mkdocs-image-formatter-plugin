import pytest
import io
from image_formatter.lexer.lexer import Lexer
from image_formatter.parser.parser import Parser
from image_formatter.lexer.token import TokenType
from tests.lexer.test_unit_lexer import get_all_tokens

# TODO: better test library with get_all_tokens maybe in separate file?
# TODO: more tests

IMAGE_LINKS_1 = ["@image1 (http://image1-image1)", "with sppaces @  here(hej-hello.png)"]

@pytest.mark.parametrize("text", IMAGE_LINKS_1)
def test_sth(text):
    fp = io.StringIO(text)
    lexer = Lexer(fp)
    tokens = get_all_tokens(lexer)
    parser = Parser(lexer)
    parser.parse()
    # assert all(token.type == TokenType.T_ for token in tokens)
