class UserNotFoundError(Exception):
    def __init__(self):
        self.detail = "User not found"
        self.status_code = 404
    

class InsufficientPermission(Exception):
    def __init__(self):
        self.detail = "Insufficient permission"
        self.status_code = 403