class NotAuthenticatedError(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return "You must be authenticated to use this methode"

class AddBeforeNewError(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return "You can use add methode before the new methode"
