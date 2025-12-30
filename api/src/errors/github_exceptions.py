class GithubException(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(message, status_code)
        self._message = message
        self._status_code = status_code
    
    @property
    def message(self) -> str:
        return self._message
    
    @property
    def status_code(self) -> int:
        return self._status_code

    def send_error(self):
        return {
            'message': self._message,
            'status_code': self._status_code
        }

class TokenMissingError(GithubException):
    """Exception raised when a required token is missing."""

    def __init__(self, message="A required token is missing."):
        super().__init__(message, 400)

class BadCredentialsError(GithubException):
    """Exception raised for bad credentials."""

    def __init__(self, message="Provided credentials are invalid. Please, verify your token."):
        super().__init__(message, 403)

class NotFoundError(GithubException):
    """Exception raised when a requested resource is not found."""

    def __init__(self, resource_type: str = "Resource", resource_identifier: str = ""):
        message = f"{resource_type} '{resource_identifier}' not found."
        super().__init__(message, 404)

class AlreadyExistsError(GithubException):
    """Exception raised when a resource already exists."""

    def __init__(self, resource_type: str = "Resource", resource_identifier: str = ""):
        message = f"{resource_type} '{resource_identifier}' already exists."
        super().__init__(message, 400)