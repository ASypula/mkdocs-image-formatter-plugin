from image_formatter.lexer.lexer import Lexer
from image_formatter.lexer.token import Token, TokenType
from image_formatter.lexer.position import Position
from image_formatter.image_properties_tag_replacer.image_properties_tag_replacer import ImagePropertiesTagReplacer
import io
import pytest


def setup_parser(request):
    fp = io.StringIO(request)
    lexer = Lexer(fp)
    lexer.next_char()
    image_tags_properties = {
        "small": {"height": "100px", "width": "100px"},
        "big": {"height": "200px", "width": "200px"},
    }
    parser = ImagePropertiesTagReplacer(lexer, image_tags_properties)
    return parser


def test_given_no_image_links_then_nothing_is_replaced():
    parser = setup_parser("word1, word2 $$ @tag1-tag \n\n @tag2 x (start-of/url.png)")
    result = []
    expected_tokens = [
        Token(TokenType.T_LITERAL, Position(1, 1), "word1"),
        Token(TokenType.T_CHAR, Position(1, 6), ","),
        Token(TokenType.T_WHITE_CHAR, Position(1, 7), " "),
        Token(TokenType.T_LITERAL, Position(1, 8), "word2"),
        Token(TokenType.T_WHITE_CHAR, Position(1, 13), " "),
        Token(TokenType.T_CHAR, Position(1, 14), "$"),
        Token(TokenType.T_CHAR, Position(1, 15), "$"),
        Token(TokenType.T_WHITE_CHAR, Position(1, 16), " "),
        Token(TokenType.T_WHITE_CHAR, Position(1, 17), "tag1-tag"),
        Token(TokenType.T_WHITE_CHAR, Position(1, 26), " "),
        Token(TokenType.T_WHITE_CHAR, Position(1, 27), "\n"),
        Token(TokenType.T_WHITE_CHAR, Position(2, 1), "\n"),
        Token(TokenType.T_WHITE_CHAR, Position(3, 1), " "),
        Token(TokenType.T_WHITE_CHAR, Position(3, 2), "tag2"),
        Token(TokenType.T_WHITE_CHAR, Position(3, 7), " "),
        Token(TokenType.T_CHAR, Position(3, 8), "x"),
        Token(TokenType.T_WHITE_CHAR, Position(3, 9), " "),
        Token(TokenType.T_IMAGE_URL, Position(3, 10), "(start-of/url.png)"),
    ]

    for link in parser.replace_image_properties_tags():
        result.append(link)
    assert result == expected_tokens


def test_given_no_input_then_nothing_is_returned():
    parser = setup_parser("")
    result = []
    for link in parser.replace_image_properties_tags():
        result.append(link)
    assert result == []


@pytest.mark.parametrize(
    "text, expected_tokens",
    [
        (
            "   @small(some/url.png)",
            [
                Token(TokenType.T_WHITE_CHAR, Position(1, 1), " "),
                Token(TokenType.T_WHITE_CHAR, Position(1, 2), " "),
                Token(TokenType.T_WHITE_CHAR, Position(1, 3), " "),
                Token(
                    TokenType.T_IMAGE_URL_WITH_PROPERTIES,
                    Position(1, 10),
                    '(some/url.png){: style="height:100px;width:100px"}',
                ),
            ],
        ),
        (
            "x@small(some/url.png)",
            [
                Token(TokenType.T_CHAR, Position(1, 1), "x"),
                Token(
                    TokenType.T_IMAGE_URL_WITH_PROPERTIES,
                    Position(1, 8),
                    '(some/url.png){: style="height:100px;width:100px"}',
                ),
            ],
        ),
    ],
)
def test_given_sequence_of_tokens_with_one_valid_image_tag_then_one_image_tag_is_replaced(text, expected_tokens):
    parser = setup_parser(text)
    result = []

    for link in parser.replace_image_properties_tags():
        result.append(link)
    assert result == expected_tokens


@pytest.mark.parametrize(
    "text, expected_tokens",
    [
        (
            "   @small(some/url.png) & word @big(next/longer.url.jpg)  word2",
            [
                Token(TokenType.T_WHITE_CHAR, Position(1, 1), " "),
                Token(TokenType.T_WHITE_CHAR, Position(1, 2), " "),
                Token(TokenType.T_WHITE_CHAR, Position(1, 3), " "),
                Token(
                    TokenType.T_IMAGE_URL_WITH_PROPERTIES,
                    Position(1, 10),
                    '(some/url.png){: style="height:100px;width:100px"}',
                ),
                Token(TokenType.T_WHITE_CHAR, Position(1, 24), " "),
                Token(TokenType.T_CHAR, Position(1, 25), "&"),
                Token(TokenType.T_WHITE_CHAR, Position(1, 26), " "),
                Token(TokenType.T_LITERAL, Position(1, 27), "word"),
                Token(TokenType.T_WHITE_CHAR, Position(1, 31), " "),
                Token(
                    TokenType.T_IMAGE_URL_WITH_PROPERTIES,
                    Position(1, 36),
                    '(next/longer.url.jpg){: style="height:200px;width:200px"}',
                ),
                Token(TokenType.T_WHITE_CHAR, Position(1, 57), " "),
                Token(TokenType.T_WHITE_CHAR, Position(1, 58), " "),
                Token(TokenType.T_LITERAL, Position(1, 59), "word2"),
            ],
        ),
        (
            "   @small(some/url.png) & word @big *(next/longer.url.jpg)  word2",
            [
                Token(TokenType.T_WHITE_CHAR, Position(1, 1), " "),
                Token(TokenType.T_WHITE_CHAR, Position(1, 2), " "),
                Token(TokenType.T_WHITE_CHAR, Position(1, 3), " "),
                Token(
                    TokenType.T_IMAGE_URL_WITH_PROPERTIES,
                    Position(1, 10),
                    '(some/url.png){: style="height:100px;width:100px"}',
                ),
                Token(TokenType.T_WHITE_CHAR, Position(1, 24), " "),
                Token(TokenType.T_CHAR, Position(1, 25), "&"),
                Token(TokenType.T_WHITE_CHAR, Position(1, 26), " "),
                Token(TokenType.T_LITERAL, Position(1, 27), "word"),
                Token(TokenType.T_WHITE_CHAR, Position(1, 31), " "),
                Token(TokenType.T_IMAGE_SIZE_TAG, Position(1, 32), "big"),
                Token(TokenType.T_WHITE_CHAR, Position(1, 36), " "),
                Token(TokenType.T_CHAR, Position(1, 37), "*"),
                Token(TokenType.T_IMAGE_URL, Position(1, 38), "(next/longer.url.jpg)"),
                Token(TokenType.T_WHITE_CHAR, Position(1, 59), " "),
                Token(TokenType.T_WHITE_CHAR, Position(1, 60), " "),
                Token(TokenType.T_LITERAL, Position(1, 61), "word2"),
            ],
        ),
    ],
)
def test_given_image_links_mixed_with_other_tokens_then_image_links_returned(text, expected_tokens):
    parser = setup_parser(text)
    result = []

    for link in parser.replace_image_properties_tags():
        result.append(link)
    assert result == expected_tokens
