from src.exceptions.base import ToDoListBaseException

class RepositoryException(ToDoListBaseException):
    """Base exception for the Repository layer."""
    pass

class NotFoundException(RepositoryException):
    """Raised when an entity is not found in the database (e.g., Project ID not found)."""
    def __init__(self, message="Entity not found."):
        self.message = message
        super().__init__(self.message)

class AlreadyExistsException(RepositoryException):
    """Raised when trying to create an entity that already exists (e.g., unique constraint violation)."""
    pass
