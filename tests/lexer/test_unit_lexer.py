from image_formatter.lexer.lexer import Lexer
from image_formatter.lexer.token import TokenType
from tests.test_helpers import get_all_tokens
import io
import pytest


@pytest.mark.parametrize("text", ["one", "some-hyphen", "one two three", "with_underscore"])
def test_given_only_plain_text_then_only_literal_tokens_are_returned(text):
    fp = io.StringIO(text)
    lexer = Lexer(fp)
    tokens = get_all_tokens(lexer)
    assert all(token.type == TokenType.T_LITERAL for token in tokens)


@pytest.mark.parametrize("text", ["@one", "@some-hyphen&@hello", "@one **", "``  @with_underscore"])
def test_given_only_tags_then_only_tag_tokens_are_returned(text):
    fp = io.StringIO(text)
    lexer = Lexer(fp)
    tokens = get_all_tokens(lexer)
    assert all(token.type == TokenType.T_IMAGE_SIZE_TAG for token in tokens)


@pytest.mark.parametrize(
    "text",
    [
        "(one/two/three.com)",
        "    (hi/some-hyphen.png)",
        "\n (with.many.dots/one.jpg)",
        "**  (url1.png.url2/url3.jpg)",
    ],
)
def test_given_only_urls_then_only_url_tokens_are_returned(text):
    fp = io.StringIO(text)
    lexer = Lexer(fp)
    tokens = get_all_tokens(lexer)
    assert all(token.type == TokenType.T_IMAGE_URL for token in tokens)


def test_given_complex_text_with_special_chars_then_sequence_of_tokens_is_returned():
    text = "word1, word2#$ $#@tag1-tag \n\n @tag2(start-of/url.png)"
    expected_types = [
        TokenType.T_LITERAL,
        TokenType.T_LITERAL,
        TokenType.T_IMAGE_SIZE_TAG,
        TokenType.T_IMAGE_SIZE_TAG,
        TokenType.T_IMAGE_URL,
    ]
    expected_strings = ["word1", "word2", "tag1-tag", "tag2", "start-of/url.png"]
    fp = io.StringIO(text)
    lexer = Lexer(fp)
    tokens = get_all_tokens(lexer)
    assert len(tokens) == len(expected_types)
    assert [token.type for token in tokens] == expected_types
    assert [token.string for token in tokens] == expected_strings


def test_when_literal_starts_with_digit_then_literal_token_without_starting_digit_returned():
    text = "1hello"
    fp = io.StringIO(text)
    lexer = Lexer(fp)
    tokens = get_all_tokens(lexer)
    assert [token.type for token in tokens] == [TokenType.T_LITERAL]
    assert [token.string for token in tokens] == ["hello"]


def test_given_text_when_tags_not_separated_by_spaces_then_tokens_returned():
    text = "@tag1(url1.png)@one-more-tag&and_word"
    fp = io.StringIO(text)
    lexer = Lexer(fp)
    tokens = get_all_tokens(lexer)
    assert [token.type for token in tokens] == [
        TokenType.T_IMAGE_SIZE_TAG,
        TokenType.T_IMAGE_URL,
        TokenType.T_IMAGE_SIZE_TAG,
        TokenType.T_LITERAL,
    ]
    assert [token.string for token in tokens] == ["tag1", "url1.png", "one-more-tag", "and_word"]
