.. _incidents-events-ref:

Incidents and event attributes
********************************

An incident is an alert that gets fired. This groups together any number of events that are worth alerting on. A single SSH Login Attempt incident can be made up of multiple attempts that use different username and password combinations against a Canary. Likewise, a single HTTP Login Attempt incident can be made up of multiple HTTP POST events to a Canary website. The events are bundled together if they occur within a short time of each other and from a single attacker. Brute force attempts on a service then get grouped together into an incident.

Each incident object has an **events** attribute storing its list of :class:`Event <Event>` objects. This page describes the different attributes events have depending on their type. Each event also contains a "updated_std" timestamp field, which is omitted for brevity below.


Canarytokens incidents
======================

There are two types of Canarytokens, HTTP and DNS.

HTTP
----

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Event Attributes:**
    - **description** -- "Canarytoken triggered"
    - **type (str)** -- "http"
    - **canarytoken (str)** -- Unique string that acts as the Canarytoken
    - **headers (dict)** -- Headers is a dict, Only present for HTTP Canarytokens.
    - **url (str)** -- URL of the HTTP Canarytoken.
    - **logtype (str)** -- "17000"

Web Image
---------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Event Attributes:**
    - **description** -- "Remote Web Image"
    - **type (str)** -- "web-image"
    - **canarytoken (str)** -- Unique string that acts as the Canarytoken
    - **headers (dict)** -- Headers is a dict, Only present for HTTP Canarytokens.
    - **url (str)** -- URL of the HTTP Canarytoken.
    - **logtype (str)** -- "17001"
    - **web_image (str)** -- Byte string of the web image
    - **web_image_type (str)** -- Type of the web image
    - **web_image_name (str)** -- Name of the web image

MS Word Doc
-----------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Event Attributes:**
    - **description** -- "Canarytoken triggered"
    - **type (str)** -- "doc-msword"
    - **canarytoken (str)** -- Unique string that acts as the Canarytoken
    - **headers (dict)** -- Headers is a dict, Only present for HTTP Canarytokens.
    - **url (str)** -- URL of the HTTP Canarytoken.
    - **logtype (str)** -- "17002"
    - **doc (str)** -- Byte String of the tokened document 
    - **doc_name (str)** -- Name of the document tokened (or created)
    - **doc_type (str)** -- Type of document chosen (doc or docx)

Cloned Site
-----------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Event Attributes:**
    - **description** -- "Cloned Website"
    - **type (str)** -- "cloned-web"
    - **canarytoken (str)** -- Unique string that acts as the Canarytoken
    - **headers (dict)** -- Headers is a dict, Only present for HTTP Canarytokens.
    - **url (str)** -- URL of the HTTP Canarytoken.
    - **logtype (str)** -- "17003"
    - **cloned_web (str) ** -- Domain that we are tokening

AWS S3
------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Event Attributes:**
    - **description** -- "Amazon S3"
    - **type (str)** -- "aws-s3"
    - **canarytoken (str)** -- Unique string that acts as the Canarytoken
    - **headers (dict)** -- Headers is a dict, Only present for HTTP Canarytokens.
    - **url (str)** -- URL of the HTTP Canarytoken.
    - **logtype (str)** -- "17005"
    - **s3_source_bucket (str)** -- bucket that we are tokening
    - **s3_log_bucket (str)** -- bucket where logging to stored and monitored
    - **online (str)** -- Whether the token is online or not

Google docs
-----------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Event Attributes:**
    - **description** -- "Google Document"
    - **type (str)** -- "google-docs"
    - **canarytoken (str)** -- Unique string that acts as the Canarytoken
    - **headers (dict)** -- Headers is a dict, Only present for HTTP Canarytokens.
    - **url (str)** -- URL of the HTTP Canarytoken.
    - **logtype (str)** -- "17006"
    - **docs_link (str)** -- url to the google doc
    - **email_link (str)** -- url used for email
    - **document_name (str)** -- Name of the document

