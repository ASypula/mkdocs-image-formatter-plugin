from image_formatter.lexer.lexer import Lexer
from image_formatter.lexer.token import TokenType
from image_formatter.lexer.position import Position
from tests.test_helpers import get_all_tokens
import sys
import io
import pytest


@pytest.mark.parametrize(
    "text, positions",
    [
        ("one ", [Position(1, 1)]),
        ("some-hyphen ", [Position(1, 1)]),
        ("one two three ", [Position(1, 1), Position(1, 5), Position(1, 9)]),
        ("with_underscore", [Position(1, 1)]),
    ],
)
def test_given_only_plain_text_then_only_literal_tokens_are_returned(text, positions):
    fp = io.StringIO(text)
    lexer = Lexer(fp)
    tokens = get_all_tokens(lexer)
    assert all(token.type == TokenType.T_LITERAL for token in tokens)
    for token, position in zip(tokens, positions):
        assert token.position == position


@pytest.mark.parametrize(
    "text, positions",
    [
        ("@one", [Position(1, 1)]),
        ("@some-hyphen @hello", [Position(1, 1), Position(1, 14)]),
        ("\n@one \n", [Position(2, 1)]),
        ("  @with_underscore", [Position(1, 3)]),
    ],
)
def test_given_only_tags_then_only_tag_tokens_are_returned(text, positions):
    fp = io.StringIO(text)
    lexer = Lexer(fp)
    tokens = get_all_tokens(lexer)
    assert all(token.type == TokenType.T_IMAGE_SIZE_TAG for token in tokens)
    for token, position in zip(tokens, positions):
        assert token.position == position


@pytest.mark.parametrize(
    "text, positions",
    [
        ("(one/two/three.com)", [Position(1, 1)]),
        ("    (hi/some-hyphen.png)", [Position(1, 5)]),
        ("\n (with.many.dots/one.jpg)", [Position(2, 2)]),
        ("  \t(url1.png.url2/url3.jpg)", [Position(1, 4)]),
    ],
)
def test_given_only_urls_then_only_url_tokens_are_returned(text, positions):
    fp = io.StringIO(text)
    lexer = Lexer(fp)
    tokens = get_all_tokens(lexer)
    assert all(token.type == TokenType.T_IMAGE_URL for token in tokens)
    for token, position in zip(tokens, positions):
        assert token.position == position


def test_given_complex_text_with_special_chars_then_sequence_of_tokens_is_returned():
    text = "word1, word2 $$ @tag1-tag \n\n @tag2(start-of/url.png)"
    expected_types = [
        TokenType.T_LITERAL,
        TokenType.T_CHAR,
        TokenType.T_LITERAL,
        TokenType.T_CHAR,
        TokenType.T_CHAR,
        TokenType.T_IMAGE_SIZE_TAG,
        TokenType.T_IMAGE_SIZE_TAG,
        TokenType.T_IMAGE_URL,
    ]
    expected_strings = [
        "word1",
        ",",
        "word2",
        "$",
        "$",
        "tag1-tag",
        "tag2",
        "start-of/url.png",
    ]
    expected_positions = [
        Position(1, 1),
        Position(1, 6),
        Position(1, 8),
        Position(1, 14),
        Position(1, 15),
        Position(1, 17),
        Position(3, 2),
        Position(3, 7),
    ]
    fp = io.StringIO(text)
    lexer = Lexer(fp)
    tokens = get_all_tokens(lexer)
    assert len(tokens) == len(expected_types)
    assert [token.type for token in tokens] == expected_types
    assert [token.string for token in tokens] == expected_strings
    assert [token.position for token in tokens] == expected_positions


def test_when_literal_starts_with_digit_then_literal_token_without_starting_digit_returned():
    text = "1hello"
    fp = io.StringIO(text)
    lexer = Lexer(fp)
    tokens = get_all_tokens(lexer)
    assert [token.type for token in tokens] == [
        TokenType.T_INTEGER,
        TokenType.T_LITERAL,
    ]
    assert [token.string for token in tokens] == ["1", "hello"]
    assert [token.position for token in tokens] == [Position(1, 1), Position(1, 2)]


def test_given_text_when_tags_not_separated_by_spaces_then_tokens_returned():
    text = "@tag1(url1.png)@one-more-tag&and_word"
    fp = io.StringIO(text)
    lexer = Lexer(fp)
    tokens = get_all_tokens(lexer)
    assert [token.type for token in tokens] == [
        TokenType.T_IMAGE_SIZE_TAG,
        TokenType.T_IMAGE_URL,
        TokenType.T_IMAGE_SIZE_TAG,
        TokenType.T_CHAR,
        TokenType.T_LITERAL,
    ]
    assert [token.string for token in tokens] == [
        "tag1",
        "url1.png",
        "one-more-tag",
        "&",
        "and_word",
    ]
    assert [token.position for token in tokens] == [
        Position(1, 1),
        Position(1, 6),
        Position(1, 16),
        Position(1, 29),
        Position(1, 30),
    ]


