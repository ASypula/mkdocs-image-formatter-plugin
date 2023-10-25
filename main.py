from lexer.lexer import Lexer

if __name__ == "__main__":
    # filename = "lexer_examples/test1.txt"
    filename = "lexer_examples/test2.txt"
    with open(filename) as fp:
        lexer = Lexer(fp)
        lexer.next_char()
        i = 0
        while lexer.running:
            token = lexer.get_token()
            if token:
                print(f"{i}. Token: {token.type.name}, value: {token.string}")
                i += 1
            else:
                lexer.next_char()
