from .base import CanaryToolsBase


class DataBundles(object):
    def __init__(self, console):
        """Initialize a DataBundles object

        :param console: The Console from which API calls are made
        """
        self.console = console

    def parse(self, data):
        """Parse JSON data

        :param data: JSON data
        :return: A list of DataBundle objects
        """
        bundles = list()
        if data and 'bundles' in data:
            for bundle in data['bundles']:
                bundles.append(DataBundle.parse(self.console, bundle))
        return bundles


class DataBundle(CanaryToolsBase):
    def __init__(self, console, data):
        """Initilaize a DataBundle object

        :param console: The Console from which API calls are made
        :param data: JSON data

        **Attributes:**
            - **settings_key (str)** -- Key that identifies this DataBundle
            - **req_len (str)** -- The length of the request
            - **bytes_copied (int)** -- Number of bytes sent in this DataBundle
            - **name (str)** -- The name or type of this DataBundle
            - **checksum (str)** -- Checksum of the DataBundle
            - **ended_time (int)** -- Time the DataBundle completed in epoch time
            - **tag (str)** -- The DataBundles tag
            - **type_ (str)** -- The type of the DataBundle
            - **bundle_size (int)** -- Size of theD DataBundle in bytes
            - **state (str)** -- The state the DataBundle is in
            - **node_id (str)** -- The id of the device for which this DataBundle is sent
            - **started_time (int)** -- Time the DataBundle started being sent, in epoch time
            - **created_time (int)** -- Time the DataBundle was created, in epoch time
            - **updated_time (int)** -- Time of the update in epoch time
        """
        super(DataBundle, self).__init__(console, data)

    def __str__(self):
        """Helper method"""
        return "[DataBundle] name: {name};".format(name=self.name)