@pytest.mark.parametrize(
    "text, expected_types, expected_values, expected_positions",
    [
        ("1", [TokenType.T_INTEGER], [1], [Position(1, 1)]),
        ("41", [TokenType.T_INTEGER], [41], [Position(1, 1)]),
        ("5014", [TokenType.T_INTEGER], [5014], [Position(1, 1)]),
    ],
)
def test_given_integer_then_integer_token_is_returned(text, expected_types, expected_values, expected_positions):
    fp = io.StringIO(text)
    lexer = Lexer(fp)
    tokens = get_all_tokens(lexer)
    assert [token.type for token in tokens] == expected_types
    assert [token.integer for token in tokens] == expected_values  # noqa
    assert [token.position for token in tokens] == expected_positions


@pytest.mark.parametrize(
    "text, expected_types, expected_values, expected_positions",
    [
        ("01", [TokenType.T_INTEGER, TokenType.T_INTEGER], [0, 1], [Position(1, 1), Position(1, 2)]),
        ("041", [TokenType.T_INTEGER, TokenType.T_INTEGER], [0, 41], [Position(1, 1), Position(1, 2)]),
        ("05014", [TokenType.T_INTEGER, TokenType.T_INTEGER], [0, 5014], [Position(1, 1), Position(1, 2)]),
    ],
)
def test_given_digits_when_zero_is_the_first_one_then_two_integer_tokens_are_returned(
    text, expected_types, expected_values, expected_positions
):
    fp = io.StringIO(text)
    lexer = Lexer(fp)
    tokens = get_all_tokens(lexer)
    assert [token.type for token in tokens] == expected_types
    assert [token.integer for token in tokens] == expected_values  # noqa
    assert [token.position for token in tokens] == expected_positions


@pytest.mark.parametrize(
    "text, expected_types, expected_values, expected_positions",
    [
        ("2147483647", [TokenType.T_INTEGER], [2147483647], [Position(1, 1)]),
        ("21474836470000", [TokenType.T_INTEGER], [21474836470000], [Position(1, 1)]),
        (f"{sys.maxsize}", [TokenType.T_INTEGER], [sys.maxsize], [Position(1, 1)]),
    ],
)
def test_given_very_large_integer_then_integer_token_is_returned(
    text, expected_types, expected_values, expected_positions
):
    fp = io.StringIO(text)
    lexer = Lexer(fp)
    tokens = get_all_tokens(lexer)
    assert [token.type for token in tokens] == expected_types
    assert [token.integer for token in tokens] == expected_values  # noqa
    assert [token.position for token in tokens] == expected_positions


@pytest.mark.parametrize(
    "text, expected_types, expected_values, expected_positions",
    [
        (
            "2147483647",
            [
                TokenType.T_INTEGER,
                TokenType.T_INTEGER,
                TokenType.T_INTEGER,
                TokenType.T_INTEGER,
            ],
            [214, 748, 364, 7],
            [Position(1, 1), Position(1, 4), Position(1, 7), Position(1, 10)],
        ),
        (
            "21474836470000",
            [
                TokenType.T_INTEGER,
                TokenType.T_INTEGER,
                TokenType.T_INTEGER,
                TokenType.T_INTEGER,
                TokenType.T_INTEGER,
                TokenType.T_INTEGER,
            ],
            [214, 748, 364, 700, 0, 0],
            [Position(1, 1), Position(1, 4), Position(1, 7), Position(1, 10), Position(1, 13), Position(1, 14)],
        ),
    ],
)
def test_given_max_int_set_to_1000_when_int_exceeds_max_int_then_multiple_integer_tokens_are_returned(
    text, expected_types, expected_values, expected_positions
):
    fp = io.StringIO(text)
    lexer = Lexer(fp, max_int=1000)
    tokens = get_all_tokens(lexer)
    assert [token.type for token in tokens] == expected_types
    assert [token.integer for token in tokens] == expected_values  # noqa
    assert [token.position for token in tokens] == expected_positions


@pytest.mark.parametrize(
    "text, positions",
    [
        ("\none ", [Position(2, 1)]),
        ("\rtwo", [Position(2, 1)]),
        ("\n\rthree", [Position(3, 1)]),
    ],
)
def test_given_different_newline_symbols_then_position_is_updated_accordingly(text, positions):
    fp = io.StringIO(text)
    lexer = Lexer(fp)
    tokens = get_all_tokens(lexer)
    assert all(token.type == TokenType.T_LITERAL for token in tokens)
    for token, position in zip(tokens, positions):
        assert token.position == position
