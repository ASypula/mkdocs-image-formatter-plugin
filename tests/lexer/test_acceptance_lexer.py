from image_formatter.lexer.lexer import Lexer
from image_formatter.lexer.token import TokenType
from image_formatter.lexer.position import Position
from tests.test_helpers import get_all_tokens


def test_file1_literals():
    filename = "./resources/test_files/test1.txt"
    expected_types = [TokenType.T_LITERAL, TokenType.T_WHITE_CHAR, TokenType.T_LITERAL, TokenType.T_WHITE_CHAR]
    expected_strings = ["hello", "\n", "second", "\n"]
    expected_positions = [Position(1, 1), Position(1, 6), Position(2, 1), Position(2, 7)]
    with open(filename) as fp:
        lexer = Lexer(fp)  # noqa
        tokens = get_all_tokens(lexer)
    assert [token.type for token in tokens] == expected_types
    assert [token.string for token in tokens] == expected_strings
    assert [token.position for token in tokens] == expected_positions


def test_file2_mix():
    filename = "./resources/test_files/test2.txt"
    expected_types = [
        TokenType.T_INTEGER,
        TokenType.T_LITERAL,
        TokenType.T_WHITE_CHAR,
        TokenType.T_IMAGE_SIZE_TAG,
        TokenType.T_WHITE_CHAR,
        TokenType.T_IMAGE_URL,
        TokenType.T_CHAR,
        TokenType.T_LITERAL,
        TokenType.T_WHITE_CHAR,
    ]
    expected_strings = ["1", "hello1", " ", "small2", "\n", "(some/url.com)", "+", "word", "\n"]
    expected_positions = [
        Position(1, 1),
        Position(1, 2),
        Position(1, 8),
        Position(1, 9),
        Position(1, 16),
        Position(2, 1),
        Position(2, 15),
        Position(2, 16),
        Position(2, 20),
    ]
    with open(filename) as fp:
        lexer = Lexer(fp)  # noqa
        tokens = get_all_tokens(lexer)
    assert [token.type for token in tokens] == expected_types
    assert [token.string for token in tokens] == expected_strings
    assert [token.position for token in tokens] == expected_positions


def test_file3_classic_macos_newline():
    filename = "./resources/test_files/test3_classic_macos_newline.txt"
    expected_types = [
        TokenType.T_INTEGER,
        TokenType.T_LITERAL,
        TokenType.T_WHITE_CHAR,
        TokenType.T_IMAGE_URL,
        TokenType.T_WHITE_CHAR,
    ]
    expected_strings = ["1", "hello1", "\r", "(some/url.com)", "\r"]
    expected_positions = [Position(1, 1), Position(1, 2), Position(1, 8), Position(2, 1), Position(2, 15)]
    with open(filename, newline="\r") as fp:
        lexer = Lexer(fp)  # noqa
        tokens = get_all_tokens(lexer)
    assert [token.type for token in tokens] == expected_types
    assert [token.string for token in tokens] == expected_strings
    assert [token.position for token in tokens] == expected_positions


def test_file4_unix_and_macos_newline():
    filename = "./resources/test_files/test4_unix_and_macos_newline.txt"
    expected_types = [
        TokenType.T_INTEGER,
        TokenType.T_LITERAL,
        TokenType.T_WHITE_CHAR,
        TokenType.T_IMAGE_URL,
        TokenType.T_WHITE_CHAR,
    ]
    expected_strings = ["1", "hello1", "\n", "(some/url.com)", "\n"]
    expected_positions = [Position(1, 1), Position(1, 2), Position(1, 8), Position(2, 1), Position(2, 15)]
    with open(filename) as fp:
        lexer = Lexer(fp)  # noqa
        tokens = get_all_tokens(lexer)
    assert [token.type for token in tokens] == expected_types
    assert [token.string for token in tokens] == expected_strings
    assert [token.position for token in tokens] == expected_positions
