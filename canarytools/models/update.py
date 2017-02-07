from .base import CanaryToolsBase


class Updates(object):
    def __init__(self, console):
        """Initialize Update object

        :param console: The Console from which API calls are made
        """
        self.console = console

    def list_updates(self):
        """List of available updates

        :return: List of Update objects
        :rtype: List of :class:`Update <Update>` objects

        Usage::

            >>> import canarytools
            >>> updates = canarytools.updates.list_updates()
        """
        params = {}
        return self.console.get('updates/list', params, self.parse)

    def update_device(self, node_id, update_tag):
        """Update the device

        :param node_id: The node_id of the device to be updated
        :param update_tag: The tag of the update to be updated to
        :return: A Result object
        :rtype: :class:`Result <Result>` object

        :except UpdateError: Device update not permitted. Automatic updates are not configured. Or the update tag does
         not exist.

        Usage::

            >>> import canarytools
            >>> result = canarytools.updates.update_device(node_id='00000000ff798b93', update_tag='4ae023bdf75f14c8f08548bf5130e861')
        """
        params = {'node_id': node_id, 'update_tag': update_tag}
        return self.console.post('device/update', params)

    def parse(self, data):
        """Parse JSON data

        :param data: JSON data
        :return: A list of Update objects
        """
        updates = list()
        if 'updates' in data:
            for update in data['updates']:
                updates.append(Update.parse(self.console, update))
        return updates


class Update(CanaryToolsBase):
    def __init__(self, console, data):
        """Initialize an Update object

        :param console: The Console from which API calls are made
        :param data: JSON data

        **Attributes:**
            - **supported_versions (list)** --List of Canary versions that support this update
            - **description (str)** -- Description of the update
            - **filename (str)** -- Name of update file
            - **ignore (bool)** -- Should this update be ignored?
            - **tag (str)** -- Update tag. Used to uniquely identify an update.
            - **version (str)** -- Version to which the Canary is updated.
        """
        super(Update, self).__init__(console, data)

    def __setattr__(self, key, value):
        """Helper method
        """
        if 'ignore' == key:
            value = value == 'True'

        super(Update, self).__setattr__(key, value)

    def __str__(self):
        """Helper method"""
        return "[Update] description: {description} version: {version}".format(
            description=self.description, version=self.version)
