from typing import Callable

from github.GithubException import (
                                    BadCredentialsException,
                                    UnknownObjectException
                                )

class TokenMissingError(Exception):
    """Exception raised when a required token is missing."""

    def __init__(self, message="A required token is missing."):
        self.message = message
        super().__init__(self.message)

class BadCredentialsError(Exception):
    """Exception raised for bad credentials."""

    def __init__(self, message="Provided credentials are invalid. Please, verify your token."):
        self.message = message
        super().__init__(self.message)

class NotFoundError(Exception):
    """Exception raised when a requested resource is not found."""

    def __init__(self, resource_type: str = "Resource", resource_identifier: str = ""):
        self.message = f"{resource_type} '{resource_identifier}' not found."
        super().__init__(self.message)

class AlreadyExistsError(Exception):
    """Exception raised when a resource already exists."""

    def __init__(self, resource_type: str = "Resource", resource_identifier: str = ""):
        self.message = f"{resource_type} '{resource_identifier}' already exists."
        super().__init__(self.message)