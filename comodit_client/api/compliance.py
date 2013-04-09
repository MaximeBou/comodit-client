# coding: utf-8
"""
Provides classes related to compliance errors on provisioned hosts, in particular
L{ComplianceError} and L{ComplianceCollection}. Other classes describe the state
of an application resource:
  - service state (L{ServiceState})
  - file state (L{FileState})
  - package state (L{PackageState})
  - user state (L{UserState})
  - group state (L{GroupState})
  - repository state (L{RepositoryState})

@see: L{Application}
"""

from comodit_client.api.collection import Collection
from comodit_client.api.entity import Entity
from comodit_client.control.exceptions import ArgumentException
from comodit_client.util.json_wrapper import JsonWrapper


class State(JsonWrapper):
    """
    Base class of an application resource's state.
    """

    pass


class ServiceState(State):
    """
    State of a service.
    """

    @property
    def running(self):
        """
        Tells if the service is currently executed.

        @rtype: bool
        """

        return self._get_field("running")

    @property
    def enabled(self):
        """
        Tells if the service is currently enabled (i.e. will be executed on
        re-boot).

        @rtype: bool
        """

        return self._get_field("enabled")

    def show(self, indent = 0):
        """
        Prints a user-friendly representation of this state to standard output.

        @param indent: The number of spaces that will be put at the beginning
        of each printed line.
        @type indent: int
        """

        print " " * indent, "Running:", self.running
        print " " * indent, "Enabled:", self.enabled


class FileState(State):
    """
    State of a file.
    """

    @property
    def creation_time(self):
        """
        The creation time of the file. Date is formatted following the ISO 8601
        norm.

        @rtype: string
        """

        return self._get_field("creationTime")

    @property
    def group(self):
        """
        Group of the file.

        @rtype: string
        """

        return self._get_field("group")

    @property
    def mode(self):
        """
        Mode of the file (i.e. its permissions in the form of 3 or 4 octal digits).

        @rtype: string
        """

        return self._get_field("mode")

    @property
    def modification_time(self):
        """
        The modification time of the file. Date is formatted following the ISO 8601
        norm.

        @rtype: string
        """

        return self._get_field("modificationTime")

    @property
    def owner(self):
        """
        Owner of the file.

        @rtype: string
        """

        return self._get_field("owner")

    @property
    def path(self):
        """
        Path to the file.

        @rtype: string
        """

        return self._get_field("path")

    @property
    def present(self):
        """
        Tells whether the file is present on the system or not.

        @rtype: bool
        """

        return self._get_field("present")

    def show(self, indent = 0):
        """
        Prints a user-friendly representation of this state to standard output.

        @param indent: The number of spaces that will be put at the beginning
        of each printed line.
        @type indent: int
        """

        print " " * indent, "Present:", self.present
        if self.present:
            print " " * indent, "Creation time:", self.creation_time
            print " " * indent, "Modification time:", self.modification_time
            print " " * indent, "Owner:", self.owner
            print " " * indent, "Group:", self.group
            print " " * indent, "Mode:", self.mode


class PackageState(State):
    """
    State of a package.
    """

    @property
    def installed(self):
        """
        Tells whether the package is installed on the system or not.

        @rtype: bool
        """

        return self._get_field("installed")

    def show(self, indent = 0):
        """
        Prints a user-friendly representation of this state to standard output.

        @param indent: The number of spaces that will be put at the beginning
        of each printed line.
        @type indent: int
        """

        print " " * indent, "Installed:", self.installed


