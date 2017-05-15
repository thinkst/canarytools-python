from .base import CanaryToolsBase
from .databundles import DataBundles

from dateutil.parser import parse


class Devices(object):
    def __init__(self, console):
        """Initialize the device

        :param console: The Console from which API calls are made
        """
        self.console = console

    def all(self):
        """Get all registered devices

        :return: List of all devices
        :rtype: List of :class:`Device <Device>` objects

        Usage::

              >>> import canarytools
              >>> devices = console.devices.all()
        """
        params = {'tz': self.console.tz}
        return self.console.get('devices/all', params, self.parse)

    def live(self):
        """Get all registered connected devices

        :return: List of live devices
        :rtype: List of :class:`Device <Device>` objects

        Usage::

              >>> import canarytools
              >>> devices = console.devices.live()
        """
        params = {'tz': self.console.tz}
        return self.console.get('devices/live', params, self.parse)

    def dead(self):
        """Get all registered disconnected devices

        :return: List of dead devices
        :rtype: List of :class:`Device <Device>` objects

        Usage::

              >>> import canarytools
              >>> devices = console.devices.dead()
        """
        params = {'tz': self.console.tz}
        return self.console.get('devices/dead', params, self.parse)

    def get_device(self, node_id):
        """Get information on a particular device

        :param node_id: Get device with specific node id
        :return: Device with all information
        :rtype: A :class:`Device <Device>` object

        :except DeviceNotFoundError: The device could not be found

        Usage::

            >>> import canarytools
            >>> device = console.devices.get_device(node_id='0000000000231c23')
        """
        params = {'node_id': node_id}
        return self.console.get('device/getinfo', params, self.parse)

    def parse(self, data):
        """Parse JSON data

        :param data: JSON data
        :return: Device object or a list if Device objects
        """
        if data and 'devices' in data:
            devices = list()
            for device in data['devices']:
                devices.append(self.get_device(device['id']))
            return devices
        elif data and 'device' in data:
            return Device.parse(self.console, data['device'])
        return list()


class Device(CanaryToolsBase):
    def __init__(self, console, data):
        """:class:`Device <Device>` Initialize a Device object

        :param console: The Console from which API calls are made
        :param data: JSON data

        **Attributes:**
                - **id (str)** -- The device identification code
                - **name (str)** -- The name of the device
                - **description (str)** -- Device description
                - **uptime_age (datetime)** -- The amount of time the device has been online for
                - **first_seen (datetime)** -- The first time the device came online
                - **last_heartbeat_age (str)** -- Time since device last communicated with the console
                - **uptime (long)** -- The amount of time (in seconds) the device has been online
                - **need_reboot (bool)** -- Has the device been scheduled for a reboot?
                - **reconnect_count (int)** -- Number of times the device has reconnected to the console
                - **live (bool)** -- Is the device online?
                - **mac_address (str)** -- The MAC address of the device
                - **ignore_notifications_disconnect (bool)** -- Should the console ignore disconnects?
                - **notify_after_horizon_reconnect (bool)** -- Notify console after horizon reconnects
                - **sensor (str)** -- The sensor of the device
                - **first_seen_age (str)** -- Time since the device was first seen i.e '2 days'
                - **ignore_notifications_general (bool)** -- Ignore all notifications
                - **device_id_hash (str)** -- Hash of the devices ID
                - **service_count (int)** -- Number of services running on the device
                - **ip_address (str)** -- The IP address of the device
                - **ippers (str)** -- Personality(s) of the device
                - **ghost (bool)** -- Is this a ghost device? i.e the device has been registered but hasn't come online
                - **unacknowleged_incidents (list)** -- List of unacknowledged incidents for the device
                - **last_seen (datetime)** -- Time the device was last seen
        """
        super(Device, self).__init__(console, data)

    def __setattr__(self, key, value):
        """Override base class implementation."""
        # json attributes to ignore
        if key in ['first_seen', 'first_seen_printable',
                   'last_heartbeat', 'last_heartbeat_printable', 'mac']:
            return

        # rename keys
        if 'device_live' == key:
            key = 'live'
        elif 'device_id' == key:
            key = 'id'

        # update string bool values
        if key in ['ghost', 'ignore_notifications_disconnect',
                            'ignore_notifications_general', 'need_reboot',
                            'notify_after_horizon_reconnect', 'device_live']:
            value = value == 'True'

        # get unack'd incidents for this device and look them up
        if 'unacknowleged_incidents' == key:
            unacknowleged_incidents = list()

            if hasattr(self, 'id'):
                node_id = self.id
            else:
                node_id = None

            all_unacked_incidents = self.console.incidents.unacknowledged(node_id=node_id)

            for device_incident in value:
                for incident in all_unacked_incidents:
                    if device_incident['key'] == incident.id:
                        unacknowleged_incidents.append(incident)
                        break
            value = unacknowleged_incidents

        # remove 'std' from key name and create datetime object from date string
        if key in ['first_seen_std', 'last_seen_std']:
            key = key[:-4]
            if value:
                value = parse(value)
            else:
                value = None

        if key in ['uptime']:
            try:
                value = long(value)
            except NameError:
                value = int(value)

        if key in ['reconnect_count', 'service_count']:
            value = int(value)

        super(Device, self).__setattr__(key, value)

    def __str__(self):
        """Helper method"""
        # ghost devices won't have an ip, so check
        if hasattr(self, 'ip_address'):
            ip_address = self.ip_address
        else:
            ip_address = ""

        return "[Device] name: {name}; ip: {ip}; location: {location}; live: {live}".format(
                name=self.name, ip=ip_address,
                location=self.description, live=self.live)

    def reboot(self):
        """Reboot the device

        :return: Result object
        :rtype: :class:`Result <Result>` object

        :except DeviceNotFoundError: The device could not be found

        Usage::

            >>> import canarytools
            >>> device = console.devices.get_device(node_id='0000000000231c23')
            >>> result = device.reboot()
        """
        params = {'node_id': self.node_id}
        r = self.console.post('device/reboot', params)

        self.refresh()

        return r

    def update(self, update_tag):
        """Update the device

        :param update_tag: The tag of the update
        :return: Result object
        :rtype: :class:`Result <Result>` object

        :except UpdateError: Device update not permitted. Automatic updates are not configured. Or the update tag does
            not exist.
        :except DeviceNotFoundError: The device could not be found

        Usage::

            >>> import canarytools
            >>> device = console.devices.get_device(node_id='0000000000231c23')
            >>> result = device.update(update_tag='4ae023bdf75f14c8f08548bf5130e861')
        """
        params = {'node_id': self.node_id, 'update_tag': update_tag}
        r = self.console.post('device/update', params)

        self.refresh()

        return r

    def list_databundles(self):
        """Lists all DataBundles

        :return: List of DataBundle objects
        :rtype: List of :class:`DataBundle <DataBundle>`

        Usage::

            >>> import canarytools
            >>> device = console.devices.get_device(node_id='0000000000231c23')
            >>> databundles = device.list_databundles()
        """
        data_bundles = DataBundles(self.console)
        params = {'node_id': self.node_id}
        return self.console.get('bundles/list', params, data_bundles.parse)

    def refresh(self):
        """Refresh a Device object by pulling all changes

        :except DeviceNotFoundError: The device could not be found

        Usage::

            >>> import canarytools
            >>> device = console.devices.get_device(node_id='0000000000231c23')
            >>> device.refresh()
        """
        devices = Devices(self.console)
        device = devices.get_device(self.node_id)

        self.__dict__.update(device.__dict__)
