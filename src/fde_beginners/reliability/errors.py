class IntegrationError(Exception):
    """A safe, structured integration failure."""

    def __init__(self, code: str, attempts: int, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.attempts = attempts


class UpstreamUnavailable(IntegrationError):
    pass


class ValidationFailure(IntegrationError):
    pass
