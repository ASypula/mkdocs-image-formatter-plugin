from image_formatter.lexer.token_stream_processor import TokenStreamProcessor
from image_formatter.lexer.token import TagToken


class TokenToStringConverter:
    def __init__(self, token_stream_processor: TokenStreamProcessor):
        self.token_stream_processor = token_stream_processor

    def to_text(self) -> str:
        text = ""
        for token in self.get_all_tokens():
            if type(token) == TagToken:
                text += f"{token.tag_character}"
            text += token.string
        return text

    def get_all_tokens(self) -> list:
        tokens = []
        for t in self.token_stream_processor.get_token():
            tokens.append(t)
        return tokens
