import os

from .base import CanaryToolsBase
from ..exceptions import InvalidParameterError

import logging
logger = logging.getLogger('canarytools')

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
        **kwargs,
    ):
        """Create a new Canarytoken

        :param memo: Use this to remind yourself where you placed the Canarytoken
        :param flock_id: Create token in different flock. Defaults to: 'flock:default'
        :param kind: The type of Canarytoken. See canarytokens.CanaryTokenKinds for supported values
        :param attempt_unrecognized: Make request even if one or more given parameters aren't recognized by this module
        :param web_image: The path to an image file for use with web-image tokens.
        :param mimetype: The type of image specified in web_image. e.g. 'image/png'
        :param cloned_web: Domain to be used in cloned-web tokens
        :param custom_domain: Specifies the custom Canarytoken domain to use (that's already been linked to the Console) when creating a Canarytoken
        :param expiry: (Only AWS API Key token) Specifies the expiry when creating a Canarytoken. String format using y, mo, w, d, h are supported. E.g. 12h, 6mo
        :param flock_id: A valid flock_id (defaults to the Default Flock or flock id of auth_token if using Canarytoken Deploy Flock API key type)
        :param process_name: For kind==CanaryTokenKinds.SENSITIVE_COMMAND, name of the process you want to monitor (required when creating sensitive-cmd tokens)
        :param browser_redirect_url: URL to redirect attackers to after triggering token (required when creating fast-redirect and slow-redirect tokens)
        :param s3_source_bucket: S3 bucket to monitor for access (required when creating aws-s3 tokens)
        :param s3_log_bucket: S3 bucket where logs will be stored (required when creating aws-s3 tokens)
        :param process_name: Name of the process you want to monitor (required when creating sensitive-cmd tokens)
        :param expected_referrer: Domain to be used in cloned-css tokens
        :param azure_id_cert_file_name: Name of the azure login certificate file to be used in azure-id tokens, e.g. prod.pem
        :param google_share_email_addr: For kind==CanaryTokenKinds.GOOGLE_DOC or kind==CanaryTokenKinds.GOOGLE_SHEET, an email address to which to share the tokened document
        :param tokened_usernames: For kind==CanaryTokenKinds.ACTIVE_DIRECTORY_LOGIN, A comma separated list of Active Directory usernames to token (required when creating active-directory-login tokens)
        :param pwa_icon: For kind==CanaryTokenKinds.PWA, Name of the icon used by your Fake App for the pwa Canarytoken
        :param pwa_app_name: For kind==CanaryTokenKinds.PWA, Name of the Fake App for the pwa Canarytoken
        :param idp_app_type: For kind==CanaryTokenKinds.IDP_APP, type of IDP app to create.  See class IdpAppTypes for available types

        :return: A Result object
        :rtype: :class:`Result <Result>` object

        :except InvalidParameterError: One of the parameters was invalid
        :except CanaryTokenError: Something went wrong while creating the CanaryToken

        Usage::

            >>> import canarytools
            >>> result = console.tokens.create(memo='Desktop Token', kind=canarytools.CanaryTokenKinds.DOC_MSWORD)
        """
        recognized_params = (
            'flock_id',
            'web_image',
            'mimetype',
            'cloned_web',
            'custom_domain',
            'expiry',
            'flock_id',
            'process_name',
            'browser_redirect_url',
            's3_source_bucket',
            's3_log_bucket',
            'process_name',
            'expected_referrer',
            'azure_id_cert_file_name',
            'google_share_email_addr',
            'tokened_usernames',
            'pwa_icon',
            'pwa_app_name',
            'idp_app_type',
        )

        attempt_unrecognized = kwargs.pop('attempt_unrecognized', False)
        for p in kwargs:
            if p not in recognized_params:
                if attempt_unrecognized:
                    logger.debug(f'Unrecognized canarytoken create parameter: {p}')
                else:
                    raise InvalidParameterError(f'Unrecognized canarytoken create parameter: {p}')

        request_params = {**kwargs, **{
            'memo': memo,
            'kind': kind,
        }}
        files = {}

        # load image and send
        if 'web_image' in kwargs:
            web_image = kwargs['web_image']
            with open(web_image, 'rb') as f:
                mimetype = kwargs.get('mimetype', None)
                if not mimetype:
                    raise InvalidParameterError('Mimetype cannot be null')

                files['web_image'] = (os.path.basename(web_image), f, mimetype)

        if len(files) > 0:
            return self.console.post('canarytoken/create', request_params, self.parse, files)
        else:
            return self.console.post('canarytoken/create', request_params, self.parse)

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
        params = {'include_endpoints': str(include_endpoints)}
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
        return (
            '[Canarytoken] kind: {kind}; memo: {memo}; enabled: {enabled};'
            ' triggered count: {count}'.format(
                kind=self.kind,
                memo=self.memo,
                enabled=self.enabled,
                count=self.triggered_count,
            )
        )

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
        resp = self.console.get(
            'canarytoken/download', {'canarytoken': self.canarytoken}, raw_resp=True
        )
        disp = resp.headers['Content-Disposition'].split('filename=')
        if not filename:
            if len(disp) == 2 and disp[0] == 'attachment; ':
                filename = disp[-1]
            else:
                raise ValueError(
                    'CanaryToken.download() requires filename for this token'
                )
        with open(filename, 'wb') as fd:
            fd.write(resp.content)
        return filename

