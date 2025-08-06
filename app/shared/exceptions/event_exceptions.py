class EventException(Exception):
    """Base exception for event-related errors"""
    pass

class EventNotFoundError(EventException):
    """Raised when an event is not found"""
    pass

class EventAlreadyExistsError(EventException):
    """Raised when trying to create an event that already exists"""
    pass

class EventValidationError(EventException):
    """Raised when event data validation fails"""
    pass 