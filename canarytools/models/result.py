from .base import CanaryToolsBase


class Result(CanaryToolsBase):
    def __init__(self, console, data):
        """Initialize Result. To be used as a result indicator

        :param console: The Console from which API calls are made
        :param data: JSON data

        **Attributes:**
            - **result** -- The result of the call. Usually 'success' or 'error'.
        """
        super(Result, self).__init__(console, data)

    def __str__(self):
        """Helper method
        """
        info = ""
        for key, value in vars(self).items():
            # exclude these from the string
            if 'console' == key:
                continue
            else:
                info += " {key}: {value}".format(
                    key=str(key), value=str(value))

        return "[Result] {info}".format(info=info)
