from src.exceptions.base import ToDoListBaseException

class ServiceException(ToDoListBaseException):
    """Base exception for the Service layer."""
    pass

class InvalidStatusTransitionException(ServiceException):
    """Raised when trying to transition a task status to an invalid state."""
    pass
