class Settings(object):
    def __init__(self, console):
        """Initialize Settings object

        :param console: The Console from which API calls are made
        """
        self.console = console

    def is_ip_whitelisted(self, src_ip):
        """Is IP address Whitelisted

        :param src_ip: The IP address to be checked
        :return: Result object
        :rtype: :class:`Result <Result>` object

        Usage::

            >>> import canarytools
            >>> devices = canarytools.settings.is_ip_whitelisted(src_ip='10.0.0.2')
        """
        params = {'src_ip': src_ip}
        result = self.console.get('settings/is_ip_whitelisted', params)

        if result.is_ip_whitelisted:
            return True
        else:
            return False

    def whitelist_ip_port(self, src_ip, dst_port=None):
        """Whitelist IP address and port

        :param src_ip: The IP to be whitelisted
        :param dst_port: The destination port
        :return: Result object
        :rtype: :class:`Result <Result>` object

        Usage::

            >>> import canarytools
            >>> devices = canarytools.settings.whitelist_ip_port(src_ip='10.0.0.2', dst_port='5000')
        """
        params = {'src_ip': src_ip, 'dst_port': dst_port}
        return self.console.post('settings/whitelist_ip_port', params)