class CanaryTokenKinds(object):
    """
    This class provides properties that map to supported token kinds
    """

    ACTIVE_DIRECTORY_LOGIN = 'active-directory-login'
    """
    Windows scheduled task that alerts on Active Directory Logins
    """

    # AUTOREG_GOOGLE_DOC = 'autoreg-google-docs'
    # """
    # Google Doc that alerts when opened (factory token generated)
    # """

    # AUTOREG_GOOGLE_SHEET = 'autoreg-google-sheets'
    # """
    # Google Sheet that alerts when opened (factory token generated)
    # """

    AWS = 'aws-id'
    """
    Amazon Web Services API key that alerts when used
    """

    AZURE_ID = 'azure-id'
    """
    Azure Service Principal certificate that alerts when used to login with
    """

    AWSS3 = 'aws-s3'
    """
    S3 Bucket in your AWS account that alerts on any access
    """

    AZURE_ENTRA_LOGIN = 'azure-entra-login'
    """
    Trigger an alert when your Azure Entra ID login is being phished
    """

    CLONED_CSS = 'cloned-css'
    """
    CSS snippet that alerts when your website is cloned
    """

    CLONED_WEB = 'cloned-web'
    """
    Javascript snippet that alerts when your website is cloned
    """

    CREDIT_CARD = 'credit-card'
    """
    Credit Card that alerts when used
    """

    DNS = 'dns'
    """
    DNS hostname that alerts when queried
    """

    FASTREDIRECT = 'fast-redirect'
    """
    URL that alerts when hit and redirects to a chosen URL
    """

    GMAIL = 'gmail'
    """
    Create tokened mails in Gmail/G Suite mailboxes across your org
    """

    GOOGLE_DOC = 'google-docs'
    """
    Google Doc that alerts when opened
    """

    GOOGLE_SHEET = 'google-sheets'
    """
    Google Sheet that alerts when opened
    """

    IDP_APP = 'idp-app'
    """
    Fake SAML2 app that alerts when opened from your IdP dashboard
    """

    HTTP = 'http'
    """
    URL that alerts when hit
    """

    MSEXCEL = 'doc-msexcel'
    """
    Microsoft Excel document that alerts when opened
    """

    MSEXCELMACRO = 'msexcel-macro'
    """
    Microsoft Excel document that alerts when macro run
    """

    MSWORD = 'doc-msword'
    """
    Microsoft Word document that alerts when opened
    """

    MSWORDMACRO = 'msword-macro'
    """
    Microsoft Word document that alerts when macro run
    """

    MYSQL_DUMP = 'mysql-dump'
    """
    MySQL dump file that alerts when loaded
    """

    OFFICE365_MAIL = 'office365mail'
    """
    Archive emails in Office 365 mailboxes that alerts when URL inside hit
    """

    PDF = 'pdf-acrobat-reader'
    """
    PDF document that alerts when opened in Acrobat Reader
    """

    PWA = 'pwa'
    """
    Fake iOS/Android app that alerts when opened on mobile device
    """

    QRCODE = 'qr-code'
    """
    QR code for physical places or objects that alerts when scanned
    """

    SENSITIVE_COMMAND = 'sensitive-cmd'
    """
    Registry file to detect sensitive command execution (Windows)
    """

    SIGNEDEXE = 'signed-exe'
    """
    Modified EXE or DLL that alerts on execution
    """

    SLACK = 'slack-api'
    """
    Slack API key that alerts when used
    """

    SLOWREDIRECT = 'slow-redirect'
    """
    URL that alerts with browser fingerprint and redirects to a chosen URL
    """

    TOKEN_FACTORY = 'tokenfactory'
    """
    A factory that allows you to mint tokens using a specialised auth token and URL
    """

    WEB_IMAGE = 'web-image'
    """
    Customisable image URL that alerts when viewed
    """

    WINDOWS_DIR = 'windows-dir'
    """
    Windows Folder that alerts when browsed in Windows Explorer
    """

    WIREGUARD = 'wireguard'
    """
    WireGuard VPN client config that alerts when connected
    """

    DOC_MSWORD = 'doc-msword'


