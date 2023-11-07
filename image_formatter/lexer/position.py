class Position:
    def __init__(self, line, column):
        self.line = line
        self.column = column

    def move_to_next_line(self) -> None:
        self.line += 1
        self.column = 1

    def move_right(self) -> None:
        self.column += 1

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False

        return (self.line == other.line) and (self.column == other.column)

    def __str__(self) -> str:
        return f"<{self.line}:{self.column}>"

    def __repr__(self) -> str:
        return self.__str__()
