# Custom exception class, that contains message and status code


class ResponseStatusError(Exception):
    def __init__(self, message, status):
        self.message = message
        self.status = status
        super().__init__(self.message)
