class BotError(Exception):
    """Base class for bot errors"""
    pass


class ParserConnectError(BotError):
    """Connection error during parser request"""
    pass


class PurchaseNotFoundError(BotError):
    """If parser resonse status is 404"""
    pass
