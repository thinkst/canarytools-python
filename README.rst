Python Canary API Wrapper
===================================

Thinkst Applied Research

Overview
------------
The Python Canary API Wrapper allows access to the Canary Web API.

.. _installation:

Installation
------------

The API is supported on python 2.7. The recommended way to
install the API Wrapper is via `pip <https://pypi.python.org/pypi/pip>`_.

.. code-block:: bash

   pip install canarytools

For instructions on installing python and pip see "The Hitchhiker's Guide to
Python" `Installation Guides
<http://docs.python-guide.org/en/latest/starting/installation/>`_.

Quickstart
----------

Assuming you have your API key handy as well as the domain of your website:

.. code-block:: python

  import canarytools
  console = canarytools.Console(api_key='API_KEY', domain='CLIENT_DOMAIN')

**Note:** You can find your API key and domain on your console. Head over to the console's setup page and under
*Canary Console API* you'll find your API key. Your domain is the tag in-front of 'canary.tools' in the console's
url. For example in https://testconsole.canary.tools/settings **testconsole** is the domain.

Alternatively,
you can download a configurations file from the *Canary Console API* tab. Inside the file you'll find instructions
on where to place it. If you have this on your system the *api_key* and *domain* parameters are no longer
necessary when instantiating a *Console* object.

With the ``console`` instance you can then interact with a Canary Console:

.. code-block:: python

  # Get all devices
  console.devices.all()

  # Acknowledge all incidents for a device older than 3 days
  console.incidents.acknowledge(node_id='329921d242c30b5e', older_than='3d')

  # Iterate all devices and start the update process
  for device in console.devices.all():
      device.update(update_tag='4ae023bdf75f14c8f08548bf5130e861')

  # Acknowledge and delete all host port scan Incidents
  for incident in console.incidents.unacknowledged():
      if isinstance(incident, canarytools.IncidentHostPortScan):
          incident.acknowledge()
          incident.delete()

  # Create a web image Canarytoken
  console.tokens.create(
      kind=canarytools.TokenKind.KIND_WEB_IMAGE,
      memo='Drop this token on DC box',
      web_image='/path/to/test.png',
      mimetype='image/png')

  # Print out the name of all incidents and the source IP address
  for incident in console.incidents.all():
      print incident.description, incident.src_host

Please see the API doc's `documentation <http://canarytools.readthedocs.io/>`_ for
more examples of what you can do with the Canary Console API.

Discussion and Support
---------------------------

Please file bugs and feature requests as issues on `GitHub
<https://github.com/thinkst/canarytools-python/issues>`_ after first searching to ensure a
similar issue was not already filed. If such an issue already exists please
give it a thumbs up reaction. Comments to issues containing additional
information are certainly welcome.

Documentation
-------------

The documentation is located at http://canarytools.readthedocs.io.

License
-------

The Python Canary API Wrapper's source (v1.0.0+) is provided under the `Revised BSD License
<https://github.com/thinkst/canarytools-python/blob/master/LICENSE.txt>`_.

* Copyright (c), 2017, Thinkst Applied Research
