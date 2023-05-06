class QRCodeNotFound(Exception):
    """This exception should be raised if a QR code can not be found
    on the Discord login page.
    """

    pass


class InvalidToken(Exception):
    """This exception should be raised if a token does not receive
    a response status code of 200 when tested against Discord's API.
    """

    pass


class WebhookSendFailure(Exception):
    """This exception should be raised if the token webhook fails
    to send, for whatever reason.
    """

    pass