Google sheets
-------------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Event Attributes:**
    - **description** -- "Google Sheet"
    - **type (str)** -- "google-sheets"
    - **canarytoken (str)** -- Unique string that acts as the Canarytoken
    - **headers (dict)** -- Headers is a dict, Only present for HTTP Canarytokens.
    - **url (str)** -- URL of the HTTP Canarytoken.
    - **logtype (str)** -- "17007"
    - **docs_link (str)** -- url to the google doc
    - **email_link (str)** -- url used for email
    - **document_name (str)** -- Name of the document

Signed EXE
----------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Event Attributes:**
    - **description** -- "Signed Exe"
    - **type (str)** -- "signed-exe"
    - **canarytoken (str)** -- Unique string that acts as the Canarytoken
    - **headers (dict)** -- Headers is a dict, Only present for HTTP Canarytokens.
    - **url (str)** -- URL of the HTTP Canarytoken.
    - **logtype (str)** -- "17008"
    - **exe (str)** -- Byte string of the tokened exe
    - **exe_name (str)** -- Name of the exe
    - **exe_type (str)** -- Type of the exe

QR Code
-------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Event Attributes:**
    - **description** -- "QR Code"
    - **type (str)** -- "qr-code"
    - **canarytoken (str)** -- Unique string that acts as the Canarytoken
    - **headers (dict)** -- Headers is a dict, Only present for HTTP Canarytokens.
    - **url (str)** -- URL of the HTTP Canarytoken.
    - **logtype (str)** -- "17009"
    - **qr_code (str)** -- Byte string of the tokened QR code

SVN
---

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Event Attributes:**
    - **description** -- "SVN Repo"
    - **type (str)** -- "svn"
    - **canarytoken (str)** -- Unique string that acts as the Canarytoken
    - **headers (dict)** -- Headers is a dict, Only present for HTTP Canarytokens.
    - **url (str)** -- URL of the HTTP Canarytoken.
    - **logtype (str)** -- "17010"

SQL
---

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Event Attributes:**
    - **description** -- "SQL Server"
    - **type (str)** -- "sql"
    - **canarytoken (str)** -- Unique string that acts as the Canarytoken
    - **headers (dict)** -- Headers is a dict, Only present for HTTP Canarytokens.
    - **url (str)** -- URL of the HTTP Canarytoken.
    - **logtype (str)** -- "17011"
    - **trigger_type (str)** -- SQL trigger type (SELECT, UPDATE, INSERT, DELETE)
    - **table_name (str)** -- SQL table name (trigger_type: UPDATE, INSERT,DELETE)
    - **trigger_name (str)** -- SQL trigger name (trigger_type: UPDATE, INSERT,DELETE)
    - **view_name (str)** -- SQL View name (trigger_type: SELECT)
    - **function_name (str)** -- SQL function name (trigger_type: SELECT)

AWS ID
------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Event Attributes:**
    - **description** -- "Amazon API Key"
    - **type (str)** -- "aws-id"
    - **canarytoken (str)** -- Unique string that acts as the Canarytoken
    - **headers (dict)** -- Headers is a dict, Only present for HTTP Canarytokens.
    - **url (str)** -- URL of the HTTP Canarytoken.
    - **logtype (str)** -- "17012"
    - **secret_access_key (str)** -- AWS generated secret access key
    - **access_key_id (str)** -- AWS generated access key ID

Fast Redirect
-------------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Event Attributes:**
    - **description** -- "Fast HTTP Redirect"
    - **type (str)** -- "fast-redirect"
    - **canarytoken (str)** -- Unique string that acts as the Canarytoken
    - **headers (dict)** -- Headers is a dict, Only present for HTTP Canarytokens.
    - **url (str)** -- URL of the HTTP Canarytoken.
    - **logtype (str)** -- "17016"
    - **browser_redirect_url (str)** -- Original url attempted before redirect

