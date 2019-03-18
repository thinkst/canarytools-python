from dateutil.parser import parse

from .base import CanaryToolsBase
from ..exceptions import IncidentError


class Incidents(object):
    def __init__(self, console):
        """Initialize Incidents Object
        """
        self.console = console

    def all(self, node_id=None, event_limit=None):
        """Get all incidents for this console.

        :param node_id: Get all incidents for a specific node
        :param event_limit: Specify the maximum number of event logs to be returned with the incident.
        :return: List of Incident objects
        :rtype: List of :class:`Incident <Incident>` objects

        Usage::

            >>> import canarytools
            >>> incidents = console.incidents.all()
        """
        params = {'tz': self.console.tz, 'node_id': node_id, 'event_limit': event_limit}
        return self.console.get('incidents/all', params, self.parse)

    def unacknowledged(self, node_id=None, event_limit=None):
        """Get list of all unacknowledged incidents for a console.

        :param node_id: Get all unacknowledged incidents for a specific node
        :param event_limit: Specify the maximum number of event logs to be returned with the incident.
        :return: Return list of all unacknowledged Incidents
        :rtype: List of :class:`Incident <Incident>` objects

        Usage::

            >>> import canarytools
            >>> incidents = console.incidents.unacknowledged()
        """
        params = {'tz': self.console.tz, 'node_id': node_id, 'event_limit': event_limit}
        return self.console.get('incidents/unacknowledged', params, self.parse)

    def acknowledged(self, node_id=None, event_limit=None):
        """Get list of all acknowledged incidents for a console.

        :param node_id: Get all acknowledged incidents for a specific node
        :param event_limit: Specify the maximum number of event logs to be returned with the incident
        :return: Return list of all acknowledged incidents
        :rtype: List of :class:`Incident <Incident>` objects

        Usage::

            >>> import canarytools
            >>> incidents = console.incidents.acknowledged()
        """
        params = {'tz': self.console.tz, 'node_id': node_id, 'event_limit': event_limit}
        return self.console.get('incidents/acknowledged', params, self.parse)

    def acknowledge(self, node_id=None, src_host=None, older_than=None):
        """Mark all incidents as acknowledged. Use parameters to filter which
            incidents are acknowledged. Calling this method with no parameters
            specified will acknowledge all incidents.

        :param str node_id: Acknowledge incidents for a specific node
            NOTE: Cannot be used in conjunction with src_host
        :param str src_host: Acknowledge incidents from a specific source IP address
            NOTE: Cannot be used in conjunction with node_id
        :param str older_than: Acknowledge incidents older than the provided
            period. Periods are "[quantity][unit]", where "[unit]" is one of
            'h', 'd', 'w' (hours, days or weeks) e.g. '1h' or '1d' or '1w'
        :return: Result indicator of the API call
        :rtype: :class:`Result <Result>` object

        :except InvalidParameterError: older_than was invalid / src_host and node_id cannot
            be used together

        Usage::

            >>> import canarytools
            >>> result = console.incidents.acknowledge()

            >>> import canarytools
            >>> result = console.incidents.acknowledge(older_than='1d')
        """
        params = {'node_id': node_id, 'src_host': src_host, 'older_than': older_than}
        return self.console.post('incidents/acknowledge', params)

    def unacknowledge(self, node_id=None, src_host=None, older_than=None):
        """Mark all incidents as unacknowledged. Use parameters to filter which
            incidents are unacknowledged. Calling this method with no parameters
            specified will unacknowledge all incidents.

        :param str node_id: Unacknowledge incidents for a specific node
            NOTE: Cannot be used in conjunction with src_host
        :param str src_host: Unacknowledge incidents from a specific source IP address
            NOTE: Cannot be used in conjunction with node_id
        :param str older_than: Unacknowledge incidents older than the provided
            period. Periods are "[quantity][unit]", where "[unit]" is one of
            'h', 'd', 'w' (hours, days or weeks) e.g. '1h' or '1d' or '1w'
        :return: Result indicator of the API call
        :rtype: :class:`Result <Result>` object

        :except InvalidParameterError: older_than was invalid / src_host and node_id cannot
            be used together

        Usage::

            >>> import canarytools
            >>> result = console.incidents.unacknowledge()

            >>> import canarytools
            >>> result = console.incidents.unacknowledge(src_host='10.0.0.2')
        """
        params = {'node_id': node_id, 'src_host': src_host, 'older_than': older_than}
        return self.console.post('incidents/unacknowledge', params)

    def delete(self, node_id=None, src_host=None, older_than=None):
        """Delete all acknowledged incidents. Use parameters to filter which
            incidents are deleted. Calling this method with no parameters
            specified will delete all acknowledged incidents.

        :param str node_id: Delete acknowledged incidents for a specific node
            NOTE: Cannot be used in conjunction with src_host
        :param str src_host: Delete acknowledged incidents from a specific source IP address
            NOTE: Cannot be used in conjunction with node_id
        :param str older_than: Delete acknowledged incidents older than the provided
            period. Periods are "[quantity][unit]", where "[unit]" is one of
            'h', 'd', 'w' (hours, days or weeks) e.g. '1h' or '1d' or '1w'
        :return: Result indicator of the API call
        :rtype: :class:`Result <Result>` object

        :except InvalidParameterError: older_than was invalid / src_host and node_id cannot
            be used together

        Usage::

            >>> import canarytools
            >>> result = console.incidents.delete()

            >>> import canarytools
            >>> result = console.incidents.delete(node_id='00000000042c23a')
        """
        params = {'node_id': node_id, 'src_host': src_host, 'older_than': older_than}
        return self.console.post('incidents/delete', params)

    def get_incident(self, incident_id):
        """Get an Incident.

        :param incident: The id of the Incident
        :return: An Incident object
        :rtype: :class:`Incident <Incident>` object

        :except IncidentNotFoundError: Could not find incident with this id

        Usage::

            >>> import canarytools
            >>> incident = console.incidents.get_incident(incident_id='incident:ftplogin:0e4b47')
        """
        params = {'tz': self.console.tz, 'incident': incident_id}
        return self.console.get('incident/fetch', params, self.parse)

    def parse(self, data):
        """Parse JSON data

        :param data: JSON data
        :return: A list of Incident objects or a single Incident object
        """
        incidents = list()
        if data and 'incidents' in data:
            # loop over each incident in the JSON response
            for incident in data['incidents']:
                if incident['summary'] in INCIDENT_MAP:
                    incidents.append(INCIDENT_MAP[incident['summary']].parse(
                        self.console, incident))
                else:
                    incidents.append(INCIDENT_MAP['Default'].parse(
                        self.console, incident))
        elif data and 'incident' in data:
            data = data['incident']
            if data['description'] in INCIDENT_MAP:
                return INCIDENT_MAP[data['description']].parse(
                    self.console, data)
            else:
                return INCIDENT_MAP['Default'].parse(self.console, data)

        return incidents


