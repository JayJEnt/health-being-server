from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str, headers: dict = None):
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers or {"WWW-Authenticate": "Bearer"}
        )

class DemandAdminAccess(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You need admin access for this action"
        )

class DemandBeingLogged(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You need to be logged in for this action"
        )

class DemandOwnerAccess(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You can perform this action only at your own data"
        )

class InvalidToken(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

class UnknownProvider(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unknown provider"
        )

class InvalidCredentials(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

class ResourceNotFound(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested resource not found"
        )

class ResourceAlreadyTaken(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Conflict, the resource is already taken"
        )

class InternalServerError(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

