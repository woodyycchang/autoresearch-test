"""Custom error types for the RetryClient."""


class ClientError(Exception):
    """Raised on non-retryable client errors (HTTP 4xx)."""

    def __init__(self, status, body=None, message=None):
        self.status = status
        self.body = body
        msg = message or f"Client error {status}"
        super().__init__(msg)


class RetryExhausted(Exception):
    """Raised when all retries have been exhausted."""

    def __init__(self, last_error, attempts):
        self.last_error = last_error
        self.attempts = attempts
        super().__init__(
            f"Retries exhausted after {attempts} attempts; last error: {last_error!r}"
        )
