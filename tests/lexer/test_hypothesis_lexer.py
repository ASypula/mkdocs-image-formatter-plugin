from image_formatter.lexer.lexer import Lexer
from image_formatter.lexer.token import TokenType
from image_formatter.lexer.position import Position
from tests.test_helpers import get_all_tokens
import io
from hypothesis import strategies as st
from hypothesis import given

"""
Lexer has some configurations that depend on user input (tag, special_signs, newline_characters and
additional_path_signs). Most of them have strict list of available symbols. Special_signs doesn't
have that. The following tests are to check if such freedom doesn't break lexer's logic.
They are similar to unit tests in test_unit_lexer.py, but we decided to keep both, because one
might want to execute unit tests without hypothesis tests as they are a bit more time consuming.
"""


def special_sign():
    chars_to_exclude = ["\n", "\r", "@", "/", ".", " ", "(", ")", "&"]
    return st.text(min_size=1, max_size=1).filter(lambda s: all(char not in s for char in chars_to_exclude))


def special_sign_tuples():
    return st.tuples(special_sign(), special_sign(), special_sign())


@given(special_sign_tuples())
def test_given_text_when_tags_not_separated_by_spaces_then_tokens_returned(
    special_signs,
):
    text = f"@tag1(url1.png)@one{special_signs[0]}more{special_signs[1]}tag&and{special_signs[2]}word"
    fp = io.StringIO(text)
    lexer = Lexer(fp, special_signs=special_signs)
    tokens = get_all_tokens(lexer)
    assert [token.type for token in tokens] == [
        TokenType.T_IMAGE_SIZE_TAG,
        TokenType.T_IMAGE_URL,
        TokenType.T_IMAGE_SIZE_TAG,
        TokenType.T_CHAR,
        TokenType.T_LITERAL,
    ]
    assert [token.position for token in tokens] == [
        Position(1, 1),
        Position(1, 6),
        Position(1, 16),
        Position(1, 29),
        Position(1, 30),
    ]


@given(special_sign_tuples())
def test_given_complex_text_with_special_chars_then_sequence_of_tokens_is_returned(
    special_signs,
):
    text = f"word1& word2 && @tag1{special_signs[0]}tag \n\n @tag2(start{special_signs[1]}of/url.png)"
    expected_types = [
        TokenType.T_LITERAL,
        TokenType.T_CHAR,
        TokenType.T_WHITE_CHAR,
        TokenType.T_LITERAL,
        TokenType.T_WHITE_CHAR,
        TokenType.T_CHAR,
        TokenType.T_CHAR,
        TokenType.T_WHITE_CHAR,
        TokenType.T_IMAGE_SIZE_TAG,
        TokenType.T_WHITE_CHAR,
        TokenType.T_WHITE_CHAR,
        TokenType.T_WHITE_CHAR,
        TokenType.T_WHITE_CHAR,
        TokenType.T_IMAGE_SIZE_TAG,
        TokenType.T_IMAGE_URL,
    ]
    expected_positions = [
        Position(1, 1),
        Position(1, 6),
        Position(1, 7),
        Position(1, 8),
        Position(1, 13),
        Position(1, 14),
        Position(1, 15),
        Position(1, 16),
        Position(1, 17),
        Position(1, 26),
        Position(1, 27),
        Position(2, 1),
        Position(3, 1),
        Position(3, 2),
        Position(3, 7),
    ]
    fp = io.StringIO(text)
    lexer = Lexer(fp, special_signs=special_signs)
    tokens = get_all_tokens(lexer)
    assert len(tokens) == len(expected_types)
    assert len(tokens) == len(expected_positions)
    assert [token.type for token in tokens] == expected_types
    assert [token.position for token in tokens] == expected_positions
