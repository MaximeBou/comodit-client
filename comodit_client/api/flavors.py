# coding: utf-8
"""
Provides flavor entity (L{Flavor}) and collection (L{FlavorCollection}) classes.
"""

from comodit_client.api.entity import Entity
from comodit_client.api.collection import Collection
from comodit_client.api.parameters import Parameter


class FlavorCollection(Collection):
    """
    Flavors collection. This is a root collection.
    """

    def __init__(self, client):
        """
        Creates a new flavor collection.
        
        @param client: The client.
        @type client: L{Client}
        """

        super(FlavorCollection, self).__init__(client, "flavors/")

    def _new(self, json_data = None):
        res = Flavor(self, json_data)
        return res


class Flavor(Entity):
    """
    Flavor entity representation. This entity represents a distribution
    "type" and describes the settings that should be created in a distribution.
    Flavors are read-only entities.
    """

    @property
    def parameters_f(self):
        """
        The parameters of this flavor.

        @rtype: list of L{Parameter}
        """

        return self._get_list_field("parameters", lambda x: Parameter(None, x))

    def _show(self, indent = 0):
        print " "*indent, "Name:", self.name
        print " "*indent, "Parameters:"
        for p in self.parameters_f:
            p._show(indent + 2)
