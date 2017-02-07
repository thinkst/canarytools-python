class ConsoleError(Exception):
    """Ambiguous exception occurred while using the Console API."""
    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        super(ConsoleError, self).__init__(*args, **kwargs)

    def __str__(self):
        if len(self.args) > 0:
            return self.args[0]
        else:
            return "To our eternal shame... Something went wrong. Sorry."


class ConfigurationError(ConsoleError):
    """Configuration missing"""


class InvalidAuthTokenError(ConsoleError):
    """Invalid Authorization Token"""
    def __str__(self):
        return "Invalid Authorization Token"


class ConnectionError(ConsoleError):
    """Connection error occurred"""


class DeviceNotFoundError(ConsoleError):
    """Device could not be found"""
    """Invalid Authorization Token"""
    def __str__(self):
        return "Device could not be found"


class IncidentNotFoundError(ConsoleError):
    """Incident not found"""
    def __str__(self):
        return "Incident could not be found. It may have been deleted."


class InvalidParameterError(ConsoleError):
    """Invalid parameter(s)"""


class UpdateError(ConsoleError):
    """Update not permitted"""


class FileNotFound(ConsoleError):
    """File not found"""


class CanaryTokenError(ConsoleError):
    """Something went wrong while calling the tokens API"""


class IncidentError(ConsoleError):
    """Something went wrong while working with Incidents"""
