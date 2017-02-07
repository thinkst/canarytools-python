.. _incidents-events-ref:

Incidents and event attribute
********************************

Each log entry is termed an event, and consists of actions such as a single SSH login attempt, or a single POST to a web site, or a single SIP request. An event will result in an incident being created, but subsequent similar events from the same source will be bundle together if they occur in close proximity. This means that if someone launches a brute-force attack, there is a single incident created with an event assigned to each login attempt.

The incident object contains a record of the individual events that constitute the incident.

The "events" attribute of each incident object contains a list of :class:`Event <Event>` objects.
object
Every :class:`Event <Event>` entry contains an "updated_std" timestamp field, and it's left out of the definitions below.

This page describes the different attributes an event may have depending on their type.

Canarytokens incidents
========================
Note: this incident type is forthcoming in Canary 2.0.

There are two types of Canarytokens, HTTP and DNS.

HTTP
------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "Canarytoken triggered"
    - **type (str)** -- "http"
    - **canarytoken (str)** -- Unique string that acts as the Canarytoken
    - **headers (dict)** -- Headers is a dict, Only present for HTTP Canarytokens.
    - **url (str)** -- URL of the HTTP Canarytoken.
    - **logtype (str)** -- "17000"

DNS
------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "Canarytoken triggered"
    - **type (str)** -- "dns"
    - **canarytoken (str)** -- Unique string that acts as the Canarytoken
    - **hostname (dict)** -- Hostname of the DNS Canarytoken.
    - **logtype (str)** -- "16000"

Port Scans
==============
There are five types of port scans incidents.

#. A host port scan is occurs when a single Canary is port scanned by a single source.
#. A consolidated network port scan occurs when multiple Canaries are scanned by a single source.
#. An NMAP NULL scan was run against the Canary.
#. An NMAP OS scan was run against the Canary.
#. An NMAP XMAS scan was run against the Canary.

Host Port Scan
----------------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "Host Port Scan"
    - **ports (list)** -- A list of ports scanned
    - **logtype (str)** -- "5003"

Consolidated Network Port Scan
--------------------------------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "Host Port Scan"
    - **ports_scanned (dict)** -- A dictionary of ports scanned and the IP address of the Canaries on which the scan occurred.
    - **logtype (str)** -- "5007"

NMAP NULL Scan
----------------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "NMAP NULL Scan Detected"
    - **logtype (str)** -- "5005"

NMAP OS Scan
----------------


The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "NMAP OS Scan Detected"
    - **logtype (str)** -- "5004"

NMAP XMAS Scan:
----------------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "NMAP XMAS Scan Detected"
    - **logtype (str)** -- "5006"


Canary Disconnected
======================
Event is generated when a Canary does not contact the console within a defined time period.

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "Canary Disconnected"
    - **logtype (str)** -- "1004"

