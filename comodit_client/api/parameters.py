# coding: utf-8
"""
Provides classes related to parameter entities, in particular L{HasParameters}.
"""

from comodit_client.api.entity import Entity
from comodit_client.api.collection import Collection


class ParameterCollection(Collection):
    """
    Collection of L{parameters<Parameter>}.
    """

    def _new(self, json_data = None):
        res = Parameter(self, json_data)
        return res

    def new(self, name, key, description = "", default_value = None):
        """
        Instantiates a new parameter representation.

        @param name: Parameter's name.
        @type name: string
        @param key: Parameter's key.
        @type key: string
        @param description: Parameter's description.
        @type description: string
        @param default_value: Parameter's default value.
        @type default_value: JSON object
        @return: A parameter representation.
        @rtype: L{Parameter}
        """

        p = self._new()
        p.name = name
        p.key = key
        p.description = description
        p.value = default_value
        return p

    def create(self, name, key, description = "", default_value = None):
        """
        Creates a new remote parameter entity and returns its local representation.

        @param name: Parameter's name.
        @type name: string
        @param key: Parameter's key.
        @type key: string
        @param description: Parameter's description.
        @type description: string
        @param default_value: Parameter's default value.
        @type default_value: JSON object
        @return: A parameter representation.
        @rtype: L{Parameter}
        """

        p = self.new(name, key, description, default_value)
        p.create()
        return p


class Parameter(Entity):
    """
    A parameter's representation.
    """

    @property
    def key(self):
        """
        Parameter's key.

        @rtype: String
        """

        return self._get_field("key")

    @key.setter
    def key(self, key):
        """
        Sets parameter's key.

        @param key: The key
        @type key: string
        """

        self._set_field("key", key)

    @property
    def value(self):
        """
        Parameter's default value.

        @rtype: JSON object
        """

        return self._get_field("value")

    @value.setter
    def value(self, value):
        """
        Sets parameter's default value.

        @param value: The default value
        @type value: JSON object
        """

        return self._set_field("value", value)

    def _show(self, indent = 0):
        print " "*indent, "Name:", self.name
        print " "*indent, "Description:", self.description
        print " "*indent, "Key:", self.key
        print " "*indent, "Default value:", self.value


class HasParameters(Entity):
    """
    Super class for entities having parameters.
    """

    def parameters(self):
        """
        Instantiates a collection of parameters.

        @rtype: L{ParameterCollection}
        """

        return ParameterCollection(self.client, self.url + "parameters/")

    def get_parameter(self, name):
        """
        Fetches a parameter given its name.
        
        @param name: Parameter's name.
        @type name: string
        @return: Requested parameter.
        @rtype: L{Parameter}
        """

        return self.parameters().get(name)

    def add_parameter(self, parameter):
        """
        Adds a parameter to local list of parameters. Note that this list is considered only at creation time.
        For later parameter modifications, collection must be used.

        @param parameter: the parameter to add.
        @type parameter: L{Parameter}
        """

        self._add_to_list_field("parameters", parameter)

    @property
    def parameters_f(self):
        """
        The local list of parameters. The object of the list may be used to interact
        with the server.

        @rtype: list of L{Parameter}
        """

        return self._get_list_field("parameters", lambda x: Parameter(self.parameters(), x))

    @parameters_f.setter
    def parameters_f(self, params):
        """
        Sets the local list of parameters. Note that this list is considered only at creation time.
        For later parameter modifications, collection must be used.

        @param params: The new list of parameters.
        @type params: list of L{Parameter}
        """

        self._set_list_field("parameters", params)

    def _show_parameters(self, indent = 0):
        print " "*indent, "Parameters:"
        for s in self.parameters_f:
            s._show(indent + 2)
