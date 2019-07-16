import requests
import pytz
import os
import logging
import sys
import time

from datetime import datetime

try:
    # python 2
    import ConfigParser as configparser
except ImportError:
    # python 3
    import configparser

from .models.devices import Devices
from .models.incidents import Incidents
from .models.settings import Settings
from .models.canarytokens import CanaryTokens
from .models.result import Result
from .models.update import Updates

from .exceptions import ConfigurationError, ConsoleError, InvalidAuthTokenError, \
    ConnectionError, DeviceNotFoundError, IncidentNotFoundError, InvalidParameterError, \
    UpdateError, CanaryTokenError

ROOT = 'https://{0}.canary.tools/api/v1/'

RESULT_SUCCESS = 'success'
RESULT_ERROR = 'error'

logger = logging.getLogger('canarytools')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))


class Console(object):
    def __init__(self, domain=None, api_key=None, timezone=pytz.utc, debug=False, debug_level=logging.DEBUG):
        """Initialize Console object. All API calls are made with this object

        :param domain: The domain of the Canary console
        :param api_key: The API key received on your Canary console
        :param timezone: The timezone to be used when displaying objects with datetime information. ``pytz``
            timezones to be used
        :param debug: Debug flag for debugging requests/responses
        :param debug_level: Debug level. ``logging`` debug level used. ``logging.DEBUG`` will display all
            requests and responses as well as response data. ``logging.INFO`` will only log the requests and responses.
            The default is ``logging.DEBUG``

        :except ConfigurationError: Domain and/or API auth token not set

        Usage::

              >>> import canarytools
              >>> console = canarytools.Console(domain='console_domain', api_key='test_key')

              >>> import canarytools
              >>> import logging
              >>> console = canarytools.Console(debug=True)
        """
        if domain is None and api_key is None:
            if 'CANARY_API_DOMAIN' in os.environ and 'CANARY_API_TOKEN' in os.environ:
                domain = os.getenv('CANARY_API_DOMAIN')
                api_key = os.getenv('CANARY_API_TOKEN')
            else:
                # try load from disk
                domain, api_key = self.read_config()

        if domain is None or api_key is None:
            raise ConfigurationError("Domain and/or API auth token not set.")

        if debug:
            self.level = debug_level
        else:
            self.level = logging.NOTSET

        self.domain = domain
        self.api_key = api_key

        global ROOT
        ROOT = ROOT.format(self.domain)

        self.tz = timezone

        self.session = requests.session()
        self.session.params = {'auth_token': api_key}

        self.devices = Devices(self)
        self.incidents = Incidents(self)
        self.settings = Settings(self)
        self.tokens = CanaryTokens(self)
        self.updates = Updates(self)

    def ping(self):
        """Tests the connection to the Canary Console

            :return: Returns ``True`` if a connection could be established
                and ``False`` otherwise
            :rtype: bool

            Usage::

              >>> import canarytools
              >>> console = canarytools.Console()
              >>> console.ping()
              True
            """
        params = {}
        result = self.get('ping', params)

        if result.result == RESULT_SUCCESS:
            return True
        else:
            return False

    def post(self, url, params, parser=None, files={}):
        """Post request

        :param url: Url of the API endpoint
        :param params: List of parameters to be sent
        :param parser: The function used to parse JSON data into an specific object
        :param files: Files to be uploaded
        :return: Object(s) or a Result Indicator Object
        """
        try:
            self.log('[{datetime}] POST to {ROOT}{url}.json: {params}'.format(
                datetime=datetime.now(self.tz), ROOT=ROOT, url=url, params=params))
            start = time.time()
            r = self.session.post(url="{0}{1}".format(ROOT, url), data=params, files=files)
            complete = time.time() - start
            self.log(
                '[{datetime}] Received {response_code} in {:.2f}ms: '.format(
                    complete * 1000, datetime=datetime.now(self.tz), response_code=r.status_code), data=r.text)
        except requests.exceptions.ConnectionError:
            self.throw_connection_error()
        return self.handle_response(r.json(), parser)

    def get(self, url, params, parser=None):
        """Get request

        :param url: Url of the API endpoint
        :param params: List of parameters to be sent
        :param parser: The function used to parse JSON data into an specific object
        :return: Object(s) or a Result Indicator Object
        """
        try:
            self.log('[{datetime}] GET to {ROOT}{url}.json: {params}'.format(
                datetime=datetime.now(self.tz), ROOT=ROOT, url=url, params=params))
            start = time.time()
            resp = self.session.get(url="{0}{1}".format(ROOT, url), params=params)
            complete = time.time() - start
            self.log(
                '[{datetime}] Received {response_code} in {:.2f}ms: '.format(
                    complete * 1000, datetime=datetime.now(self.tz), response_code=resp.status_code), data=resp.text)
        except requests.exceptions.ConnectionError:
            self.throw_connection_error()
        return self.handle_response(resp.json(), parser)

    def delete(self, url, params, parser=None):
        """Delete request

        :param url: Url of the API endpoint
        :param params: List of parameters to be sent
        :param parser: The function used to parse JSON data into an specific object
        :return: Object(s) or a Result Indicator Object
        """
        try:
            self.log('[{datetime}] DELETE to {ROOT}{url}.json: {params}'.format(
                datetime=datetime.now(self.tz), ROOT=ROOT, url=url, params=params))
            start = time.time()
            r = self.session.delete(url="{0}{1}".format(ROOT, url), params=params)
            complete = time.time() - start
            self.log(
                '[{datetime}] Received {response_code} in {:.2f}ms: '.format(
                    complete * 1000, datetime=datetime.now(self.tz), response_code=r.status_code), data=r.text)
        except requests.exceptions.ConnectionError:
            self.throw_connection_error()
        return self.handle_response(r.json(), parser)

    def throw_connection_error(self):
        raise ConnectionError(
            "Failed to establish a new connection with console at domain: '{domain}'".format(
                domain=self.domain))

    def read_config(self):
        """Read config from disk

        :return: The api_key and the domain
        """
        paths = [os.path.expanduser('~/.canarytools.config'), os.path.expanduser('~/canarytools.config'),
                 '/etc/canarytools.config']
        config_parser = configparser.RawConfigParser()
        for path in paths:
            try:
                config_parser.read(path)
                api_key = config_parser.get('CanaryTools', 'api_key')
                domain = config_parser.get('CanaryTools', 'domain')

                if api_key and domain:
                    return domain, api_key
            except configparser.NoSectionError:
                pass
            except configparser.NoOptionError:
                pass
        return None, None

    def handle_response(self, response, parser):
        """Handle JSON response. Check for exceptions and objectify

        :param response: The response from the request made to the web API
        :param parser: The function used to parse JSON data into an specific object
        :return: Object(s) or a Result Indicator Object
        """
        if 'result' in response and response['result'] == RESULT_ERROR:
            self.handle_exception(response)
        else:
            if parser:
                return parser(response)
            else:
                return Result.parse(self, response)

    def handle_exception(self, response):
        """Handle unsuccessful results returned from the web API

        :param response: The response from the request made to the web API
        """
        if 'message' in response:
            message = response['message']
            if message in ERROR_MAP:
                raise ERROR_MAP[message]
            elif 'Update with tag ' in message:
                raise ERROR_MAP['Update with tag %s does not exist.'](message)
            raise ConsoleError(message)
        raise ConsoleError()

    def log(self, msg, data=None):
        """Log debug information based on level
        """
        if self.level == logging.INFO:
            log_msg = '{log_msg} Please set logging level to INFO, or greater, to see response data payload.'.format(
                log_msg=msg)
            logger.info(log_msg)
        elif self.level == logging.DEBUG:
            log_msg = '{log_msg} {data}'.format(log_msg=msg, data=data)
            logger.debug(log_msg)

    def __repr__(self):
        return '<Console %s>' % self.api_key

