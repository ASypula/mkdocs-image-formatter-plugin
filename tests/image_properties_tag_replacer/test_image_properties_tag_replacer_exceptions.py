from unittest.mock import Mock
from image_formatter.image_properties_tag_replacer.image_properties_tag_replacer import ImagePropertiesTagReplacer
from image_formatter.lexer.token import Token, TokenType
from image_formatter.error_handler.error_handler import ErrorHandler
from image_formatter.error_handler.errors import UnexpectedTagException
from image_formatter.lexer.position import Position
from tests.test_helpers import get_all_tags_replacer_results

# @ TODO inline global var
image_tags_properties = {
    "small": {"height": "100px", "width": "100px"},
    "small-2": {"height": "110px", "width": "110px"},
}


def test_given_tag_when_not_followed_by_url_then_exception_is_registered():
    mock_lexer = Mock()
    mock_lexer.get_token.side_effect = [
        Token(TokenType.T_IMAGE_SIZE_TAG, Position(1, 1), "small"),
        Token(TokenType.T_CHAR, Position(2, 1), "$"),
        "",
    ]
    error_handler = ErrorHandler()
    tags_replacer = ImagePropertiesTagReplacer(mock_lexer, image_tags_properties, error_handler)
    get_all_tags_replacer_results(tags_replacer, 1)
    assert len(error_handler.errors) == 1
    assert error_handler.errors == [UnexpectedTagException(TokenType.T_IMAGE_URL, TokenType.T_CHAR)]


def test_given_tag_when_followed_by_another_tag_with_url_then_exception_is_registered_and_tag_is_parsed():
    mock_lexer = Mock()
    mock_lexer.get_token.side_effect = [
        Token(TokenType.T_IMAGE_SIZE_TAG, Position(1, 1), "small"),
        Token(TokenType.T_IMAGE_SIZE_TAG, Position(2, 1), "small-2"),
        Token(TokenType.T_IMAGE_URL, Position(3, 1), "(some/url.png)"),
        "",
    ]
    error_handler = ErrorHandler()
    tags_replacer = ImagePropertiesTagReplacer(mock_lexer, image_tags_properties, error_handler)
    expected_tokens = [
        Token(TokenType.T_IMAGE_SIZE_TAG, Position(1, 1), "small"),
        Token(
            TokenType.T_IMAGE_URL_WITH_PROPERTIES, Position(3, 1), '(some/url.png){: style="height:110px;width:110px"}'
        ),
    ]
    result = get_all_tags_replacer_results(tags_replacer, 2)

    assert len(error_handler.errors) == 1
    assert error_handler.errors == [UnexpectedTagException(TokenType.T_IMAGE_URL, TokenType.T_IMAGE_SIZE_TAG)]
    assert len(result) == 2
    assert result == expected_tokens
