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


def test_given_tag_when_followed_by_another_tag_with_url_then_exception_is_registered_and_tag_is_parsed():
    mock_lexer = Mock()
    mock_lexer.get_token.side_effect = [
        Token(TokenType.T_IMAGE_SIZE_TAG, "small"),
        Token(TokenType.T_IMAGE_SIZE_TAG, "small-2"),
        Token(TokenType.T_IMAGE_URL, "some/url.png"),
        "",
    ]
    error_handler = ErrorHandler()
    parser = Parser(mock_lexer, error_handler)
    result = get_all_parser_results(parser, 2)

    assert len(error_handler.errors) == 1
    assert error_handler.errors == [UnexpectedTagException(TokenType.T_IMAGE_URL, TokenType.T_IMAGE_SIZE_TAG)]
    assert len(result) == 2
    assert result[0] is False
    assert result[1] == ("small-2", "some/url.png")