Slow Redirect
-------------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Event Attributes:**
    - **description** -- "Slow HTTP Redirect"
    - **type (str)** -- "slow-redirect"
    - **canarytoken (str)** -- Unique string that acts as the Canarytoken
    - **headers (dict)** -- Headers is a dict, Only present for HTTP Canarytokens.
    - **url (str)** -- URL of the HTTP Canarytoken.
    - **logtype (str)** -- "17017"
    - **browser_redirect_url (str)** -- Original url attempted before redirect

DNS
---

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Event Attributes:**
    - **description** -- "DNS"
    - **type (str)** -- "dns"
    - **canarytoken (str)** -- Unique string that acts as the Canarytoken
    - **hostname (dict)** -- Hostname of the DNS Canarytoken.
    - **logtype (str)** -- "16000"

Desktop ini
-----------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Event Attributes:**
    - **description** -- "Windows Directory Browsing"
    - **type (str)** -- "windows-dir"
    - **canarytoken (str)** -- Unique string that acts as the Canarytoken
    - **hostname (dict)** -- Hostname of the DNS Canarytoken.
    - **logtype (str)** -- "16006"

Adobe Reader PDF
----------------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Event Attributes:**
    - **description** -- "Acrobat Reader PDF Document"
    - **type (str)** -- "pdf-acrobat-reader"
    - **canarytoken (str)** -- Unique string that acts as the Canarytoken
    - **hostname (dict)** -- Hostname of the DNS Canarytoken.
    - **logtype (str)** -- "16008"

MS Word Doc Macroed
-------------------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Event Attributes:**
    - **description** -- "MS Word .docm Document"
    - **type (str)** -- "msword-macro"
    - **canarytoken (str)** -- Unique string that acts as the Canarytoken
    - **hostname (dict)** -- Hostname of the DNS Canarytoken.
    - **logtype (str)** -- "16009"
    - **doc (str)** -- Byte String of the tokened document 
    - **doc_name (str)** -- Name of the document
    - **doc_type (str)** -- Type of document chosen (doc or docx)

MS Excel Doc Macroed
--------------------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Event Attributes:**
    - **description** -- "MS Excel .xlsm Document"
    - **type (str)** -- "msexcel-macro"
    - **canarytoken (str)** -- Unique string that acts as the Canarytoken
    - **hostname (dict)** -- Hostname of the DNS Canarytoken.
    - **logtype (str)** -- "16010"
    - **doc (str)** -- Byte String of the tokened document 
    - **doc_name (str)** -- Name of the document
    - **doc_type (str)** -- Type of document chosen (doc or docx)

Port Scans
==========
There are five types of port scan incidents.

#. A host port scan occurs when a single Canary is port scanned by a single source.
#. A consolidated network port scan occurs when multiple Canaries are scanned by a single source.
#. An NMAP NULL scan was run against the Canary.
#. An NMAP OS scan was run against the Canary.
#. An NMAP XMAS scan was run against the Canary.

Host Port Scan
--------------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "Host Port Scan"
    - **ports (list)** -- A list of ports scanned
    - **logtype (str)** -- "5003"

Consolidated Network Port Scan
------------------------------

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

NMAP OS Scan:
-------------


The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "NMAP OS Scan Detected"
    - **logtype (str)** -- "5004"

NMAP XMAS Scan:
---------------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "NMAP XMAS Scan Detected"
    - **logtype (str)** -- "5006"

NMAP FIN Scan:
--------------

The :class:`Event <Event>` object in this scenario will have the following attributes:

**Attributes:**
    - **description** -- "NMAP FIN Scan Detected"
    - **logtype (str)** -- "5008"


Canary Disconnected
======================
A Disconnect event is generated when a Canary does not contact the console within a defined time period.

The :class:`Incident <Incident>` object in this scenario will have the following attributes:

