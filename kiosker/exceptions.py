"""Custom exceptions for the Kiosker API."""


class KioskerException(Exception):
    """Base exception for Kiosker API errors."""

class ConnectionError(KioskerException):
    """Exception raised when connection to Kiosker device fails."""

class AuthenticationError(KioskerException):
    """Exception raised when authentication fails."""

class IPAuthenticationError(KioskerException):
    """Exception raised when ip-list authentication fails."""

class TLSVerificationError(KioskerException):
    """Exception raised when access is denied."""

class BadRequestError(KioskerException):
    """Exception raised when the request is invalid."""
    
class NotFoundError(KioskerException):
    """Exception raised when the requested object doesn't exist."""

class ConflictError(KioskerException):
    """Exception raised when the operation is blocked, eg. because the setting is managed by MDM."""

class PingError(KioskerException):
    """Exception raised when ping fails."""