FTP Incident
==============

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "FTP Login Attemp"
    - **username (list)** -- Attacker supplied username.
    - **password (list** --  Attacked supplied password.
    - **logtype (str)** -- "2000"


Git Repository Clone Attempt
=============================
Triggered when an attacker connects to the Canary git service and attempts any repo clone.

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "Git Repository Clone Attempt"
    - **host (list)** -- Git client's view of the Canary's hostname.
    - **repo (str)** -- Name of the repository the client attempted to clone.
    - **logtype (str)** -- "19001"


HTTP Incidents
================
Two types of HTTP Incidents:

#. Page loads, triggered by GET requests. They are disabled by default as they're noisy, and needs to be specifically enabled.
#. Login attempts, triggered by GET requests. They are always enabled.

HTTP Page Load
-----------------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "HTTP Page Load"
    - **path (list)** -- Web path requested by the source.
    - **useragent (str)** -- Useragent of the source's browser.
    - **channel (str)** -- Optional. Set to 'TLS' if an encrypted site is configured, otherwise absent.
    - **logtype (str)** -- "3000"


HTTP Login Attempt
--------------------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "HTTP Login Attempt"
    - **username (str)** -- Attack supplied username.
    - **password (str)** -- Attacked supplied password.
    - **path (list)** -- Web path requested by the source.
    - **useragent (str)** -- Useragent of the source's browser.
    - **channel (str)** -- Optional. Set to 'TLS' if an encrypted site is configured, otherwise absent.
    - **logtype (str)** -- "3001"


HTTP Proxy Request
=====================
Triggered by any request through the HTTP proxy module.

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "HTTP Proxy Request"
    - **username (str)** -- Attack supplied username.
    - **password (str)** -- Attacked supplied password.
    - **url (str)** -- URL requested by the source.
    - **useragent (str)** -- Useragent of the source's browser.
    - **logtype (str)** -- "7001"


MSSQL Login Attempt
=====================
Triggered by any attempt to authenticate to the MS-SQL Server module.

SQL Server supports multiple authentication modes, and the fields that come through depend on the mode.

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "MSSQL Login Attempt"
    - **username (str)** -- Attack supplied username.
    - **password (str)** -- Optional. Attacker supplied database password
    - **hostname (str)** -- Optional. Attacker supplied hostname.
    - **domainname (str)** -- Optional. Attacker supplied Active Directory name.
    - **logtype (str)** -- "9001" - SQL Server authentication.
    - **logtype (str)** -- "9002" - Windows authentication.


ModBus Request
=================
Note: this incident is forthcoming in Canary 2.0.

Triggered by any valid ModBus request.

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "ModBus Request"
    - **unit_id (str)** -- ModBus unit target.
    - **func_code (str)** -- ModBus function code.
    - **func_name (str)** -- Optional. ModBus function name, if available.
    - **sfunc_code (str)** -- Optional. ModBus subfunction code, if available.
    - **sfunc_nmae (str)** -- Optional. ModBus subfunction name, if available.
    - **logtype (str)** -- "18001" (Modbus Query Function)
    - **logtype (str)** -- "18002" (Modbus Read Function)
    - **logtype (str)** -- "18003" (Modbus Write Function)

MySQL Login Attempt
======================
Triggered by an authentication attempt against the MySQL service.

The client sends a hashed password, not a cleartext password. The Canary will try crack the hash with passwords one might expect in a brute-force.

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "MySQL Login Attempt"
    - **username (str)** -- Attacker supplied database username.
    - **client_hash (str)** -- Attacker supplied database password hash.
    - **salt (str)** -- Attacker supplied database password hash salt.
    - **password (str)** -- Recovered password if possible, otherwise '<Password not in common list>'
    - **logtype (str)** -- "8001


NTP Monlist Request
======================
Triggered by the NTP Monlist command.

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "NTP Monlist Request"
    - **ntp_cmd (str)** -- Name of the NTP command sent. Currently is 'monlist'.
    - **client_hash (str)** -- Attacker supplied database password hash.
    - **salt (str)** -- Attacker supplied database password hash salt.
    - **password (str)** -- Recovered password if possible, otherwise '<Password not in common list>'
    - **logtype (str)** -- "11001


Redis Command
===============
Note: this incident type is forthcoming in Canary 2.0.

Triggered by an attacker connecting to the Redis service and issuing valid Redis commands.

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "NTP Monlist Request"
    - **cmd (str)** -- Redis command issued by the attacker.
    - **args (str)** -- Arguments to the command.
    - **logtype (str)** -- "21001


SIP Request
=============
Triggered by an attacker connecting to the SIP service and issuing valid SIP request.

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "SIP Request"
    - **headers (dict)** -- Dict of the SIP headers included in the request.
    - **args (str)** -- Arguments to the command.
    - **logtype (str)** -- "15001


Shared File Opened
=====================
Triggered by the opening of a file on the Canary's Windows File Share.


The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "Shared File Opened"
    - **user (str)** --  Username supplied by the attacker.
    - **filename (str)** -- Name of file on the Canary that was accessed.
    - **auditaction (str)** -- Type of file action. Currently only 'pread'.
    - **domain (str)** -- Name of domain or workgroup.
    - **localname (str)** -- Windows Name of Canary machine.
    - **mode (str)** -- 'workgroup' or 'domain'
    - **offset (str)** -- Starting position of the read.
    - **remotename (str)** -- Windows Name of client machine.
    - **sharename (str)** -- Name of the share on which the file resides.
    - **size (str)** -- Amount of bytes read.
    - **smbarch (str)** -- Guess of the remote machine's Windows version.
    - **smbver (str)** -- Version of the SMB protocol that was used.
    - **status (str)** -- Result of the file read. Currently only 'ok'.
    - **logtype (str)** -- "5000


SNMP Request
===============
Triggered by an incoming SNMP query against the Canary.

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "SNMP Request"
    - **community_string (str)** -- SNMP community string supplied by attacker.
    - **requests (str)** -- SNMP OID requested by the attacker.
    - **logtype (str)** -- "13001"

SSH Login Attempt
===================
Triggered by an attempt to login to the Canary using SSH. Both password-based and key-based authentication is possible.

It is also possible to configure "Watched Credentials", which says to only alert if the attacker-supplied credentials match a configured list.

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "SSH Login Attempt"
    - **username (str)** -- SNMP community string supplied by attacker.
    - **password (str)** -- SNMP OID requested by the attacker.
    - **localversion (str)** -- SNMP community string supplied by attacker.
    - **remoteversion (str)** -- SNMP OID requested by the attacker.
    - **key (str)** -- SNMP community string supplied by attacker.
    - **watched_credentials (str)** -- SNMP OID requested by the attacker.
    - **logtype (str)** -- "4002"

Custom TCP Service Request
============================
Note: this incident type is forthcoming in Canary 2.0.

The Custom TCP Service module let's the Canary administrator create simple services that either immediately print a banner on connection, or wait for the client to send data before responding.

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "Custom TCP Service Request"
    - **banner_id (str)** -- Multiple banners are supported, the id identifies which banner service was triggered.
    - **data (str)** -- Optional. Attacker's supplied data.
    - **function (str)** -- Indicates which trigger fired, either 'DATA_RECEIVED' for when a banner was sent after the attacker sent data, or 'CONNECTION_MADE' for when a banner was sent immediately on connection.
    - **logtype (str)** -- "20001" (Banner set immediately on connection)
    - **logtype (str)** -- "20002" (Banner sent after client sent a line)

TFTP Request
==============
Triggered by a TFTP request against the Canary.

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "TFTP Request"
    - **filename (str)** -- Name of file the attacker tried to act on.
    - **opcode (str)** -- File action, either 'READ' or 'WRITE'
    - **logtype (str)** -- "10001"


Telnet Login Attempt
=======================
Triggered by a Telnet authentication attempt.

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "Telnet Login Attempt"
    - **username (str)** -- Attacker supplied username.
    - **password (str)** -- Attacker supplied password.
    - **logtype (str)** -- "6001"

VNC Login Attempt
====================
Triggered by an attempt to login to Canary's password protected VNC service.

VNC passwords are not transmitted in the clear. Instead a hashed version is sent. The Canary will test the hashed password against a handful of common passwords to guess the password, but the hash parameters are also reported so the administrator can crack the hash on more powerful rigs.

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "VNC Login Attempt"
    - **password (str)** -- Cracked password if very weak.
    - **server_challenge (str)** -- VNC password hashing parameter.
    - **client_response (str)** -- VNC password hashing parameter.
    - **logtype (str)** -- "12001"