**Incident Attributes:**
    - **description** -- "Canary Disconnected"
    - **logtype (str)** -- "1004"

FTP Incident
==============

The :class:`Incident <Incident>` and :class:`Event <Event>` objects will have the following attributes:

**Incident Attributes:**
    - **description** -- "FTP Login Attempt"
    - **logtype (str)** -- "2000"

**Event Attributes:**
    - **username (list)** -- Attacker supplied username.
    - **password (list** --  Attacked supplied password.


Git Repository Clone Attempt
=============================
Triggered when an attacker connects to the Canary git service and attempts any repo clone.

The :class:`Incident <Incident>` and :class:`Event <Event>` objects will have the following attributes:

**Incident Attributes:**
    - **description** -- "Git Repository Clone Attempt"
    - **logtype (str)** -- "19001"

**Event Attributes:**
    - **host (list)** -- Git client's view of the Canary's hostname.
    - **repo (str)** -- Name of the repository the client attempted to clone.


HTTP Incidents
================
Two types of HTTP Incidents:

#. Page loads, triggered by GET requests. They are disabled by default as they're noisy and need to be specifically enabled.
#. Login attempts, triggered by GET requests. They are always enabled.

HTTP Page Load
-----------------

The :class:`Incident <Incident>` and :class:`Event <Event>` objects will have the following attributes:

**Incident Attributes:**
    - **description** -- "HTTP Page Load"
    - **logtype (str)** -- "3000"

**Event Attributes:**
    - **path (list)** -- Web path requested by the source.
    - **useragent (str)** -- Useragent of the source's browser.
    - **channel (str)** -- Optional. Set to 'TLS' if an encrypted site is configured, otherwise absent.


HTTP Login Attempt
--------------------

The :class:`Incident <Incident>` and :class:`Event <Event>` objects will have the following attributes:

**Incident Attributes:**
    - **description** -- "HTTP Login Attempt"
    - **logtype (str)** -- "3001"

**Event Attributes:**
    - **username (str)** -- Attack supplied username.
    - **password (str)** -- Attacked supplied password.
    - **path (list)** -- Web path requested by the source.
    - **useragent (str)** -- Useragent of the source's browser.
    - **channel (str)** -- Optional. Set to 'TLS' if an encrypted site is configured, otherwise absent.


HTTP Proxy Request
=====================
Triggered by any request through the HTTP proxy module.

The :class:`Incident <Incident>` and :class:`Event <Event>` objects will have the following attributes:

**Incident Attributes:**
    - **description** -- "HTTP Proxy Request"
    - **logtype (str)** -- "7001"

**Event Attributes:**
    - **username (str)** -- Attack supplied username.
    - **password (str)** -- Attacked supplied password.
    - **url (str)** -- URL requested by the source.
    - **useragent (str)** -- Useragent of the source's browser.


Microsoft SQL Server Login Attempt
===================================
Triggered by any attempt to authenticate to the Microsoft SQL Server module.

SQL Server supports multiple authentication modes and the fields that come through depend on the mode.

The :class:`Incident <Incident>` and :class:`Event <Event>` objects will have the following attributes:

**Incident Attributes:**
    - **description** -- "MSSQL Login Attempt"
    - **logtype (str)** -- "9001" - SQL Server authentication.
    - **logtype (str)** -- "9002" - Windows authentication.


**Event Attributes:**
    - **username (str)** -- Attack supplied username.
    - **password (str)** -- Optional. Attacker supplied database password
    - **hostname (str)** -- Optional. Attacker supplied hostname.
    - **domainname (str)** -- Optional. Attacker supplied Active Directory name.

Modbus Request
=================

Triggered by any valid Modbus request.

The :class:`Incident <Incident>` and :class:`Event <Event>` objects will have the following attributes:

**Incident Attributes:**
    - **description** -- "ModBus Request"
    - **logtype (str)** -- "18001" (Modbus Query Function)
    - **logtype (str)** -- "18002" (Modbus Read Function)
    - **logtype (str)** -- "18003" (Modbus Write Function)


**Event Attributes:**
    - **unit_id (str)** -- ModBus unit target.
    - **func_code (str)** -- ModBus function code.
    - **func_name (str)** -- Optional. ModBus function name, if available.
    - **sfunc_code (str)** -- Optional. ModBus subfunction code, if available.
    - **sfunc_nmae (str)** -- Optional. ModBus subfunction name, if available.

MySQL Login Attempt
======================
Triggered by an authentication attempt against the MySQL service.

The client sends a hashed password, not a cleartext password. The Canary will try to crack the hash with passwords one might expect in a brute-force.

The :class:`Incident <Incident>` and :class:`Event <Event>` objects will have the following attributes:

**Incident Attributes:**
    - **description** -- "MySQL Login Attempt"
    - **logtype (str)** -- "8001

**Event Attributes:**
    - **username (str)** -- Attacker supplied database username.
    - **client_hash (str)** -- Attacker supplied database password hash.
    - **salt (str)** -- Attacker supplied database password hash salt.
    - **password (str)** -- Recovered password if possible, otherwise '<Password not in common list>'


NTP Monlist Request
======================
Triggered by the NTP Monlist command.

The :class:`Incident <Incident>` and :class:`Event <Event>` objects will have the following attributes:

**Incident Attributes:**
    - **description** -- "NTP Monlist Request"
    - **logtype (str)** -- "11001

**Event Attributes:**
    - **ntp_cmd (str)** -- Name of the NTP command sent. Currently is 'monlist'.
    - **client_hash (str)** -- Attacker supplied database password hash.
    - **salt (str)** -- Attacker supplied database password hash salt.
    - **password (str)** -- Recovered password if possible, otherwise '<Password not in common list>'



Redis Command
===============

Triggered by an attacker connecting to the Redis service and issuing valid Redis commands.

The :class:`Incident <Incident>` and :class:`Event <Event>` objects will have the following attributes:

**Incident Attributes:**
    - **description** -- "Redis Command"
    - **logtype (str)** -- "21001

**Event Attributes:**
    - **cmd (str)** -- Redis command issued by the attacker.
    - **args (str)** -- Arguments to the command.


SIP Request
=============
Triggered by an attacker connecting to the SIP service and issuing a valid SIP request.

The :class:`Incident <Incident>` and :class:`Event <Event>` objects will have the following attributes:

**Incident Attributes:**
    - **description** -- "SIP Request"
    - **logtype (str)** -- "15001

**Event Attributes:**
    - **headers (dict)** -- Dict of the SIP headers included in the request.
    - **args (str)** -- Arguments to the command.


Shared File Opened
=====================
Triggered by the opening of a file on the Canary's Windows File Share.


The :class:`Incident <Incident>` and :class:`Event <Event>` objects will have the following attributes:

**Incident Attributes:**
    - **description** -- "Shared File Opened"
    - **logtype (str)** -- "5000

**Event Attributes:**
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


SNMP Request
===============
Triggered by an incoming SNMP query against the Canary.

The :class:`Incident <Incident>` and :class:`Event <Event>` objects will have the following attributes:

**Incident Attributes:**
    - **description** -- "SNMP Request"
    - **logtype (str)** -- "13001"

**Event Attributes:**
    - **community_string (str)** -- SNMP community string supplied by attacker.
    - **requests (str)** -- SNMP OID requested by the attacker.

SSH Login Attempt
===================
Triggered by an attempt to login to the Canary using SSH. Both password-based and key-based authentication is possible.

It is also possible to configure "Watched Credentials", which says to only alert if the attacker-supplied credentials match a configured list.

The :class:`Incident <Incident>` and :class:`Event <Event>` objects will have the following attributes:

**Incident Attributes:**
    - **description** -- "SSH Login Attempt"
    - **logtype (str)** -- "4002"

**Event Attributes:**
    - **username (str)** -- SSH username
    - **password (str)** -- SSH password
    - **localversion (str)** -- SSH server string supplied by canary.
    - **remoteversion (str)** -- SSH client string supplied by the attacker.
    - **key (str)** -- SSH key used by attacker.
    - **watched_credentials (str)** -- Indicates whether this an SSH key watched for.

Custom TCP Service Request
============================

The Custom TCP Service module lets the Canary administrator create simple services that either immediately prints a banner on connection, or wait for the client to send data before responding.

The :class:`Incident <Incident>` and :class:`Event <Event>` objects will have the following attributes:


**Incident Attributes:**
    - **description** -- "Custom TCP Service Request"

**Event Attributes:**
    - **banner_id (str)** -- Multiple banners are supported, the id identifies which banner service was triggered.
    - **data (str)** -- Optional. Attacker's supplied data.
    - **function (str)** -- Indicates which trigger fired, either 'DATA_RECEIVED' for when a banner was sent after the attacker sent data or 'CONNECTION_MADE' for when a banner was sent immediately on connection.
    - **logtype (str)** -- "20001" (Banner set immediately on connection)
    - **logtype (str)** -- "20002" (Banner sent after client sent a line)

TFTP Request
==============
Triggered by a TFTP request against the Canary.

The :class:`Incident <Incident>` and :class:`Event <Event>` objects will have the following attributes:

**Incident Attributes:**
    - **description** -- "TFTP Request"
    - **logtype (str)** -- "10001"

**Event Attributes:**
    - **filename (str)** -- Name of file the attacker tried to act on.
    - **opcode (str)** -- File action, either 'READ' or 'WRITE'


Telnet Login Attempt
=======================
Triggered by a Telnet authentication attempt.

The :class:`Incident <Incident>` and :class:`Event <Event>` objects will have the following attributes:

**Incident Attributes:**
    - **description** -- "Telnet Login Attempt"
    - **logtype (str)** -- "6001"

**Event Attributes:**
    - **username (str)** -- Attacker supplied username.
    - **password (str)** -- Attacker supplied password.

VNC Login Attempt
====================
Triggered by an attempt to log in to Canary's password-protected VNC service.

VNC passwords are not transmitted in the clear. Instead, a hashed version is sent. The Canary will test the hashed password against a handful of common passwords to guess the password, but the hash parameters are also reported so the administrator can crack the hash on more powerful rigs.

**Incident Attributes:**
    - **description** -- "VNC Login Attempt"
    - **logtype (str)** -- "12001"

**Event Attributes:**
    - **password (str)** -- Cracked password if very weak.
    - **server_challenge (str)** -- VNC password hashing parameter.
    - **client_response (str)** -- VNC password hashing parameter.

Console Settings Changed
========================
Triggered by a Canary console setting being changed.

**Incident Attributes:**
    - **description** -- "Console Settings Changed"
    - **logtype (str)** -- "23001"

**Event Attributes:**
    - **settings (str)** -- the settings that were changed.

Device Settings Changed
========================
Triggered by a Canary's settings being changed.

**Incident Attributes:**
    - **description** -- "Device Settings Changed"
    - **logtype (str)** -- "23002"

**Event Attributes:**
    - **settings (str)** -- the settings that were changed.

Flock Settings Changed
========================
Triggered by a flock's settings being changed.

**Incident Attributes:**
    - **description** -- "Flock Settings Changed"
    - **logtype (str)** -- "23003"

**Event Attributes:**
    - **settings (str)** -- the settings that were changed.

Rollback Network Settings
=========================
Triggered by a Canary rolling back its settings after an unsuccessful attempt to change
its network settings.

**Incident Attributes:**
    - **description** -- "Network Settings Roll-back"
    - **logtype (str)** -- "22001"
