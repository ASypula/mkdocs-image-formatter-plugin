from image_formatter.lexer.lexer import Lexer
from image_formatter.lexer.token import TokenType
from image_formatter.lexer.position import Position
from tests.test_helpers import get_all_tokens
import sys
import io
import pytest
from hypothesis import strategies as st
from hypothesis import given


def two_element_tuple():
    return st.tuples(st.text(min_size=1), st.text(min_size=1))


def lexer_configuration():
    return st.fixed_dictionaries(
        {
            "special_signs": two_element_tuple(),
            "newline_characters": two_element_tuple(),
            "additional_path_signs": two_element_tuple(),
        }
    )


# TODO: add hypothesis tests