ERROR_MAP = {
    'Invalid auth_token': InvalidAuthTokenError,
    'Device not found': DeviceNotFoundError,
    'Incident not found': IncidentNotFoundError,
    'Settings does not permit updating this canary.':
        UpdateError("Settings does not permit updating this canary. "
                    "Check that automatic updates are not configured in the console."),
    'Update with tag %s does not exist.': UpdateError,
    'Parameter older_than was invalid.':
        InvalidParameterError("Parameter older_than was invalid"),
    'Cannot use src_host and node_id together':
        InvalidParameterError("Cannot use src_host and node_id together"),
    'Empty memo':
        InvalidParameterError("Please specify a memo when creating a Canarytoken "
                              "to remind yourself where you intend to use it :)"),
    'Supplied kind is not valid.':
        InvalidParameterError("Supplied kind is not valid when creating a Canarytoken"),
    'Could not process the parameters':
        InvalidParameterError("Error occurred while creating a Canarytoken. "
                              "Please ensure all required parameters are present and in the correct format."),
    'Could not process the parameters. cloned_web is invalid, not enough domain labels':
        InvalidParameterError("The parameter cloned_web is invalid, not enough domain labels"),
    'Could not save Canarydrop': CanaryTokenError('Could not save Canarydrop'),
    'Could not process the parameters': CanaryTokenError('Could not process the parameters'),
    'Could not find the Canarytoken': CanaryTokenError('Could not find the Canarytoken'),
    'Could not decode the memo': CanaryTokenError('Could not decode the memo'),
    'Could not delete Canarydrop': CanaryTokenError('Could not delete Canarydrop'),
    'File generation not supported.': CanaryTokenError('File generation not supported.'),
}
