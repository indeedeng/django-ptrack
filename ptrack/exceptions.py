class PtrackError(Exception):
    """Base class for errors raised in Ptrack."""


class PtrackRegistrationError(PtrackError):
    """Error raised when Ptrack tracking pixel fails to register."""


class PtrackKeyTooLong(PtrackError):
    """Error raised when secret key > 32"""
