from image_formatter.lexer.token_sequence import TokenSequence
from image_formatter.lexer.token import TagToken


class TokenToStringConverter:
    def __init__(self, token_sequence: TokenSequence):
        self.token_sequence = token_sequence

    def to_text(self) -> str:
        text = ""
        for token in self.get_all_tokens():
            if type(token) == TagToken:
                text += f"{token.tag_character}"
            text += token.string
        return text

    def get_all_tokens(self) -> list:
        tokens = []
        for t in self.token_sequence.get_token():
            tokens.append(t)
        return tokens