class Incident(CanaryToolsBase):
    def __init__(self, console, data):
        """Initialize Incident Object

        **Attributes:**
            - **id (str)** -- The identification code of the incident
            - **description (str)** -- The event description of the incident
            - **acknowledged (bool)** -- Has the incident been acknowledged?
            - **events (list)** -- List of events
            - **logtype (str)** -- Log type
            - **summary (str)** -- The event description of the incident

        **Subclasses:**
            List of classes which extend this base class.

            ``IncidentDeviceReconnected``, ``IncidentDeviceDied``, ``IncidentFTPLogin``, ``IncidentHTTPLogin``,
            ``IncidentHTTPLoad``, ``IncidentSSHLogin``, ``IncidentTelnetLogin``, ``IncidentHTTPProxyRequest``,
            ``IncidentMySQLLogin``, ``IncidentMSSQLLogin``, ``IncidentTFTPRequest``, ``IncidentNmapOSScan``,
            ``IncidentNmapNULLScan``, ``IncidentNmapXMASScan``, ``IncidentNTPMonlist``, ``IncidentVNCLogin``,
            ``IncidentGitCloneRequest``, ``IncidentTCPBannerRequest``, ``IncidentModbusRequest``, ``IncidentRedisCommand``,
            ``IncidentUser``, ``IncidentSNMPRequest``, ``IncidentSIPRequest``, ``IncidentSMBFileOpen``, ``IncidentCanarytokenTriggered``,
            ``IncidentHostPortScan``, ``IncidentNetworkPortScan``, ``IncidentConsolidatedNetworkPortScan``

        """
        super(Incident, self).__init__(console, data)

    def __setattr__(self, key, value):
        """Override function on base class. This will be used to do any
            extra processing to the JSON data. e.g. Parsing Event data
            to Event objects.
        """
        # Set only specified fields as attributes
        if key not in ['console', 'id', 'description', 'summary', 'logtype', 'events', \
                       'acknowledged', 'dst_host', 'src_host', 'node_id', 'dst_port', \
                       'src_port']:
            return

        # if the key is events parse list of events parse events
        if 'events' == key:
            events = list()
            for event in value:
                events.append(Event.parse(self.console, event))
            value = events

        # flatten description key
        if 'description' == key and isinstance(value, dict):
            for attribute, val in value.items():
                self.__setattr__(attribute, val)
            # return as we don't want to call __setattr__ again
            return

        # update string bool values
        if key in ['acknowledged']:
            value = value == 'True'

        super(Incident, self).__setattr__(key, value)

    def __str__(self):
        """Helper method
        """
        return "[{type}] acknowledged: {acked};".format(
            type=self.__class__.__name__, acked=self.acknowledged)

    def unacknowledge(self):
        """Mark incident as unacknowledged

        :return: Result indicator of the API call
        :rtype: :class:`Result <Result>` object

        Usage::

            >>> import canarytools
            >>> incident = console.incidents.get_incident(incident_id='incident:ftplogin:0e4b47')
            >>> result = incident.unacknowledge()
        """
        params = {'incident': self.id}
        r = self.console.post('incident/unacknowledge', params)

        self.refresh()

        return r

    def acknowledge(self):
        """Mark incident as acknowledged

        :return: Result indicator of the API call
        :rtype: :class:`Result <Result>` objects

        Usage::

            >>> import canarytools
            >>> incident = console.incidents.get_incident(incident_id='incident:ftplogin:0e4b47')
            >>> result = incident.acknowledge()
        """
        params = {'incident': self.id}
        r = self.console.post('incident/acknowledge', params)

        self.refresh()

        return r

    def delete(self):
        """Delete incident

        :return: Result indicator of the API call
        :rtype: :class:`Result <Result>` object

        Usage::

            >>> import canarytools
            >>> incident = console.incidents.get_incident(incident_id='incident:ftplogin:0e4b47')
            >>> result = incident.delete()
        """
        params = {'incident': self.id}

        # Incident must be acknowledged in order to delete
        if self.acknowledged == False:
            raise IncidentError('Cannot delete an unacknowledged Incident')

        return self.console.delete('incident/delete', params)

    def refresh(self):
        """Refresh object after API calls to keep up-to-date

        Usage::

            >>> import canarytools
            >>> incident = console.incidents.get_incident(incident_id='incident:ftplogin:0e4b47')
            >>> incident.refresh()
        """
        incidents = Incidents(self.console)
        new_incident = incidents.get_incident(incident_id=self.id)

        self.__dict__.update(new_incident.__dict__)


