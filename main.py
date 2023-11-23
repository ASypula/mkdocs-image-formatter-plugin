from image_formatter.lexer.lexer import Lexer
from image_formatter.image_properties_tag_replacer.image_properties_tag_replacer import ImagePropertiesTagReplacer

if __name__ == "__main__":
    # filename = "tests/lexer/test_files/test1.txt"
    filename = "tests/lexer/test_files/test3.txt"
    with open(filename) as fp:
        print(type(fp))
        lexer = Lexer(fp)
        lexer.next_char()
        parser = ImagePropertiesTagReplacer(lexer)
        parser.parse()
