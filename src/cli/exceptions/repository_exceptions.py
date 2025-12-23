class NotFoundException(Exception):
    """Raised when an entity (project or task) is not found."""
    pass

class AlreadyExistsException(Exception):
    """Raised when trying to create a project with a duplicate name."""
    pass

class MaxLimitExceededException(Exception):
    """Raised when maximum number of projects or tasks is reached."""
    pass

class InvalidStatusTransitionException(Exception):
    """Raised when trying to change a completed (done) task status."""
    pass
