from unittest.mock import Mock
from image_formatter.parser.parser import Parser
from image_formatter.lexer.token import Token, TokenType
from image_formatter.error_handler.error_handler import ErrorHandler
from image_formatter.error_handler.errors import UnexpectedTagException
from tests.test_helpers import get_all_parser_results


def test_given_tag_when_not_followed_by_url_then_exception_is_registered():
    mock_lexer = Mock()
    mock_lexer.get_token.side_effect = [
        Token(TokenType.T_IMAGE_SIZE_TAG, "small"),
        Token(TokenType.T_CHAR, "$"),
        "",
    ]
    error_handler = ErrorHandler()
    parser = Parser(mock_lexer, error_handler)
    get_all_parser_results(parser, 1)
    assert len(error_handler.errors) == 1
    assert error_handler.errors == [UnexpectedTagException(TokenType.T_IMAGE_URL, TokenType.T_CHAR)]
