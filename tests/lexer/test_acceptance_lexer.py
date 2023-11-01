from image_formatter.lexer.lexer import Lexer
from image_formatter.lexer.token import TokenType
from tests.test_helpers import get_all_tokens


def test_file1_literals():
    filename = "tests/lexer/test_files/test1.txt"
    expected_types = [TokenType.T_LITERAL, TokenType.T_LITERAL]
    expected_strings = ["hello", "second"]
    tokens = []
    with open(filename) as fp:
        lexer = Lexer(fp)
        tokens = get_all_tokens(lexer)
    assert [token.type for token in tokens] == expected_types
    assert [token.string for token in tokens] == expected_strings


def test_file2_mix():
    filename = "tests/lexer/test_files/test2.txt"
    expected_types = [
        TokenType.T_INTEGER,
        TokenType.T_LITERAL,
        TokenType.T_IMAGE_SIZE_TAG,
        TokenType.T_IMAGE_URL,
        TokenType.T_CHAR,
        TokenType.T_LITERAL,
    ]
    expected_strings = ["1", "hello1", "small2", "some/url.com", "+", "word"]
    tokens = []
    with open(filename) as fp:
        lexer = Lexer(fp)
        tokens = get_all_tokens(lexer)
    assert [token.type for token in tokens] == expected_types
    assert [token.string for token in tokens] == expected_strings
