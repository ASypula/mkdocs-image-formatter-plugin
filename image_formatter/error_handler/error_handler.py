class ErrorHandler:
    def __init__(self):
        self.errors = []

    def handle(self, err: Exception) -> None:
        self.errors.append(err)
