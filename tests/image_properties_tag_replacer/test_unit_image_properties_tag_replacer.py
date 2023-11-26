from unittest.mock import Mock
from image_formatter.image_properties_tag_replacer.image_properties_tag_replacer import ImagePropertiesTagReplacer
from image_formatter.lexer.token import TokenType, Token
from image_formatter.lexer.position import Position
from tests.test_helpers import get_all_tags_replacer_results

# @ TODO inline global var
image_tags_properties = {
    "small": {"height": "100px", "width": "100px"},
    "medium": {"height": "150px", "width": "150px"},
}


def test_given_only_one_image_link_then_one_image_link_returned():
    mock_lexer = Mock()
    mock_lexer.get_token.side_effect = [
        Token(TokenType.T_IMAGE_SIZE_TAG, Position(1, 1), "small"),
        Token(TokenType.T_IMAGE_URL, Position(2, 1), "(some/url.png)"),
        "",
    ]
    tags_replacer = ImagePropertiesTagReplacer(mock_lexer, image_tags_properties)
    result = get_all_tags_replacer_results(tags_replacer, 1)
    assert len(result) == 1
    assert result[0] == Token(
        TokenType.T_IMAGE_URL_WITH_PROPERTIES, Position(2, 1), '(some/url.png){: style="height:100px;width:100px"}'
    )


def test_given_only_image_links_then_only_image_links_returned():
    mock_lexer = Mock()
    mock_lexer.get_token.side_effect = [
        Token(TokenType.T_IMAGE_SIZE_TAG, Position(1, 1), "small"),
        Token(TokenType.T_IMAGE_URL, Position(2, 1), "(some/url.png)"),
        Token(TokenType.T_IMAGE_SIZE_TAG, Position(3, 1), "medium"),
        Token(TokenType.T_IMAGE_URL, Position(4, 1), "(medium-url.png)"),
        "",
    ]
    expected_tokens = [
        Token(
            TokenType.T_IMAGE_URL_WITH_PROPERTIES, Position(2, 1), '(some/url.png){: style="height:100px;width:100px"}'
        ),
        Token(
            TokenType.T_IMAGE_URL_WITH_PROPERTIES,
            Position(4, 1),
            '(medium-url.png){: style="height:150px;width:150px"}',
        ),
    ]
    tags_replacer = ImagePropertiesTagReplacer(mock_lexer, image_tags_properties)
    result = get_all_tags_replacer_results(tags_replacer, 2)
    assert len(result) == 2
    assert result == expected_tokens


def test_given_tag_and_url_separated_by_char_then_only_false_returned():
    mock_lexer = Mock()
    mock_lexer.get_token.side_effect = [
        Token(TokenType.T_IMAGE_SIZE_TAG, Position(1, 1), "small"),
        Token(TokenType.T_CHAR, Position(2, 1), "*"),
        Token(TokenType.T_IMAGE_URL, Position(3, 1), "(some/url.png)"),
        Token(TokenType.T_EOF, Position(4, 1), ""),
    ]
    expected_tokens = [
        Token(TokenType.T_IMAGE_SIZE_TAG, Position(1, 1), "small"),
        Token(TokenType.T_CHAR, Position(2, 1), "*"),
        Token(TokenType.T_IMAGE_URL, Position(3, 1), "(some/url.png)"),
    ]
    tags_replacer = ImagePropertiesTagReplacer(mock_lexer, image_tags_properties)
    result = []

    for link in tags_replacer.get_token():
        result.append(link)
    assert result == expected_tokens


def test_given_no_tags_or_urls_then_only_false_returned():
    mock_lexer = Mock()
    mock_lexer.get_token.side_effect = [
        Token(TokenType.T_CHAR, Position(1, 1), "*"),
        Token(TokenType.T_CHAR, Position(2, 1), "*"),
        Token(TokenType.T_LITERAL, Position(3, 1), "hello"),
        Token(TokenType.T_EOF, Position(4, 1), ""),
    ]
    expected_tokens = [
        Token(TokenType.T_CHAR, Position(1, 1), "*"),
        Token(TokenType.T_CHAR, Position(2, 1), "*"),
        Token(TokenType.T_LITERAL, Position(3, 1), "hello"),
    ]
    tags_replacer = ImagePropertiesTagReplacer(mock_lexer, image_tags_properties)
    result = []

    for link in tags_replacer.get_token():
        result.append(link)
    assert result == expected_tokens


def test_given_url_and_tag_token_in_reverted_order_then_only_false_returned():
    mock_lexer = Mock()
    mock_lexer.get_token.side_effect = [
        Token(TokenType.T_IMAGE_URL, Position(1, 1), "(some/url.png)"),
        Token(TokenType.T_IMAGE_SIZE_TAG, Position(2, 1), "medium"),
        "",
    ]
    tags_replacer = ImagePropertiesTagReplacer(mock_lexer, image_tags_properties)
    result = get_all_tags_replacer_results(tags_replacer, 2)
    assert len(result) == 2
    assert all(value is False for value in result)
