class TokenMissingError(Exception):
    """Exception raised when a required token is missing."""

    def __init__(self, message="A required token is missing."):
        self.message = message
        super().__init__(self.message)