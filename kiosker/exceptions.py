"""Custom exceptions for the Kiosker API."""


class KioskerError(Exception):
    """Base exception for Kiosker API errors."""

class ConnectionError(KioskerError):
    """Exception raised when connection to Kiosker device fails."""

class AuthenticationError(KioskerError):
    """Exception raised when authentication fails."""

class IPAuthenticationFailed(KioskerError):
    """Exception raised when ip-list authentication fails."""

class TLSVerificationFailed(KioskerError):
    """Exception raised when access is denied."""

class BadRequestError(KioskerError):
    """Exception raised when the request is invalid."""

class InvalidResponseError(KioskerError):
    """Exception raised when device returns invalid response."""
    
class PingError(KioskerError):
    """Exception raised when ping fails."""