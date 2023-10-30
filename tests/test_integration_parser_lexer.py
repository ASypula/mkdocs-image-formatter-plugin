from image_formatter.lexer.lexer import Lexer
from image_formatter.parser.parser import Parser
from tests.test_helpers import get_all_parser_results
import io
import pytest


@pytest.fixture
def setup_parser(request):
    fp = io.StringIO(request.param)
    lexer = Lexer(fp)
    lexer.next_char()
    parser = Parser(lexer)
    return parser


@pytest.mark.parametrize(
    "setup_parser",
    ["word1, word2 $$ @tag1-tag \n\n @tag2 x (start-of/url.png)"],
    indirect=True,
)
def test_given_no_image_links_then_nothing_is_returned(setup_parser):
    result = get_all_parser_results(setup_parser)
    assert len(result) == 0


@pytest.mark.parametrize("setup_parser", [""], indirect=True)
def test_given_no_input_then_nothing_is_returned(setup_parser):
    result = get_all_parser_results(setup_parser)
    assert len(result) == 0


@pytest.mark.parametrize("setup_parser", ["   @small \n (some/url.png)"], indirect=True)
def test_given_only_image_link_then_image_link_returned(setup_parser):
    result = get_all_parser_results(setup_parser)
    tag, url = result[0]
    assert len(result) == 1
    assert tag == "small"
    assert url == "some/url.png"


@pytest.mark.parametrize(
    "setup_parser",
    ["   @small \n (some/url.png) & word @big(next/longer.url.jpg)  word2"],
    indirect=True,
)
def test_given_image_links_mixed_with_other_tokens_then_image_links_returned(
    setup_parser,
):
    result = get_all_parser_results(setup_parser)
    assert len(result) == 2
    assert result[0] == ("small", "some/url.png")
    assert result[1] == ("big", "next/longer.url.jpg")


@pytest.mark.parametrize(
    "setup_parser",
    ["   @small \n (some/url.png) & word @big *(next/longer.url.jpg)  word2"],
    indirect=True,
)
def test_given_one_image_link_mixed_with_other_tokens_then_image_link_returned(
    setup_parser,
):
    result = get_all_parser_results(setup_parser)
    assert len(result) == 1
    assert result[0] == ("small", "some/url.png")
