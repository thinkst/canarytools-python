class CanaryToolsBase(object):
    @classmethod
    def parse(cls, console, data):
        """Initialize model

        :param data: JSON data to parse
        :param console: Console object from which API calls are made
        :return: Initializes sub-class
        """
        return cls(console, data)

    def __init__(self, console, data):
        """Initialize CanaryToolsBase and set all JSON key-value pairs as the
            objects attributes

        :param console: Console object from which API calls are made
        :param data: JSON data to parse
        """
        self.console = console
        if data:
            if type(data) is dict:
                # sort data to maintain predictability
                for attribute, value in sorted(data.items()):
                    setattr(self, attribute, value)
            elif type(data) is list:
                setattr(self, "details", data)
