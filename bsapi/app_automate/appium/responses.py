class DeleteResponse:
    """
    Response for delete requests sents to BrowserStack

    :param str status: Status of the delete request
    :param str message: Message from the server
    """
    def __init__(self, status=None, message=None):
        self.status = status
        self.message = message
