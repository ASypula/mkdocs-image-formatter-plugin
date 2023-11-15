from unittest.mock import Mock
from image_formatter.parser.parser import Parser
from image_formatter.lexer.token import TokenType, Token
from image_formatter.lexer.position import Position
from tests.test_helpers import get_all_parser_results


def test_given_only_one_image_link_then_one_image_link_returned():
    mock_lexer = Mock()
    mock_lexer.get_token.side_effect = [
        Token(TokenType.T_IMAGE_SIZE_TAG, Position(1, 1), "small"),
        Token(TokenType.T_IMAGE_URL, Position(2, 1), "some/url.png"),
        "",
    ]
    parser = Parser(mock_lexer)
    result = get_all_parser_results(parser, 1)
    assert len(result) == 1
    assert result[0] == ("small", "some/url.png")


def test_given_only_image_links_then_only_image_links_returned():
    mock_lexer = Mock()
    mock_lexer.get_token.side_effect = [
        Token(TokenType.T_IMAGE_SIZE_TAG, Position(1, 1), "small"),
        Token(TokenType.T_IMAGE_URL, Position(2, 1), "some/url.png"),
        Token(TokenType.T_IMAGE_SIZE_TAG, Position(3, 1), "medium"),
        Token(TokenType.T_IMAGE_URL, Position(4, 1), "medium-url.png"),
        "",
    ]
    parser = Parser(mock_lexer)
    result = get_all_parser_results(parser, 2)
    assert len(result) == 2
    assert result[0] == ("small", "some/url.png")
    assert result[1] == ("medium", "medium-url.png")


def test_given_image_links_separated_by_Nones_then_only_image_links_returned():
    mock_lexer = Mock()
    mock_lexer.get_token.side_effect = [
        Token(TokenType.T_IMAGE_SIZE_TAG, Position(1, 1), "small"),
        None,
        Token(TokenType.T_IMAGE_URL, Position(2, 1), "some/url.png"),
        Token(TokenType.T_IMAGE_SIZE_TAG, Position(3, 1), "medium"),
        None,
        Token(TokenType.T_IMAGE_URL, Position(4, 1), "medium-url.png"),
        "",
    ]
    parser = Parser(mock_lexer)
    result = get_all_parser_results(parser, 2)
    assert len(result) == 2
    assert result[0] == ("small", "some/url.png")
    assert result[1] == ("medium", "medium-url.png")


def test_given_tag_and_url_separated_by_char_then_only_False_returned():
    mock_lexer = Mock()
    mock_lexer.get_token.side_effect = [
        Token(TokenType.T_IMAGE_SIZE_TAG, Position(1, 1), "small"),
        Token(TokenType.T_CHAR, Position(2, 1), "*"),
        Token(TokenType.T_IMAGE_URL, Position(3, 1), "some/url.png"),
        "",
    ]
    parser = Parser(mock_lexer)
    result = get_all_parser_results(parser, 3)
    assert len(result) == 3
    assert all(value is False for value in result)


def test_given_no_tags_or_urls_then_only_False_returned():
    mock_lexer = Mock()
    mock_lexer.get_token.side_effect = [
        Token(TokenType.T_CHAR, Position(1, 1), "*"),
        None,
        Token(TokenType.T_CHAR, Position(2, 1), "*"),
        Token(TokenType.T_LITERAL, Position(3, 1), "hello"),
        "",
    ]
    parser = Parser(mock_lexer)
    result = get_all_parser_results(parser, 4)
    assert len(result) == 4
    assert all(value is False for value in result)


def test_given_url_and_tag_token_in_reverted_order_then_only_False_returned():
    mock_lexer = Mock()
    mock_lexer.get_token.side_effect = [
        Token(TokenType.T_IMAGE_URL, Position(1, 1), "some/url.png"),
        Token(TokenType.T_IMAGE_SIZE_TAG, Position(2, 1), "medium"),
        "",
    ]
    parser = Parser(mock_lexer)
    result = get_all_parser_results(parser, 2)
    assert len(result) == 2
    assert all(value is False for value in result)