class UserState(State):
    """
    State of a user.
    """

    @property
    def present(self):
        """
        Tells whether the user is present on the system or not.

        @rtype: bool
        """

        return self._get_field("present")

    @property
    def gid(self):
        """
        The GID of the user.

        @rtype: string
        """

        return self._get_field("gid")

    @property
    def uid(self):
        """
        The UID of the user.

        @rtype: string
        """

        return self._get_field("uid")

    @property
    def name(self):
        """
        The username of the user.

        @rtype: string
        """

        return self._get_field("name")

    @property
    def home_dir(self):
        """
        The home directory of the user.

        @rtype: string
        """

        return self._get_field("dir")

    @property
    def shell(self):
        """
        The login shell of the user.

        @rtype: string
        """

        return self._get_field("shell")

    @property
    def gecos(self):
        """
        The GECOS of the user.

        @rtype: string
        """

        return self._get_field("gecos")

    @property
    def groups(self):
        """
        The groups the user belongs to.

        @rtype: list of string
        """

        return self._get_list_field("groups")

    def show(self, indent = 0):
        """
        Prints a user-friendly representation of this state to standard output.

        @param indent: The number of spaces that will be put at the beginning
        of each printed line.
        @type indent: int
        """

        print " " * indent, "Present:", self.present
        print " " * indent, "Name:", self.name
        print " " * indent, "GID:", self.gid
        print " " * indent, "UID:", self.uid
        print " " * indent, "Home directory:", self.home_dir
        print " " * indent, "Shell:", self.shell
        print " " * indent, "GECOS:", self.gecos
        print " " * indent, "Groups:", self.groups


class GroupState(State):
    """
    State of a group.
    """

    @property
    def present(self):
        """
        Tells whether the group is present on the system or not.

        @rtype: bool
        """

        return self._get_field("present")

    @property
    def name(self):
        """
        The group's name.

        @rtype: string
        """

        return self._get_field("name")

    @property
    def gid(self):
        """
        The group's GID.

        @rtype: string
        """

        return self._get_field("gid")

    def show(self, indent = 0):
        """
        Prints a user-friendly representation of this state to standard output.

        @param indent: The number of spaces that will be put at the beginning
        of each printed line.
        @type indent: int
        """

        print " " * indent, "Present:", self.present
        print " " * indent, "Name:", self.name
        print " " * indent, "GID:", self.gid


class RepositoryState(State):
    """
    State of a repository.
    """

    @property
    def present(self):
        """
        Tells whether the repository is present on the system or not.

        @rtype: bool
        """

        return self._get_field("present")

    @property
    def name(self):
        """
        The repository's name.

        @rtype: string
        """

        return self._get_field("name")

    @property
    def location(self):
        """
        The repository's location. This is generally a URL to an RPM repository
        or a DEB line.

        @rtype: string
        """

        return self._get_field("location")

    def show(self, indent = 0):
        """
        Prints a user-friendly representation of this state to standard output.

        @param indent: The number of spaces that will be put at the beginning
        of each printed line.
        @type indent: int
        """

        print " " * indent, "Present:", self.present
        print " " * indent, "Name:", self.name
        print " " * indent, "Location:", self.location


