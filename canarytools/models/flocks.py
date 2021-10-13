import os

from .base import CanaryToolsBase
from ..exceptions import InvalidParameterError


class Flocks(object):
    def __init__(self, console):
        """Initialize Flock

        :param console: The Console object from which API calls are made
        """
        self.console = console

    def create(self, name):
        """Create a new Flock

        :param name: Use this to give your Flock a human readable name
        :return: A Result object
        :rtype: :class:`Result <Result>` object

        :except FlockError: Something went wrong while creating the Flock

        Usage::

            >>> import canarytools
            >>> result = console.flocks.create(name='Cape Town')
        """
        params = {'name': name}
        return self.console.post('flock/create', params, self.parse)

    def all(self):
        """Fetch all Flocks

        :return: A list of Flock objects
        :rtype: List of :class:`Flock <Flock>` objects

        :except FlockError: Something went wrong while getting the Flocks

        Usage::

            >>> import canarytools
            >>> flocks = console.flocks.all()
        """
        return self.console.get('flocks/list', {}, self.parse)

    def parse(self, data):
        """Parse JSON data

        :param data: JSON data returned from the web API
        :return: An initliazed list of Flocks or a single Flock
        """
        flocks = list()
        if data and 'flocks' in data:
            for flock_id, name in data['flocks'].items():
                flocks.append(
                    Flock.parse(self.console,
                    {'flock_id': flock_id, 'name': name})
                )
        elif data and 'flock' in data:
            return Flock.parse(self.console, data['flock'])
        elif data and 'flock_id' in data:
            for flock in self.console.flocks.all():
                if flock.flock_id == data['flock_id']:
                    return flock
        return flocks


class Flock(CanaryToolsBase):
    def __init__(self, console, data):
        """Initialize a Flock object

        **Attributes:**
            - **flock_id (str)** -- The id the flock
            - **name (str)** -- The name of the flock

        :param console: The Console from which the API calls are made
        :param data: JSON data containing Flock attributes
        """
        super(Flock, self).__init__(console, data)

    def __setattr__(self, key, value):
        """Override base class method

        :param key: Key of attribute
        :param value: Value of attribute
        """
        super(Flock, self).__setattr__(key, value)

    def __str__(self):
        """Helper method"""
        return "[Flock] name: {name}; flock_id: {flock_id}".format(
                    name=self.name, flock_id=self.flock_id)

    def rename(self, name):
        """Rename a Flock

        :param name: The new name to be used
        :return: A Result object
        :rtype: :class:`Result <Result>` object

        :except FlockError: Something went wrong while updating the Flock

        Usage::

            >>> import canarytools
            >>> flocks = console.flocks.all()
            >>> for flock in flocks:
            >>>     if flock.flock_id == 'flock:id_im_looking_to_rename':
            >>>         flock.rename("New name")
        """
        params = {'name': self.name, 'flock_id': self.flock_id}
        return self.console.post('flock/rename', params)


    def delete(self):
        """Delete a Flock

        :param flock_id: Unique identifier for your Flock
        :return: A Result object
        :rtype: :class:`Result <Result>` object

        :except FlockError: Something went wrong while deleting the Flock

        Usage::

            >>> import canarytools
            >>> result = console.flocks.delete(flock_id='flock:0bd349d8514a8256a0f1c8e6acf77cf0')
        """
        params = {'flock_id': self.flock_id}

        return self.console.post('flock/delete', params)
