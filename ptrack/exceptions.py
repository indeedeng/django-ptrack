class PtrackError(Exception):
    """Base class for errors raised in Ptrack."""


class PtrackRegistrationError(PtrackError):
    """Error raised when Ptrack tracking pixel fails to register."""
