from image_formatter.lexer.lexer import Lexer
from image_formatter.lexer.token import TokenType
from tests.test_helpers import get_all_tokens
import io
import pytest

LITERALS_1 = ["one", "some-hyphen", "one two three", "with_underscore"]
TAGS_1 = ["@one", "@some-hyphen&@hello", "@one **", "``  @with_underscore"]
URLS_1 = [
    "(one/two/three.com)",
    "    (hi/some-hyphen.png)",
    "\n (with.many.dots/one.jpg)",
    "**  (url1.png.url2/url3.jpg)",
]
TRICKY_1 = ["1hello", "@tag1(url1.png)@one-more-tag&and_word"]
EXP_T_TYPES_TRICKY1 = [
    [TokenType.T_LITERAL],
    [
        TokenType.T_IMAGE_SIZE_TAG,
        TokenType.T_IMAGE_URL,
        TokenType.T_IMAGE_SIZE_TAG,
        TokenType.T_LITERAL,
    ],
]
EXP_T_STRINGS_TRICKY1 = [["hello"], ["tag1", "url1.png", "one-more-tag", "and_word"]]

@pytest.mark.parametrize("text", LITERALS_1)
def test_T_LITERAL_only(text):
    fp = io.StringIO(text)
    lexer = Lexer(fp)
    tokens = get_all_tokens(lexer)
    assert all(token.type == TokenType.T_LITERAL for token in tokens)


@pytest.mark.parametrize("text", TAGS_1)
def test_T_IMAGE_SIZE_TAG_only(text):
    fp = io.StringIO(text)
    lexer = Lexer(fp)
    tokens = get_all_tokens(lexer)
    assert all(token.type == TokenType.T_IMAGE_SIZE_TAG for token in tokens)


@pytest.mark.parametrize("text", URLS_1)
def test_T_IMAGE_URL_only(text):
    fp = io.StringIO(text)
    lexer = Lexer(fp)
    tokens = get_all_tokens(lexer)
    assert all(token.type == TokenType.T_IMAGE_URL for token in tokens)


def test_mix1():
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


def combine(text, expected_types, expected_strings):
    for word, type, string in zip(text, expected_types, expected_strings):
        yield word, type, string


@pytest.mark.parametrize(
    "text, exp_t_types, exp_t_strings",
    combine(TRICKY_1, EXP_T_TYPES_TRICKY1, EXP_T_STRINGS_TRICKY1),
)
def test_tricky1(text, exp_t_types, exp_t_strings):
    fp = io.StringIO(text)
    lexer = Lexer(fp)
    tokens = get_all_tokens(lexer)
    assert [token.type for token in tokens] == exp_t_types
    assert [token.string for token in tokens] == exp_t_strings
