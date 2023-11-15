class Position:
    """
    Class position represents cursor position in text / text stream.
    """

    def __init__(self, line: int = 1, column: int = 1):
        """
        Args:
            line: line number in analyzed text / text stream
            column: column number in analyzed text / text stream
        """
        self.line = line
        self.column = column

    def move_to_next_line(self) -> None:
        """
        Updates position to represent the position before the first character in next line of the text.
        """
        self.line += 1
        self.column = 1

    def move_right(self) -> None:
        """
        Updates position to represent the next character in current line of the text.
        """
        self.column += 1

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False

        return (self.line == other.line) and (self.column == other.column)

    def __str__(self) -> str:
        return f"<{self.line}:{self.column}>"

    def __repr__(self) -> str:
        return self.__str__()
