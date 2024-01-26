
class TiktokException(Exception):
    """Tiktok Custom exception class."""
    
    def __init__(self, message="Oops! Something went wrong, Please try again"):
        self.message = message
        super().__init__(self.message)