# coding: utf-8
"""
Provides classes related to stores, in particular L{PublishedEntity}.
"""

from comodit_client.api.collection import Collection
from comodit_client.api.entity import Entity


class AppStoreCollection(Collection):
    """
    Collection of published applications. This is a root collection.
    """

    def __init__(self, client):
        super(AppStoreCollection, self).__init__(client, "store/applications/")

    def _new(self, json_data = None):
        return PublishedApplication(self, json_data)

    def new(self, app_uuid, authorized_orgs = None):
        """
        Instantiates a new published application representation.

        @param app_uuid: The UUID of the application to publish.
        @type app_uuid: string
        @param authorized_orgs: The list of organizations that have access to
        this application. If left None or empty, application is public.
        @type authorized_orgs: list of string
        @return: New published application.
        @rtype: L{PublishedApplication}
        """

        app = self._new()
        app.application = app_uuid
        app.authorized = authorized_orgs
        return app

    def create(self, app_uuid, authorized_orgs = None):
        """
        Creates a remote published application and returns its representation.

        @param app_uuid: The UUID of the application to publish.
        @type app_uuid: string
        @param authorized_orgs: The list of organizations that have access to
        this application. If left None or empty, application is public.
        @type authorized_orgs: list of string
        @return: New published application.
        @rtype: L{PublishedApplication}
        """

        app = self.new(app_uuid, authorized_orgs)
        app.create()
        return app

    def get(self, identifier = "", parameters = {}, org_name = None):
        """
        Fetches a published application. Giving an organization name can give
        access to published applications with restricted access.

        @return: Fetched published application.
        @rtype: L{PublishedApplication}
        """

        if org_name:
            parameters["org_name"] = org_name
        return super(AppStoreCollection, self).get(identifier, parameters)


class DistStoreCollection(Collection):
    def __init__(self, client):
        super(DistStoreCollection, self).__init__(client, "store/distributions/")

    def _new(self, json_data = None):
        return PublishedDistribution(self, json_data)

    def new(self, dist_uuid, authorized_orgs = None):
        """
        Instantiates a new published distribution representation.

        @param dist_uuid: The UUID of the distribution to publish.
        @type dist_uuid: string
        @param authorized_orgs: The list of organizations that have access to
        this distribution. If left None or empty, distribution is public.
        @type authorized_orgs: list of string
        @return: New published distribution.
        @rtype: L{PublishedDistribution}
        """

        dist = self._new()
        dist.distribution = dist_uuid
        dist.authorized = authorized_orgs
        return dist

    def create(self, dist_uuid, authorized_orgs = None):
        """
        Creates a remote published distribution and returns its representation.

        @param dist_uuid: The UUID of the distribution to publish.
        @type dist_uuid: string
        @param authorized_orgs: The list of organizations that have access to
        this distribution. If left None or empty, distribution is public.
        @type authorized_orgs: list of string
        @return: New published distribution.
        @rtype: L{PublishedDistribution}
        """

        dist = self.new(dist_uuid, authorized_orgs)
        dist.create()
        return dist

    def get(self, identifier = "", parameters = {}, org_name = None):
        """
        Fetches a published distribution. Giving an organization name can give
        access to published distributions with restricted access.

        @return: Fetched published distribution.
        @rtype: L{PublishedDistribution}
        """

        if org_name:
            parameters["org_name"] = org_name
        return super(DistStoreCollection, self).get(identifier, parameters)


class PublishedEntity(Entity):
    """
    Base class for published entities.
    """

    @property
    def identifier(self):
        return self.uuid

    @property
    def label(self):
        return self.uuid + " - " + self.name

    @property
    def publisher_summary(self):
        """
        Informations about the user that published the entity.

        @rtype: string
        """

        return self._get_field("publisherSummary")

    @property
    def publishing_organization(self):
        """
        Contact information of publishing organization.

        @rtype: JSON object
        """

        return self._get_field("publishingOrganization")

    @property
    def date_published(self):
        """
        Date the entity was published on.

        @rtype: string
        """

        return self._get_field("datePublished")

    @property
    def date_updated(self):
        """
        Date the entity was last updated.

        @rtype: string
        """

        return self._get_field("dateUpdated")

    @property
    def authorized(self):
        """
        The list of organizations having access to published application.

        @rtype: list of string
        """

        return self._get_field("authorized")

    @authorized.setter
    def authorized(self, org_names):
        """
        Sets the list of organizations having access to published application.

        @param org_names: The new list of organizations having access to published application.
        @type org_names: list of string
        """

        return self._set_field("authorized", org_names)

    @property
    def url_f(self):
        """
        URL to published entity's web site.

        @rtype: string
        """

        return self._get_field("url")

    @property
    def documentation(self):
        """
        Published entity's documentation.

        @rtype: string
        """

        return self._get_field("documentation")

    @property
    def license(self):
        """
        Published entity's license text.

        @rtype: string
        """

        return self._get_field("license")

    @property
    def price(self):
        """
        Published entity's price.

        @rtype: string
        """

        return self._get_field("price")

    @property
    def featured(self):
        """
        Tells if published entity is featured or not.

        @rtype: bool
        """

        return self._get_field("isFeatured")

    def _show(self, indent = 0):
        super(PublishedEntity, self)._show(indent)
        print " "*indent, "Published:", self.date_published
        print " "*indent, "Last update:", self.date_updated
        print " "*indent, "URL:", self.url_f
        print " "*indent, "Documentation:", self.documentation
        print " "*indent, "License:", self.license
        print " "*indent, "Price:", self.price
        print " "*indent, "Featured:", self.featured


