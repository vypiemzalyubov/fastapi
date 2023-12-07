from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    def __init__(self,
                 status_code: int = status.HTTP_404_NOT_FOUND,
                 detail: str = "User not found",
                 solution: str = "Enter the correct username"):
        super().__init__(status_code=status_code, detail=detail)
        self.solution = solution


class InvalidUserCookiesException(HTTPException):
    def __init__(self,
                 status_code: int = status.HTTP_401_UNAUTHORIZED,
                 detail: str = "Unauthorized",
                 solution: str = "You need to get a valid cookie"):
        super().__init__(status_code=status_code, detail=detail)
        self.solution = solution
