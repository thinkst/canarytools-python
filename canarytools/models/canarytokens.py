import os

from .base import CanaryToolsBase
from ..exceptions import InvalidParameterError


class CanaryTokens(object):
    def __init__(self, console):
        """Initialize CanaryToken

        :param console: The Console object from which API calls are made
        """
        self.console = console

    def create(
        self, 
        memo, 
        kind, 
        web_image=None, 
        mimetype=None, 
        cloned_web=None, 
        browser_redirect_url=None,
        s3_source_bucket=None,
        s3_log_bucket=None,
        process_name=None,
        ):
        """Create a new Canarytoken

        :param memo: Use this to remind yourself where you placed the Canarytoken
        :param kind: The type of Canarytoken. Supported classes currently are: 
            aws-id, cloned-web, dns, doc-msword, http, 
            doc-msexcel, msexcel-macro, doc-msword, msword-macro, 
            pdf-acrobat-reader, qr-code, sensitive-cmd, signed-exe, 
            slack-api, web-image, windows-dir, wireguard
        :param web_image: The path to an image file for use with web-image tokens.
        :param mimetype: The type of image specified in web_image. e.g. 'image/png'
        :param cloned_web: Domain to be used in cloned-web tokens
        :param browser_redirect_url: URL to redirect attackers to after triggering token (required when creating fast-redirect and slow-redirect tokens)
        :param s3_source_bucket: S3 bucket to monitor for access (required when creating aws-s3 tokens)
        :param s3_log_bucket: S3 bucket where logs will be stored (required when creating aws-s3 tokens)
        :param process_name: Name of the process you want to monitor (required when creating sensitive-cmd tokens)
        :return: A Result object
        :rtype: :class:`Result <Result>` object

        :except InvalidParameterError: One of the parameters was invalid
        :except CanaryTokenError: Something went wrong while creating the CanaryToken

        Usage::

            >>> import canarytools
            >>> result = console.tokens.create(memo='Desktop Token', kind=canarytools.CanaryTokenKinds.DOC_MSWORD)
        """
        params = {'memo': memo, 'kind': kind}
        if cloned_web:
            params['cloned_web'] = cloned_web

        if browser_redirect_url:
            params['browser_redirect_url'] = browser_redirect_url

        if s3_source_bucket:
            params['s3_source_bucket'] = s3_source_bucket

        if s3_log_bucket:
            params['s3_log_bucket'] = s3_log_bucket

        if process_name:
            params['process_name'] = process_name

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
    
    def download(self, filename=None):
        """Download a Canarytoken

        :param filename: Optional target filename. The console should provide a default value.
        :return: The filename written to.
        :rtype: :class:`str`

        :except CanaryTokenError: Something went wrong while downloading the CanaryToken.
        :except ValueError: This token doesn't have a default filename, you need to provide one.

        Usage::

            >>> import canarytools
            >>> token = console.tokens.create(memo="Excel file on Jim's Laptop", kind="doc-msexcel")
            >>> token.download(filename="Payroll.xslx")
            OR
            >>> filename = token.download()
        """
        resp = self.console.get('canarytoken/download', {'canarytoken': self.canarytoken}, raw_resp=True)
        disp = resp.headers['Content-Disposition'].split('filename=')
        if not filename:
            if len(disp) == 2 and disp[0] == 'attachment; ':
                filename = disp[-1]
            else:
                raise ValueError('CanaryToken.download() requires filename for this token')
        with open(filename, 'wb') as fd:
            fd.write(resp.content)
        return filename


class CanaryTokenKinds(object):
    AWS = 'aws-id'
    AWSS3 = 'aws-s3'
    CLONED_WEB = 'cloned-web'
    DNS = 'dns'
    DOC_MSWORD = 'doc-msword'
    FASTREDIRECT = 'fast-redirect'
    HTTP = 'http'
    MSEXCEL = 'doc-msexcel'
    MSEXCELMACRO = 'msexcel-macro'
    MSWORD = 'doc-msword'
    MSWORDMACRO = 'msword-macro'
    PDF = 'pdf-acrobat-reader'
    QRCODE = 'qr-code'
    SIGNEDEXE = 'signed-exe'
    SLACK = 'slack-api'
    SLOWREDIRECT = 'slow-redirect'
    WEB_IMAGE = 'web-image'
    WINDOWS_DIR = 'windows-dir'
    WIREGUARD = 'wireguard'