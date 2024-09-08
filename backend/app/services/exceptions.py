class ServiceError(Exception):
    """Base exception for service errors."""


class ProjectNotFoundError(ServiceError):
    """Raised when a project is not found."""


class UserNotFoundError(ServiceError):
    """Raised when a user is not found."""


class WrongInitiatorError(ServiceError):
    """Raised when initiator is not found."""


class UserExistError(ServiceError):
    """Raised when a user already exists."""


class NotAllowedError(ServiceError):
    """Raised when an action is not allowed."""

    pass


class NodeNotFoundError(ServiceError):
    """Raised when node is not found"""

    pass


class NodeCannotBeDeletedError(ServiceError):
    """Raised when node is cannot be deleted"""

    pass


class NodeInDifferentTreeError(ServiceError):
    """Raised when trying reparent node to another tree"""

    pass


class TemplateDoesNotExistError(ServiceError):
    """Raised when given node template does not exist"""


class AttributeTypeNotFoundError(ServiceError):
    """Raised when attribute type does not exist"""

    pass


class NodeAttributeNotFoundError(ServiceError):
    """Raised when node attribute does not exist"""

    pass


class AttributeDoesNotExistError(ServiceError):
    """Raised when type does not contain given attribute"""

    pass


class AttributeTypeAlreadyExists(ServiceError):
    """Raised when attribute type already exist exist"""

    pass


class InvalidAttributeValueError(ServiceError):
    """Raised when attribute is being passed with wrong value"""

    pass


class FileDoesNotExistError(ServiceError):
    """Raised when given file does not exist"""

    pass


class InvalidFileFormatError(ServiceError):
    """Raised when given file with incompatible format"""

    pass


class IncompatibleNodeError(ServiceError):
    """Raised when target node does not support an operation"""

    pass


class FileTooBigError(ServiceError):
    """Raised when given file is too big"""

    pass


class EndNodeError(ServiceError):
    """Raised when trying to add a node to an end node"""

    pass
