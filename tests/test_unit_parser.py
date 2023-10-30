from mock import patch
from image_formatter.parser.parser import Parser
from image_formatter.lexer.token import TokenType, Token
from tests.test_helpers import get_all_parser_results


@patch("image_formatter.lexer.lexer.Lexer")
def test_given_only_one_image_link_then_one_image_link_returned(mock_lexer):
    with patch("image_formatter.lexer.lexer.Lexer.get_token") as mock_get_token:
        tokens = [
            Token(TokenType.T_IMAGE_SIZE_TAG, "small"),
            Token(TokenType.T_IMAGE_URL, "some/url.png"),
            "",
        ]
        mock_get_token.side_effect = tokens
        parser = Parser(mock_lexer)
        result = get_all_parser_results(parser, 1)
        assert len(result) == 1
        assert result[0] == ("small", "some/url.png")


@patch("image_formatter.lexer.lexer.Lexer")
def test_given_only_image_links_then_only_image_links_returned(mock_lexer):
    with patch("image_formatter.lexer.lexer.Lexer.get_token") as mock_get_token:
        tokens = [
            Token(TokenType.T_IMAGE_SIZE_TAG, "small"),
            Token(TokenType.T_IMAGE_URL, "some/url.png"),
            Token(TokenType.T_IMAGE_SIZE_TAG, "medium"),
            Token(TokenType.T_IMAGE_URL, "medium-url.png"),
            "",
        ]
        mock_get_token.side_effect = tokens
        parser = Parser(mock_lexer)
        result = get_all_parser_results(parser, 2)
        assert len(result) == 2
        assert result[0] == ("small", "some/url.png")
        assert result[1] == ("medium", "medium-url.png")


@patch("image_formatter.lexer.lexer.Lexer")
def test_given_image_links_separated_by_Nones_then_only_image_links_returned(
    mock_lexer,
):
    with patch("image_formatter.lexer.lexer.Lexer.get_token") as mock_get_token:
        tokens = [
            Token(TokenType.T_IMAGE_SIZE_TAG, "small"),
            None,
            Token(TokenType.T_IMAGE_URL, "some/url.png"),
            Token(TokenType.T_IMAGE_SIZE_TAG, "medium"),
            None,
            Token(TokenType.T_IMAGE_URL, "medium-url.png"),
            "",
        ]
        mock_get_token.side_effect = tokens
        parser = Parser(mock_lexer)
        result = get_all_parser_results(parser, 2)
        assert len(result) == 2
        assert result[0] == ("small", "some/url.png")
        assert result[1] == ("medium", "medium-url.png")


@patch("image_formatter.lexer.lexer.Lexer")
def test_given_tag_and_url_separated_by_char_then_only_False_returned(mock_lexer):
    with patch("image_formatter.lexer.lexer.Lexer.get_token") as mock_get_token:
        tokens = [
            Token(TokenType.T_IMAGE_SIZE_TAG, "small"),
            Token(TokenType.T_CHAR, "*"),
            Token(TokenType.T_IMAGE_URL, "some/url.png"),
            "",
        ]
        mock_get_token.side_effect = tokens
        parser = Parser(mock_lexer)
        result = get_all_parser_results(parser, len(tokens) - 1)
        assert len(result) == 3
        assert all(value == False for value in result)


@patch("image_formatter.lexer.lexer.Lexer")
def test_given_no_tags_or_urls_then_only_False_returned(mock_lexer):
    with patch("image_formatter.lexer.lexer.Lexer.get_token") as mock_get_token:
        tokens = [
            Token(TokenType.T_CHAR, "*"),
            None,
            Token(TokenType.T_CHAR, "*"),
            Token(TokenType.T_LITERAL, "hello"),
            "",
        ]
        mock_get_token.side_effect = tokens
        parser = Parser(mock_lexer)
        result = get_all_parser_results(parser, len(tokens) - 1)
        assert len(result) == 4
        assert all(value == False for value in result)


@patch("image_formatter.lexer.lexer.Lexer")
def test_given_url_and_tag_token_in_reverted_order_then_only_False_returned(mock_lexer):
    with patch("image_formatter.lexer.lexer.Lexer.get_token") as mock_get_token:
        tokens = [
            Token(TokenType.T_IMAGE_URL, "some/url.png"),
            Token(TokenType.T_IMAGE_SIZE_TAG, "medium"),
            "",
        ]
        mock_get_token.side_effect = tokens
        parser = Parser(mock_lexer)
        result = get_all_parser_results(parser, len(tokens) - 1)
        assert len(result) == 2
        assert all(value == False for value in result)
