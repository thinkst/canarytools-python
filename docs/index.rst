.. canarytools documentation master file, created by
   sphinx-quickstart on Mon Jan 30 17:35:20 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: _static/images/logo_canary@2x.png

Welcome to canarytools's documentation!
=======================================

This Python library wraps the Canarytools API, for deploying and managing `Thinkst Canary honeypots <https://canary.tools>`_.

NOTE: This API  is still in Beta.

Requirements
=======================
Python 2.7+, Python 3.3+

Installation
=======================
The recommended way to install the API Wrapper is via pip.

.. code-block:: bash

    pip install canarytools

For instructions on installing python and pip see “The Hitchhiker’s Guide to Python”
`Installation Guides <http://docs.python-guide.org/en/latest/starting/installation/>`_

Using the Library
=======================

All uses of the Canary Console API start by importing the library module and instantiating the ``Console`` class.

.. code-block:: python

    import canarytools
    client = canarytools.Console('YOUR_DOMAIN', 'YOUR_API_KEY')

Alternatively, you can download a configuration file from your console's *Canary Console API* settings tab.
Place this file in your home directory (*~/* for Unix environments and *C:\\Users\\{Current User}\\*
for Windows Environments). With this file in place you can instantiate the ``Console`` class without needing the API
token nor the domain anywhere in your code.

.. code-block:: python

    import canarytools
    client = canarytools.Console()

You may also specify the timezone to be used to format time specific data.

.. code-block:: python

    import canarytools
    from pytz import timezone
    console = canarytools.Console(timezone=timezone('US/Eastern'))

After instantiating the ``Console`` class, you're ready to start making calls. See :ref:`console-int-ref` for more details
on the ``Console`` class.

Quick Start
=======================

With the ``Console`` instance it's easy to do all the cool things you can do on the Canary Console webpage. Let's take a look at some key features.

Devices
-----------------------

The API makes managing your devices simple. Managing more than one device at a time can become difficult. Why not
manage them programmatically?

.. code-block:: python

  # Get all devices
  console.devices.all()

Updating and rebooting all your devices can be done in just a few lines of code.

.. code-block:: python

  # Iterate all devices and start the update process
  for device in console.devices.all():
      device.update(update_tag='4ae023bdf75f14c8f08548bf5130e861')

If you'd like to see more cool things you can do with your devices, see :ref:`devices-int-ref`.

Incidents
-----------------------

Keep a handle on incidents. Want to quickly acknowledge a large batch? No problem!

.. code-block:: python

  # Acknowledge all incidents for a device older than 3 days
  console.incidents.acknowledge(node_id='329921d242c30b5e', older_than='3d')

Perhaps you'd just like to do a large clean up of a specific incident type? Don't forget to acknowledge before deleting!

.. code-block:: python

  # Acknowledge and delete all host port scan Incidents
  for incident in console.incidents.unacknowledged():
      if isinstance(incident, canarytools.IncidentHostPortScan):
          incident.acknowledge()
          incident.delete()

Get important incident information quickly. Perhaps to be piped to your SIEM system.

.. code-block:: python

  # Print out the name of all incidents and the source IP address
  for incident in console.incidents.all():
      print incident.description, incident.src_host

To see more head to :ref:`incidents-int-ref`.

Canarytokens
-----------------------

Canarytokens are our form of agentless detection. More information is `on the tokens site <http://canarytokens.org>`_
and `this blog post <http://blog.thinkst.com/p/canarytokensorg-quick-free-detection.html>`_.

You can manage your cool Canarytokens with the canarytools library!

.. code-block:: python

  # Create a web image Canarytoken
  console.tokens.create(
      kind=canarytools.CanaryTokenKinds.KIND_WEB_IMAGE,
      memo='Drop this token on DC box',
      web_image='/path/to/test.png',
      mimetype='image/png')

Read more at :ref:`tokens-int-ref`.

Flocks
-----------------------

Flocks are organisation groupings of Canaries.

.. code-block:: python

  # List Flocks on your Canary Console
  console.flocks.all()

Read more at :ref:`flocks-int-ref`.

Settings
-----------------------

Ignorelist devices like scanners and other harmless hosts.

.. code-block:: python

  # Ignorelist IP and destionation port
  console.settings.whitelist_ip_port('10.0.0.2', '5000')

For a complete list of options see :ref:`settings-int-ref`.

Updates
-----------------------

Keep an eye out for new device updates.

.. code-block:: python

    # List all available updates
    for update in console.updates.list_updates():
        print update.tag()

See :ref:`updates-int-ref` for more.

API Documentation
=======================

.. toctree::
   :maxdepth: 2

   console_python_api_v1
   incident_attributes