class ComplianceError(Entity):
    """
    Compliance error entity. A compliance error represents the fact that
    a system resource has diverged from what is defined in ComodIT by the
    applications (in fact, their entities) installed on a particular host.
    """

    def __init__(self, collection, json_data = None):
        super(ComplianceError, self).__init__(collection, json_data)
        if (json_data != None) and (json_data.has_key("type")):
            self._set_type_collection(json_data["type"])

    @property
    def application(self):
        """
        The application name.

        @rtype: string
        """

        return self._get_field("application")

    @property
    def resource_type(self):
        """
        Associated resource type (as provided by ComodIT). Possible values are
        serviceResource, fileResource, packageResource, userResource, groupResource,
        repoResource.

        @rtype: string
        """

        return self._get_field("type")

    def _set_type_collection(self, col):
        if col == "services":
            self._set_field("type", "serviceResource")
        elif col == "files":
            self._set_field("type", "fileResource")
        elif col == "packages":
            self._set_field("type", "packageResource")
        elif col == "users":
            self._set_field("type", "userResource")
        elif col == "groups":
            self._set_field("type", "groupResource")
        elif col == "repos":
            self._set_field("type", "repoResource")

    @property
    def type_collection(self):
        """
        Associated resource collection. Possible values are services, files,
        packages, users, groups or repos.

        @rtype: string
        """

        res_type = self.resource_type
        if res_type == "serviceResource":
            return "services"
        elif res_type == "fileResource":
            return "files"
        elif res_type == "packageResource":
            return "packages"
        elif res_type == "userResource":
            return "users"
        elif res_type == "groupResource":
            return "groups"
        elif res_type == "repoResource":
            return "repos"

    @property
    def res_name(self):
        """
        The resource's name.

        @rtype: string
        """

        return self._get_field("name")

    @property
    def identifier(self):
        return "applications/" + self.application + "/" + self.type_collection + "/" + self.res_name

    @property
    def current_state(self):
        """
        The resource's current state.

        @rtype: L{State}
        """

        return self._get_state("current")

    @property
    def expected_state(self):
        """
        The resource's expected state (as defined by ComodIT).

        @rtype: L{State}
        """

        return self._get_state("expected")

    def _get_state(self, state):
        if self.resource_type == "serviceResource":
            return ServiceState(self._get_field(state + "State"))
        elif self.resource_type == "fileResource":
            return FileState(self._get_field(state + "State"))
        elif self.resource_type == "packageResource":
            return PackageState(self._get_field(state + "State"))
        elif self.resource_type == "userResource":
            return UserState(self._get_field(state + "State"))
        elif self.resource_type == "groupResource":
            return GroupState(self._get_field(state + "State"))
        elif self.resource_type == "repoResource":
            return RepositoryState(self._get_field(state + "State"))
        else:
            return self._get_field("currentState")

    def _show(self, indent = 0):
        """
        Prints a user-friendly representation of this entity to standard output.

        @param indent: The number of spaces that will be put at the beginning
        of each printed line.
        @type indent: int
        """

        col = self.resource_type
        print " " * indent, "Type:", col
        print " " * indent, "Application:", self.application
        print " " * indent, "Name:", self.res_name

        print " " * indent, "Current state:"
        self.current_state.show(indent + 2)

        print " " * indent, "Expected state:"
        self.expected_state.show(indent + 2)


class ComplianceCollection(Collection):
    """
    Compliance errors collection. Errors may be fetched and removed but cannot
    be updated.
    """

    def _new(self, json_data = None):
        return ComplianceError(self, json_data)

    def __split_name(self, name):
        slash_index0 = name.find("/")
        slash_index1 = name.find("/", slash_index0 + 1)
        if slash_index1 == -1:
            raise ArgumentException("Wrong compliance error name, should be of the form applications/<app_name>/<type>/<id>")
        slash_index2 = name.find("/", slash_index1 + 1)
        if slash_index2 == -1:
            raise ArgumentException("Wrong compliance error name, should be of the form applications/<app_name>/<type>/<id>")
        return (name[slash_index0 + 1:slash_index1], name[slash_index1 + 1:slash_index2], name[slash_index2 + 1:])

    def get(self, identifier = "", parameters = {}):
        """
        Retrieves a particular compliance error of this collection.

        @param identifier: The identifier of the entity to retrieve. It
        must have the following form: 'applications/I{app_name}/I{collection}/I{id}'
        where I{app_name} is the name of an application installed on the host,
        I{collection} on of (services, files, packages, users, groups, repos)
        and I{id} the name of the application's resource.
        @type identifier: string
        @param parameters: Query parameters to send to ComodIT server.
        @type parameters: dict of strings

        @return: A compliance error representation.
        @rtype: L{ComplianceError}

        @raise EntityNotFoundException: If the entity was not found on the
        server.
        """

        (app_name, res_type, res_name) = self.__split_name(identifier)

        error = ComplianceError(self, {"application": app_name, "name":res_name, "type": res_type})
        error.refresh(parameters = parameters)
        return error
