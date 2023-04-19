class RequirementAuditorException(Exception):
    pass


class DatabaseError(RequirementAuditorException):
    pass


class LibraryNotFoundError(RequirementAuditorException):
    """Library not found on external services like PyPi for example."""

class ConfigurationError(RequirementAuditorException):
    pass


class ParsingError(RequirementAuditorException):
    """Error parsing"""