class Event(CanaryToolsBase):
    def __init__(self, console, data):
        """An event contains all the details relating to a incident occurence.

        :param console: The Console from which API calls are made
        :param data: JSON data

        For a more detailed list of event attributes see :ref:`incidents-events-ref`
        """
        super(Event, self).__init__(console, data)

    def __setattr__(self, key, value):
        """ Override base class function
        """
        # key's are integers, probably a consolidated port scan
        if self.is_int(key):
            if not hasattr(self, 'ports_scanned'):
                ports_scanned = {key: value}
                self.ports_scanned = ports_scanned
                return
            else:
                self.ports_scanned[key] = value
                return

        if key in ['timestamp']:
            return

        if 'timestamp_std' == key:
            key = key[:-4]
            if value:
                value = parse(value)
            else:
                value = None

        super(Event, self).__setattr__(key.lower(), value)

    def __str__(self):
        """Helper method
        """
        time = None
        event_info = ""
        for key, value in vars(self).items():
            # exclude these from the string
            if 'console' == key:
                continue
            if 'timestamp' == key:
                time = value
            else:
                event_info += " {key}: {value}".format(
                    key=str(key), value=self.trim(value))

        return "[Event] timestamp: {time} {event_info}".format(
            time=time, event_info=event_info)

    def is_int(self, value):
        """Helper method

        :param value:
        :return:
        """
        try:
            int(value)
            return True
        except ValueError:
            return False

    def trim(self, value):
        """Trim value if too large

        :return: Shortened version of value
        """
        if len(value) > 25:
            return value[:25] + "... {trimmed}"
        return value


class IncidentDeviceReconnected(Incident):
    """Canary Reconnected"""


class IncidentDeviceDied(Incident):
    """Canary Disconnected"""


class IncidentFTPLogin(Incident):
    """FTP Login Attempt"""


class IncidentHTTPLogin(Incident):
    """HTTP Login Attempt"""

class IncidentHTTPLoad(Incident):
    """HTTP Page Load"""


class IncidentSSHLogin(Incident):
    """SSH Login Attempt"""


