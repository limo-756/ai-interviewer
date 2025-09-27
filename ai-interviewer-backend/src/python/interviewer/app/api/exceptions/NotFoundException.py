class NotFoundException(Exception):

    def __init__(self, message):
        super().__init__(self.message)
        self.message = message
        self.status_code = 404
