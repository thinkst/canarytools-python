
Canary Console API Python Client v1
*******************************************

.. module:: canarytools

.. _console-int-ref:

Main Interface
=======================
.. autoclass:: canarytools.console.Console
   :members: ping

.. _exceptions-int-ref:

Exceptions
=======================

All endpoints can raise the following errors:

**Errors:**
   - **InvalidAuthTokenError** – API authorization token is invalid
   - **ConnectionError** – A connection error occurred while sending a request to the console
   - **ConsoleError** – A general exception occurred

More specific endpoint errors are listed in an endpoint's documentation.

.. _devices-int-ref:

Devices Interface
=======================
API calls for managing devices. All methods endpoints are accessed by first initializing
a console object and by making calls as follows:

.. code-block:: python

   console.devices.dead()

   console.devices.get_device('0000000000231c23')

.. autoclass:: canarytools.models.devices.Devices
   :members: all, live, dead, get_device

.. _incidents-int-ref:

Incidents Interface
=======================
API calls for managing incidents. All methods endpoints are accessed by first initializing
a console object and by making calls as follows:

.. code-block:: python

   console.incidents.all()

   console.incidents.delete()

.. autoclass:: canarytools.models.incidents.Incidents
   :members: all, unacknowledged, acknowledged, acknowledge, unacknowledge,
      delete, get_incident

.. _tokens-int-ref:

Canarytokens Interface
=======================
API calls for managing Canarytokens. All methods endpoints are accessed by first initializing
a console object and by making calls as follows:

.. code-block:: python

   console.tokens.all()

   canarytools.tokens.create(memo='Desktop Token', kind=canarytools.CanaryTokenKinds.DOC_MSWORD)

.. autoclass:: canarytools.models.canarytokens.CanaryTokens
   :members: create, get_token, all

.. _flocks-int-ref:

Flocks Interface
=================
API calls for managing Flocks. All methods endpoints are accessed by first initializing
a console object and by making calls as follows:

.. code-block:: python

   console.flocks.all()

   canarytools.flocks.create(name='Cape Town')

.. autoclass:: canarytools.models.flocks.Flocks
   :members: create, all

.. _settings-int-ref:

Settings Interface
=======================

.. autoclass:: canarytools.models.settings.Settings
   :members: is_ip_whitelisted, whitelist_ip_port

.. _updates-int-ref:

Updates Interface
=======================

.. autoclass:: canarytools.models.update.Updates
   :members: list_updates, update_device

Returned Classes
=======================

This section describes the objects returned from the various interfaces described above. These objects
represent console entities. For example, the :class:`Device <Device>` object encapsulates all the information related to
a specific device. Operations can be performed on these objects too. See below for more information.

.. autoclass:: Device
   :members: reboot, update, list_databundles, refresh

.. autoclass:: Incident
   :members: unacknowledge, acknowledge, delete, refresh

.. autoclass:: CanaryToken
   :members: update, delete, disable, enable

.. autoclass:: Flock
   :members: rename, delete

.. autoclass:: Update

.. autoclass:: DataBundle

.. autoclass:: Result

.. autoclass:: Event