class IdpAppKinds(object):
    """
    This class provides properties that map to supported IDP app types
    """

    AWS = "aws"
    """
    aws IdP application
    """
    AZURE = "azure"
    """
    azure IdP application
    """
    BITWARDEN = "bitwarden"
    """
    bitwarden IdP application
    """
    DROPBOX = "dropbox"
    """
    dropbox IdP application
    """
    DUO = "duo"
    """
    duo IdP application
    """
    ELASTICSEARCH = "elasticsearch"
    """
    elasticsearch IdP application
    """
    FRESHBOOKS = "freshbooks"
    """
    freshbooks IdP application
    """
    GCLOUD = "gcloud"
    """
    gcloud IdP application
    """
    GDRIVE = "gdrive"
    """
    gdrive IdP application
    """
    GITHUB = "github"
    """
    github IdP application
    """
    GITLAB = "gitlab"
    """
    gitlab IdP application
    """
    GMAIL = "gmail"
    """
    gmail IdP application
    """
    INTUNE = "intune"
    """
    intune IdP application
    """
    JAMF = "jamf"
    """
    jamf IdP application
    """
    JIRA = "jira"
    """
    jira IdP application
    """
    KIBANA = "kibana"
    """
    kibana IdP application
    """
    LASTPASS = "lastpass"
    """
    lastpass IdP application
    """
    MS365 = "ms365"
    """
    ms365 IdP application
    """
    MSTEAMS = "msteams"
    """
    msteams IdP application
    """
    ONEDRIVE = "onedrive"
    """
    onedrive IdP application
    """
    ONEPASSWORD = "onepassword"
    """
    onepassword IdP application
    """
    OUTLOOK = "outlook"
    """
    outlook IdP application
    """
    PAGERDUTY = "pagerduty"
    """
    pagerduty IdP application
    """
    SAGE = "sage"
    """
    sage IdP application
    """
    SALESFORCE = "salesforce"
    """
    salesforce IdP application
    """
    SAP = "sap"
    """
    sap IdP application
    """
    SLACK = "slack"
    """
    slack IdP application
    """
    VIRTRU = "virtru"
    """
    virtru IdP application
    """
    ZENDESK = "zendesk"
    """
    zendesk IdP application
    """
    ZOHO = "zoho"
    """
    zoho IdP application
    """
    ZOOM = "zoom"
    """
    zoom IdP application
    """


