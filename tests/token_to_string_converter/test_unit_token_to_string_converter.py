import io

from image_formatter.lexer.lexer import Lexer
from image_formatter.image_properties_tag_replacer.image_properties_tag_replacer import ImagePropertiesTagReplacer
from image_formatter.token_to_string_converter.token_to_string_converter import TokenToStringConverter

image_tags_properties = {
    "small": {"height": "100px", "width": "100px"},
    "small2": {"height": "110px", "width": "110px"},
}


def test_file1_literals():
    filename = "./resources/test_files/test1.txt"
    with open(filename, "r") as fp:
        expected = fp.read()
    with open(filename, "r") as fp:
        lexer = Lexer(fp)  # noqa
        image_tag_replacer = ImagePropertiesTagReplacer(lexer, image_tags_properties)
        converter = TokenToStringConverter(image_tag_replacer)
        result = converter.to_text()
    assert expected == result


def test_file2_mock():
    text = """
    1hello1 &&@small2
@small2(some/url.com)+word

    """
    expected = """
    1hello1 &&@small2
(some/url.com){: style="height:110px;width:110px"}+word

    """
    fp = io.StringIO(text)
    lexer = Lexer(fp)  # noqa
    image_tag_replacer = ImagePropertiesTagReplacer(lexer, image_tags_properties)
    converter = TokenToStringConverter(image_tag_replacer)
    result = converter.to_text()
    assert expected == result


def test_file3_classic_macos_newline():
    filename = "./resources/test_files/test3_classic_macos_newline.txt"
    with open(filename, "r") as fp:
        expected = fp.read()
    with open(filename, "r") as fp:
        lexer = Lexer(fp)  # noqa
        image_tag_replacer = ImagePropertiesTagReplacer(lexer, image_tags_properties)
        converter = TokenToStringConverter(image_tag_replacer)
        result = converter.to_text()
    assert expected == result


def test_file4_unix_and_macos_newline():
    filename = "./resources/test_files/test4_unix_and_macos_newline.txt"
    with open(filename, "r") as fp:
        expected = fp.read()
    with open(filename, "r") as fp:
        lexer = Lexer(fp)  # noqa
        image_tag_replacer = ImagePropertiesTagReplacer(lexer, image_tags_properties)
        converter = TokenToStringConverter(image_tag_replacer)
        result = converter.to_text()
    assert expected == result
