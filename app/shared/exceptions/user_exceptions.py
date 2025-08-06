class UserException(Exception):
    """Base exception for user-related errors"""
    pass

class UserNotFoundError(UserException):
    """Raised when a user is not found"""
    pass

class UserAlreadyExistsError(UserException):
    """Raised when trying to create a user that already exists"""
    pass

class UserValidationError(UserException):
    """Raised when user data validation fails"""
    pass 