class IncidentTelnetLogin(Incident):
    """Telnet Login Attempt"""


class IncidentHTTPProxyRequest(Incident):
    """HTTP Proxy Request"""


class IncidentMySQLLogin(Incident):
    """MySQL Login Attempt"""


class IncidentMSSQLLogin(Incident):
    """MSSQL Login Attempt"""


class IncidentTFTPRequest(Incident):
    """TFTP Request"""


class IncidentNmapOSScan(Incident):
    """NMAP OS Scan Detected"""


class IncidentNmapNULLScan(Incident):
    """NMAP NULL Scan Detected"""


class IncidentNmapXMASScan(Incident):
    """NMAP XMAS Scan Detected"""


class IncidentNTPMonlist(Incident):
    """NTP Monlist Request"""


class IncidentVNCLogin(Incident):
    """VNC Login Attempt"""


class IncidentGitCloneRequest(Incident):
    """Git Repository Clone Attempt"""


class IncidentTCPBannerRequest(Incident):
    """Custom TCP Service Request"""


class IncidentModbusRequest(Incident):
    """ModBus Request"""


class IncidentRedisCommand(Incident):
    """Redis Command"""


class IncidentUser(Incident):
    """User Module Incident"""


class IncidentSNMPRequest(Incident):
    """SNMP Request"""


class IncidentSIPRequest(Incident):
    """SIP Request"""


class IncidentSMBFileOpen(Incident):
    """Shared File Opened"""


class IncidentCanarytokenTriggered(Incident):
    """Canarytoken triggered"""


class IncidentHostPortScan(Incident):
    """Host Port Scan"""


class IncidentNetworkPortScan(Incident):
    """Network Port Scan"""


class IncidentConsolidatedNetworkPortScan(Incident):
    """Consolidated Network Port Scan"""

class IncidentConsoleSettingsChange(Incident):
    """Console Settings Changed"""

class IncidentDeviceSettingsChange(Incident):
    """Device Settings Changed"""

class IncidentFlockSettingsChange(Incident):
    """Flock Settings Changed"""

class IncidentSettingsRollback(Incident):
    """Device Setting Rollback Detected"""

class IncidentNmapFINScan(Incident):
    """NMAP FIN Scan Detected"""


INCIDENT_MAP = {
    'Default':                          Incident,
    'Canary Reconnected':               IncidentDeviceReconnected,
    'Canary Disconnected':              IncidentDeviceDied,
    'FTP Login Attempt':                IncidentFTPLogin,
    'HTTP Login Attempt':               IncidentHTTPLogin,
    'HTTP Page Load':                   IncidentHTTPLoad,
    'SSH Login Attempt':                IncidentSSHLogin,
    'Telnet Login Attempt':             IncidentTelnetLogin,
    'HTTP Proxy Request':               IncidentHTTPProxyRequest,
    'MySQL Login Attempt':              IncidentMySQLLogin,
    'MSSQL Login Attempt':              IncidentMSSQLLogin,
    'TFTP Request':                     IncidentTFTPRequest,
    'NMAP OS Scan Detected':            IncidentNmapOSScan,
    'NMAP NULL Scan Detected':          IncidentNmapNULLScan,
    'NMAP XMAS Scan Detected':          IncidentNmapXMASScan,
    'NTP Monlist Request':              IncidentNTPMonlist,
    'VNC Login Attempt':                IncidentVNCLogin,
    'Git Repository Clone Attempt':     IncidentGitCloneRequest,
    'Custom TCP Service Request':       IncidentTCPBannerRequest,
    'ModBus Request':                   IncidentModbusRequest,
    'Redis Command':                    IncidentRedisCommand,
    'User Module %d Incident':          IncidentUser,
    'SNMP Request':                     IncidentSNMPRequest,
    'SIP Request':                      IncidentSIPRequest,
    'Shared File Opened':               IncidentSMBFileOpen,
    'Canarytoken triggered':            IncidentCanarytokenTriggered,
    'Host Port Scan':                   IncidentHostPortScan,
    'Network Port Scan':                IncidentNetworkPortScan,
    'Consolidated Network Port Scan':   IncidentConsolidatedNetworkPortScan,
    'Console Settings Changed':         IncidentConsoleSettingsChange,
    'Device Settings Changed':          IncidentDeviceSettingsChange,
    'Flock Settings Changed':           IncidentFlockSettingsChange,
    'Device Setting Rollback Detected': IncidentSettingsRollback,
    'NMAP FIN Scan Detected':           IncidentNmapFINScan
}