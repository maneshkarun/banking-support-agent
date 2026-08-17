"""Domain-level exceptions."""


class NotFoundError(Exception):
    """Raised when a requested domain entity does not exist."""


class ConflictError(Exception):
    """Raised when a request conflicts with existing state."""


class BusinessRuleError(Exception):
    """Raised when an operation violates a banking business rule."""