class PublishedApplication(PublishedEntity):
    """
    Published application representation.
    """

    @property
    def application(self):
        """
        The UUID of the original application.
        """

        return self._get_field("application")

    @application.setter
    def application(self, uuid):
        """
        Sets the UUID of the original application.
        """

        return self._set_field("application", uuid)


class PublishedDistribution(PublishedEntity):
    """
    Published distribution representation.
    """

    @property
    def distribution(self):
        """
        The UUID of the original distribution.
        """

        return self._get_field("distribution")

    @distribution.setter
    def distribution(self, uuid):
        """
        Sets the UUID of the original distribution.
        """

        return self._set_field("distribution", uuid)


class IsStoreCapable(Entity):
    """
    Base class for all entities that are publishable/purchasable.
    """

    @property
    def published_as(self):
        """
        If the entity has been published, gives the UUID of published
        entity.

        @see: L{PublishedEntity}
        """

        return self._get_field("publishedAs")

    @property
    def purchased_as(self):
        """
        If the entity has been purchased, gives the UUID of purchased
        entity.

        @see: L{PurchasedEntity}
        """

        return self._get_field("purchasedAs")

    @property
    def can_pull(self):
        """
        If the entity has been purchased, tells if changes may be pulled
        from the store i.e. published entity has been updated and this
        entity is therefore obsolete.
        """

        return self._get_field("canPull")

    @property
    def can_push(self):
        """
        If the entity has been published, tells if changes may be pushed
        to the store i.e. entity has been updated and published
        entity is therefore obsolete.
        """

        return self._get_field("canPush")

    @property
    def url_f(self):
        """
        URL to entity's WEB site.

        @rtype: string
        """

        return self._get_field("url")

    @url_f.setter
    def url_f(self, url):
        """
        Sets the URL to entity's WEB site.

        @param url: The URL to application's WEB site.
        @type url: string
        """

        self._set_field("url", url)

    @property
    def documentation(self):
        """
        Entity's documentation.

        @rtype: string
        """

        return self._get_field("documentation")

    @documentation.setter
    def documentation(self, documentation):
        """
        Sets entity's documentation.

        @param documentation: The documentation of the entity.
        @type documentation: string
        """

        self._set_field("documentation", documentation)

    @property
    def license(self):
        """
        Entity's license.

        @rtype: string
        """

        return self._get_field("license")

    @license.setter
    def license(self, license_text):
        """
        Sets entity's license.

        @param license_text: The license of the entity.
        @type license_text: string
        """

        return self._set_field("license", license_text)

    @property
    def price(self):
        """
        Entity's price.

        @rtype: string
        """

        return self._get_field("price")

    @price.setter
    def price(self, price):
        """
        Sets entity's price.

        @param price: The price of the entity.
        @type price: string
        """

        return self._set_field("price", price)

    def get_thumbnail_content(self):
        """
        Fetches the thumbnail of the entity.

        @return: a reader to file's content.
        @rtype: file-like object
        """

        return self._http_client.read(self.url + "thumb", decode = False)

    def set_thumbnail_content(self, path):
        """
        Uploads the content of the thumbnail.

        @param path: Path to local thumbnail file.
        @type path: string
        """

        self._http_client.upload_to_exising_file_with_path(path, self.url + "thumb")

    def _show_store_fields(self, indent = 0):
        is_purchased = not self.purchased_as is None
        print " "*indent, "Purchased: " + str(is_purchased),
        if is_purchased:
            print "(can pull: " + str(self.can_pull) + ")"
        else:
            print

        is_published = not self.published_as is None
        print " "*indent, "Published: " + str(is_published),
        if is_published:
            print "(can push: " + str(self.can_push) + ")"
        else:
            print

        print " "*indent, "Url: %s" % self.url_f
        print " "*indent, "Documentation:\n%s" % self.documentation
        print " "*indent, "License:\n%s" % self.license
        print " "*indent, "Price: %s" % self.price