class PwaIconKinds:
    """
    Valid values for pwa_icon when creating a PWA token
    """

    ABSA = 'absa',
    """
        Icon for Absa
    """

    AMEX = 'amex',
    """
        Icon for American Express
    """

    APPLEMAIL = 'applemail',
    """
        Icon for Mail
    """

    APPLEWALLET = 'applewallet',
    """
        Icon for Wallet
    """

    AXIS = 'axis',
    """
        Icon for Axis Mobile
    """

    BOA = 'boa',
    """
        Icon for Bank of America
    """

    BUMBLE = 'bumble',
    """
        Icon for Bumble
    """

    BUNQ = 'bunq',
    """
        Icon for bunq
    """

    CAPITEC = 'capitec',
    """
        Icon for Capitec
    """

    CHASE = 'chase',
    """
        Icon for Chase
    """

    CRED = 'cred',
    """
        Icon for CRED
    """

    DASHLANE = 'dashlane',
    """
        Icon for Dashlane
    """

    DISCORD = 'discord',
    """
        Icon for Discord
    """

    FACEBOOK = 'facebook',
    """
        Icon for Facebook
    """

    FNB = 'fnb',
    """
        Icon for FNB
    """

    GMAIL = 'gmail',
    """
        Icon for Gmail
    """

    GOOGLEPAY = 'googlepay',
    """
        Icon for GPay
    """

    GOOGLEWALLET = 'googlewallet',
    """
        Icon for Wallet
    """

    HDFC = 'hdfc',
    """
        Icon for HDFC Bank
    """

    HINGE = 'hinge',
    """
        Icon for Hinge
    """

    ICICI = 'icici',
    """
        Icon for iMobile Pay
    """

    INSTAGRAM = 'instagram',
    """
        Icon for Instagram
    """

    MESSENGER = 'messenger',
    """
        Icon for Messenger
    """

    MONZO = 'monzo',
    """
        Icon for Monzo
    """

    N26 = 'n26',
    """
        Icon for N26
    """

    NEDBANK = 'nedbank',
    """
        Icon for Nedbank
    """

    NORDPASS = 'nordpass',
    """
        Icon for NordPass
    """

    OLDMUTUAL = 'oldmutual',
    """
        Icon for Old Mutual
    """

    ONEPASSWORD = 'onepassword',
    """
        Icon for 1Password
    """

    PAYPAL = 'paypal',
    """
        Icon for PayPal
    """

    PAYTM = 'paytm',
    """
        Icon for Paytm
    """

    PHONEPE = 'phonepe',
    """
        Icon for PhonePe
    """

    PROTONPASS = 'protonpass',
    """
        Icon for Proton Pass
    """

    RBC = 'rbc',
    """
        Icon for RBC Mobile
    """

    REVOLUT = 'revolut',
    """
        Icon for Revolut
    """

    SBI = 'sbi',
    """
        Icon for YONO SBI
    """

    SIGNAL = 'signal',
    """
        Icon for Signal
    """

    SNAPCHAT = 'snapchat',
    """
        Icon for Snapchat
    """

    SNAPSCAN = 'snapscan',
    """
        Icon for SnapScan
    """

    STANDARD = 'standard',
    """
        Icon for Standard Bank
    """

    STARLING = 'starling',
    """
        Icon for Starling
    """

    TELEGRAM = 'telegram',
    """
        Icon for Telegram
    """

    TIKTOK = 'tiktok',
    """
        Icon for TikTok
    """

    TINDER = 'tinder',
    """
        Icon for Tinder
    """

    TWITTER = 'twitter',
    """
        Icon for X
    """

    WHATSAPP = 'whatsapp',
    """
        Icon for WhatsApp
    """

    ZAPPER = 'zapper',
    """
        Icon for Zapper
    """

