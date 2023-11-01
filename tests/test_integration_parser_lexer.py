from image_formatter.lexer.lexer import Lexer
from image_formatter.parser.parser import Parser
import io


def setup_parser(request):
    fp = io.StringIO(request)
    lexer = Lexer(fp)
    lexer.next_char()
    parser = Parser(lexer)
    return parser


def test_given_no_image_links_then_nothing_is_returned():
    parser = setup_parser("word1, word2 $$ @tag1-tag \n\n @tag2 x (start-of/url.png)")
    result = []
    for link in parser.parse():
        result.append(link)
    assert result == []


def test_given_no_input_then_nothing_is_returned():
    parser = setup_parser("")
    result = []
    for link in parser.parse():
        result.append(link)
    assert result == []


def test_given_only_image_link_then_image_link_returned():
    parser = setup_parser("   @small \n (some/url.png)")
    result = []
    for link in parser.parse():
        result.append(link)
    assert result == [("small", "some/url.png")]


def test_given_image_links_mixed_with_other_tokens_then_image_links_returned():
    parser = setup_parser(
        "   @small \n (some/url.png) & word @big(next/longer.url.jpg)  word2"
    )
    result = []
    for link in parser.parse():
        result.append(link)
    assert result[0] == ("small", "some/url.png")
    assert result[1] == ("big", "next/longer.url.jpg")


def test_given_one_image_link_mixed_with_other_tokens_then_image_link_returned():
    parser = setup_parser(
        "   @small \n (some/url.png) & word @big *(next/longer.url.jpg)  word2"
    )
    result = []
    for link in parser.parse():
        result.append(link)
    assert len(result) == 1
    assert result[0] == ("small", "some/url.png")
