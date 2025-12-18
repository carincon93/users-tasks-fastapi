class UserNotFoundError(Exception):
    def __init__(self):
        self.detail = "User not found"
        self.status_code = 404