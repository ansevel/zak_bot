class BotError(Exception):
    """Base class for bot errors"""
    pass


class ParserConnectError(BotError):
    """Connection error during parser request"""
    pass
