# coding: utf-8
"""
Provides classes related to purchased entities: L{PurchasedEntity} and
L{PurchasedCollection}.
"""

from comodit_client.api.collection import Collection
from comodit_client.api.entity import Entity


class PurchasedCollection(Collection):
    def _new(self, json_data = None):
        return PurchasedEntity(self, json_data)

    def new(self, pub_uuid, name):
        """
        Instantiates a new purchased entity.

        @param pub_uuid: The UUID of related published entity.
        @type pub_uuid: string
        @param name: The name the entity has inside purchasing organization.
        @type name: string
        @return: A purchased entity.
        @rtype: L{PurchasedEntity}
        """

        pur = self._new()
        pur.published = pub_uuid
        pur.name = name
        return pur

    def create(self, pub_uuid, name):
        """
        Creates a remote purchased entity and returns its local representation.

        @param pub_uuid: The UUID of related published entity.
        @type pub_uuid: string
        @param name: The name the entity has inside purchasing organization.
        @type name: string
        @return: A purchased entity.
        @rtype: L{PurchasedEntity}
        """

        pur = self.new(pub_uuid, name)
        pur.create()
        return pur


class PurchasedEntity(Entity):
    """
    A purchased entity represents the link between an organization's application
    or distribution and its related published entity.
    """

    @property
    def identifier(self):
        return self.uuid

    @property
    def label(self):
        return self.uuid + " - " + self.name

    @property
    def purchased_version(self):
        """
        The version of published entity at purchase time.

        @rtype: int
        """

        return self._get_field("purchasedVersion")

    @property
    def date_purchased(self):
        """
        The date the entity was purchased.

        @rtype: string
        """

        return self._get_field("datePurchased")

    @property
    def published(self):
        """
        The UUID of related published entity.
        """

        return self._get_field("published")

    @published.setter
    def published(self, uuid):
        """
        Sets the UUID of related published entity.
        """

        return self._set_field("published", uuid)
