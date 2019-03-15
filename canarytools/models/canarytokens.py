import os

from .base import CanaryToolsBase
from ..exceptions import InvalidParameterError


class CanaryTokens(object):
    def __init__(self, console):
        """Initialize CanaryToken

        :param console: The Console object from which API calls are made
        """
        self.console = console

    def create(self, memo, kind, web_image=None, cloned_web=None, mimetype=None):
        """Create a new Canarytoken

        :param memo: Use this to remind yourself where you placed the Canarytoken
        :param kind: The type of Canarytoken. Supported classes currently are: http, dns,
            cloned-web, doc-msword
        :param web_image: The path to an image file for use with web-image tokens.
        :param cloned_web: Domain to be used in clonded-web tokens
        :param mimetype: The type of image specified in web_image. e.g. 'image/png'
        :return: A Result object
        :rtype: :class:`Result <Result>` object

        :except InvalidParameterError: One of the parameters was invalid
        :except CanaryTokenError: Something went wrong while creating the CanaryToken

        Usage::

            >>> import canarytools
            >>> result = console.tokens.create(memo='Desktop Token', kind=canarytools.CanaryTokenKinds.DOC_MSWORD)
        """
        params = {'memo': memo, 'kind': kind, 'cloned_web': cloned_web}

        # load image and send
        if web_image:
            with open(web_image, 'rb') as f:
                if not mimetype:
                    raise InvalidParameterError("Mimetype cannot be null")

                files = {'web_image': (os.path.basename(web_image), f, mimetype)}
                return self.console.post('canarytoken/create', params, self.parse, files)

        return self.console.post('canarytoken/create', params, self.parse)

    def get_token(self, canarytoken):
        """Gets a single Canarytoken

        :param canarytoken: The key specifying a unique Canarytoken
        :return: A Canarytoken object
        :rtype: :class:`CanaryToken <CanaryToken>` object

        :except CanaryTokenError: Could not find the CanaryToken

        Usage::

            >>> import canarytools
            >>> token = console.tokens.get_token(canarytoken='gv3xjl75b3nr7vwsmvxexcle0')
        """
        params = {'canarytoken': canarytoken}
        return self.console.get('canarytoken/fetch', params, self.parse)

    def all(self, include_endpoints=True):
        """Fetch all Canarytokens

        :return: A list of Canarytoken objects
        :rtype: List of :class:`CanaryToken <CanaryToken>` objects

        :except CanaryTokenError: Something went wrong while getting the CanaryTokens

        Usage::

            >>> import canarytools
            >>> tokens = console.tokens.all()
        """
        params = {'include_endpoints':str(include_endpoints)}
        return self.console.get('canarytokens/fetch', params, self.parse)

    def parse(self, data):
        """Parse JSON data

        :param data: JSON data returned from the web API
        :return: An initliazed list of Canarytokens or a single Canarytoken
        """
        tokens = list()
        if data and 'tokens' in data:
            for token in data['tokens']:
                tokens.append(CanaryToken.parse(self.console, token))
        elif data and 'token' in data:
            return CanaryToken.parse(self.console, data['token'])
        elif data and 'canarytoken' in data:
            return CanaryToken.parse(self.console, data['canarytoken'])
        return tokens


class CanaryToken(CanaryToolsBase):
    def __init__(self, console, data):
        """Initialize a CanaryToken object

        :param console: The Console from which the API calls are made
        :param data: JSON data containing CanaryToken attributes
        """
        super(CanaryToken, self).__init__(console, data)

    def __setattr__(self, key, value):
        """Override base class method

        :param key: Key of attribute
        :param value: Value of attribute
        """
        super(CanaryToken, self).__setattr__(key, value)

    def __str__(self):
        """Helper method"""
        return "[Canarytoken] kind: {kind}; memo: {memo}; enabled: {enabled};" \
               " triggered count: {count}".format(
                    kind=self.kind, memo=self.memo,
                    enabled=self.enabled, count=self.triggered_count)

    def update(self, memo):
        """Update a Canarytoken memo

        :param memo: The new memo to be used
        :return: A Result object
        :rtype: :class:`Result <Result>` object

        :except CanaryTokenError: Something went wrong while updating the CanaryToken
        :except InvalidParameterError: The memo parameter is invalid

        Usage::

            >>> import canarytools
            >>> token = console.tokens.get_token(canarytoken='gv3xjl75b3nr7vwsmvxexcle0')
            >>> result = token.update(memo='Token in downloads folder')
        """
        params = {'memo': memo, 'canarytoken': self.canarytoken}
        return self.console.post('canarytoken/update', params)

    def delete(self):
        """Delete a Canarytoken

        :param canarytoken: The key of the Canarytoken to be deleted
        :return: A Result object
        :rtype: :class:`Result <Result>` object

        :except CanaryTokenError: Something went wrong while deleting the CanaryToken

        Usage::

            >>> import canarytools
            >>> token = console.tokens.get_token(canarytoken='gv3xjl75b3nr7vwsmvxexcle0')
            >>> result = token.delete()
        """
        params = {'canarytoken': self.canarytoken}
        return self.console.post('canarytoken/delete', params)

    def disable(self):
        """Disable a Canarytoken

        :param canarytoken: The key of the Canarytoken
        :return: A Result object
        :rtype: :class:`Result <Result>` object

        :except CanaryTokenError: Something went wrong while disabling the CanaryToken

        Usage::

            >>> import canarytools
            >>> token = console.tokens.get_token(canarytoken='gv3xjl75b3nr7vwsmvxexcle0')
            >>> result = token.disable()
        """
        params = {'canarytoken': self.canarytoken}
        return self.console.post('canarytoken/disable', params)

    def enable(self):
        """Enable a Canarytoken

        :param canarytoken: The key of the Canarytoken
        :return: A Result object
        :rtype: :class:`Result <Result>` object

        :except CanaryTokenError: Something went wrong while enabling the CanaryToken

        Usage::

            >>> import canarytools
            >>> token = console.tokens.get_token(canarytoken='gv3xjl75b3nr7vwsmvxexcle0')
            >>> result = token.enable()
        """
        params = {'canarytoken': self.canarytoken}
        return self.console.post('canarytoken/enable', params)


class CanaryTokenKinds(object):
    HTTP = 'http'
    DNS = 'dns'
    CLONED_WEB = 'cloned-web'
    DOC_MSWORD = 'doc-msword'
    WEB_IMAGE = 'web-image'
    WINDOWS_DIR = 'windows-dir'
    AWS = 'aws-id'
    AWSS3 = 'aws-s3'
    MSWORD = 'doc-msword'
    SIGNEDEXE = 'signed-exe'
    QRCODE = 'qr-code'
    SVN = 'svn'
    SQL = 'sql'
    PDF = 'pdf-acrobat-reader'
    FASTREDIRECT = 'fast-redirect'
    SLOWREDIRECT = 'slow-redirect'
    MSWORDMACRO = 'msword-macro'
    MSEXCELMACRO = 'msexcel-macro'
