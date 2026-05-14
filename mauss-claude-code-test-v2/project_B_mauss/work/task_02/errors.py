"""Custom exceptions for the async retry HTTP client."""


class ClientError(Exception):
    """Raised for non-retryable client-side HTTP errors (4xx status codes)."""

    def __init__(self, status: int, body: str = "", url: str = ""):
        self.status = status
        self.body = body
        self.url = url
        super().__init__(f"ClientError {status} for {url!r}: {body!r}")


class RetryExhausted(Exception):
    """Raised when max_retries have all failed; wraps the last underlying error."""

    def __init__(self, attempts: int, last_error: BaseException, url: str = ""):
        self.attempts = attempts
        self.last_error = last_error
        self.url = url
        super().__init__(
            f"RetryExhausted after {attempts} attempts for {url!r}; "
            f"last_error={type(last_error).__name__}: {last_error}"
        )
