# coding: utf-8
"""
Provides the importer tool. The importer can be used to importer entities
from local directories into a ComodIT server.
"""

import os, json

from comodit_client.api.application import Application
from comodit_client.api.collection import EntityNotFoundException
from comodit_client.api.distribution import Distribution
from comodit_client.api.platform import Platform
from comodit_client.api.environment import Environment
from comodit_client.api.host import Host, Instance
from comodit_client.api.contexts import ApplicationContext, PlatformContext, \
    DistributionContext
from comodit_client.api.organization import Organization
from comodit_client.api.exceptions import PythonApiException


class ImportException(Exception):
    """
    Exception raised by importer in case of error.
    """

    pass


class Import(object):
    """
    The importer is a tool that enables to import entities from local
    directories. Imported entities have generally been exported (see L{Export}).
    """

    def __init__(self, skip_conflict = False, queue_actions = False):
        """
        Creates an importer instance. When importing entities, there might be
        conflicts with existing remote entities. In this case, import fails unless
        'skip conflicts' flag is set (conflicting entities are not imported).
        This is not a synchronization tool, see L{sync tool<SyncEngine>} for
        this feature.

        The importer can queue actions before executing them on import. This
        allows to audit the actions before actually applying them. It also
        enabled to detect conflicts.

        @param skip_conflict: If true, sets 'skip conflicts' flag.
        @type skip_conflict: bool
        @param queue_actions: If true, enabled queuing mode.
        @type queue_actions: bool
        """

        self._skip_conflict = skip_conflict
        self._queue_actions = queue_actions
        if queue_actions:
            self._actions_queue = ActionsQueue()

    def _import_entity(self, local_res, entity_type = "entity"):
        res_name = local_res.name

        # Retrieve remote entity (if it exists)
        collection = local_res.collection
        try:
            collection.get(res_name)
            if not self._skip_conflict and not self._queue_actions:
                raise ImportException("There is a conflict for " + entity_type + " '" + res_name + "'")
            elif self._queue_actions:
                self._actions_queue.add_action(CreateEntity(True, local_res, entity_type))
            return True
        except EntityNotFoundException:
            if self._queue_actions:
                self._actions_queue.add_action(CreateEntity(False, local_res, entity_type))
            else:
                local_res.create()
            return False

    def _import_instance(self, instance):
        try:
            instance.collection.get()
        except PythonApiException:
            if self._queue_actions:
                self._actions_queue.add_action(CreateEntity(False, instance, "host instance"))
            else:
                instance.create()

    def _import_file_content(self, conflict, src_file, app, name, entity_type = "entity"):
        if self._queue_actions:
            self._actions_queue.add_action(UploadContent(conflict, src_file, app, name, entity_type))
        else:
            app.files().get(name).set_content(src_file)

    def _import_thumbnail(self, conflict, src_file, app, entity_type = "entity"):
        if self._queue_actions:
            self._actions_queue.add_action(UploadThumb(conflict, src_file, app, entity_type))
        else:
            app.set_thumbnail_content(src_file)

    def _import_entity_with_files(self, res, root_folder, entity_type = "entity"):
        res.load(root_folder)

        conflict = self._import_entity(res, entity_type)

        # Push files' content
        file_list = res.files_f
        for f in file_list:
            file_name = f.name
            content_file = os.path.join(root_folder, "files", file_name)
            self._import_file_content(conflict, content_file, res, file_name, entity_type)

        if os.path.exists(os.path.join(root_folder, "thumb")):
            thumb_file = os.path.join(root_folder, "thumb")
            self._import_thumbnail(conflict, thumb_file, res, entity_type)

    def import_application(self, org, root_folder):
        """
        Imports an application from a local folder into a given organization.

        @param org: The target organization.
        @type org: L{Organization}
        @param root_folder: Path to directory containing application's definition.
        @type root_folder: string
        """

        app = Application(org.applications(), None)
        self._import_entity_with_files(app, root_folder, "application")

    def import_distribution(self, org, root_folder):
        """
        Imports a distribution from a local folder into a given organization.

        @param org: The target organization.
        @type org: L{Organization}
        @param root_folder: Path to directory containing distribution's definition.
        @type root_folder: string
        """

        dist = Distribution(org.distributions(), None)
        self._import_entity_with_files(dist, root_folder, "distribution")

    def import_platform(self, org, root_folder):
        """
        Imports a platform from a local folder into a given organization.

        @param org: The target organization.
        @type org: L{Organization}
        @param root_folder: Path to directory containing platform's definition.
        @type root_folder: string
        """

        plat = Platform(org.platforms(), None)
        self._import_entity_with_files(plat, root_folder, "platform")

    def import_environment(self, org, env_folder):
        """
        Imports an environment from a local folder into a given organization.

        @param org: The target organization.
        @type org: L{Organization}
        @param env_folder: Path to directory containing environment's definition.
        @type env_folder: string
        """

        env = Environment(org.environments(), None)
        env.load(env_folder)
        self._import_entity(env, "environment")

        # Push hosts
        hosts_folder = os.path.join(env_folder, "hosts")
        if os.path.exists(hosts_folder):
            hosts_list = os.listdir(hosts_folder)
            for host_name in hosts_list:
                host_folder = os.path.join(hosts_folder, host_name)

                self.import_host(env, host_folder)

    def import_host(self, env, host_folder):
        """
        Imports a host from a local folder into a given environment.

        @param env: The target environment.
        @type env: L{Environment}
        @param host_folder: Path to directory containing host's definition.
        @type host_folder: string
        """

        host = Host(env.hosts(), None)
        host.load(host_folder)

        apps = host.application_names

        # Contexts are created below
        host._del_field("applications")
        host._del_field("platform")
        host._del_field("distribution")

        self._import_entity(host, "host")

        # Import application contexts
        for app in apps:
            context = ApplicationContext(host.applications(), None)
            context.load_json(os.path.join(host_folder, "applications", app + ".json"))
            self._import_entity(context, "application context")

        # Import platform context
        platform_file = os.path.join(host_folder, "platform.json")
        if os.path.exists(platform_file):
            context = PlatformContext(host.platform(), None)
            context.load_json(platform_file)
            self._import_entity(context, "platform context")

        # Import distribution context
        dist_file = os.path.join(host_folder, "distribution.json")
        if os.path.exists(dist_file):
            context = DistributionContext(host.distribution(), None)
            context.load_json(dist_file)
            self._import_entity(context, "distribution context")

        # Import instance (must come at last)
        instance_file = os.path.join(host_folder, "instance.json")
        if os.path.exists(instance_file):
            instance = Instance(host.instance(), None)
            instance.load_json(instance_file)
            self._import_instance(instance)

    def import_organization(self, client, org_folder):
        """
        Imports an organization from a local folder.

        @param client: The client.
        @type client: L{Client}
        @param org_folder: Path to directory containing organization's definition.
        @type org_folder: string
        """

        org = Organization(client.organizations(), None)
        org.load(org_folder)

        self._import_entity(org, "organization")

        apps_folder = os.path.join(org_folder, "applications")
        if os.path.exists(apps_folder):
            for app in os.listdir(apps_folder):
                self.import_application(org, os.path.join(apps_folder, app))

        dists_folder = os.path.join(org_folder, "distributions")
        if os.path.exists(dists_folder):
            for dist in os.listdir(dists_folder):
                self.import_distribution(org, os.path.join(dists_folder, dist))

        plats_folder = os.path.join(org_folder, "platforms")
        if os.path.exists(plats_folder):
            for plat in os.listdir(plats_folder):
                self.import_platform(org, os.path.join(plats_folder, plat))

        envs_folder = os.path.join(org_folder, "environments")
        if os.path.exists(envs_folder):
            for env in os.listdir(envs_folder):
                self.import_environment(org, os.path.join(envs_folder, env))

    def display_queue(self, show_only_conflicts = True):
        """
        If queuing was enabled, displays the queued actions to standard output.
        This method must be called after a call to one of the C{import_*} methods.
        """

        if not self._queue_actions:
            raise ImportException("Queueing is not enabled")

        self._actions_queue.display_actions(show_only_conflicts)

    def execute_queue(self):
        """
        If queuing was enabled, executes the queued actions to standard output.
        This method must be called after a call to one of the C{import_*} methods.
        """

        if not self._queue_actions:
            raise ImportException("Queueing is not enabled")

        self._actions_queue.apply_actions(self._skip_conflict)

    def no_conflict(self):
        """
        If queuing was enabled, tells if a conflict was detected.
        This method must be called after a call to one of the C{import_*} methods.

        @return: True if a conflict was detected, false otherwise.
        @rtype: bool
        """

        if not self._queue_actions:
            raise ImportException("Queueing is not enabled")

        return self._actions_queue.no_conflict()


class Action(object):
    """
    An import action.
    """

    def __init__(self, conflict):
        """
        Creates a new action instance.

        @param conflict: True if this actions is conflicting.
        @type conflict: bool
        """

        self._conflict = conflict

    def conflict(self):
        """
        Tells if the action is conflicting.

        @return: True if the action is conflicting, false otherwise.
        @rtype: bool
        """

        return self._conflict

    def execute(self):
        """
        Executes this action.
        """

        raise NotImplementedError

    def get_summary(self):
        """
        Provides a description of this action.
        
        @return: A description of this action.
        @rtype: string
        """

        raise NotImplementedError

    def display(self):
        """
        Displays this actions to standard output.
        """

        print "Conflict:", self._conflict
        print "Summary: " + self.get_summary()


class UploadContent(Action):
    """
    File-upload action.
    """

    def __init__(self, conflict, src_file, res, file_name, entity_type = "entity"):
        """
        Creates a new file-upload action instance.

        @param conflict: True if the action is conflicting, false otherwise.
        @type conflict: bool
        @param src_file: Path to local file to upload.
        @type src_file: string
        @param file_name: Name of the remote file.
        @type file_name: string
        @param entity_type: Entity type.
        @type entity_type: string
        """

        super(UploadContent, self).__init__(conflict)
        self._src_file = src_file
        self._res = res
        self._entity_type = entity_type
        self._file_name = file_name

    def get_summary(self):
        return "Upload file " + self._src_file + " to " + self._entity_type + " '" + self._res.name + "'"

    def execute(self):
        file_res = self._res.get_file(self._file_name)
        file_res.set_content(self._src_file)


class UploadThumb(Action):
    """
    Thumbnail-upload action.
    """

    def __init__(self, conflict, src_file, res, entity_type = "entity"):
        """
        Creates a new thumbnail-upload action instance.

        @param conflict: True if the action is conflicting, false otherwise.
        @type conflict: bool
        @param src_file: Path to local file to upload.
        @type src_file: string
        @param entity_type: Entity type.
        @type entity_type: string
        """

        super(UploadThumb, self).__init__(conflict)
        self._src_file = src_file
        self._res = res
        self._entity_type = entity_type

    def get_summary(self):
        return "Upload thumbnail to " + self._entity_type + " '" + self._res.name + "'"

    def execute(self):
        self._res.set_thumbnail_content(self._src_file)


class CreateEntity(Action):
    """
    Entity creation action.
    """

    def __init__(self, conflict, res_object, entity_type):
        """
        Creates a new create-entity action instance.

        @param conflict: True if the action is conflicting, false otherwise.
        @type conflict: bool
        @param res_object: The entity to create.
        @type res_object: L{Entity}
        @param entity_type: Entity type.
        @type entity_type: string
        """

        super(CreateEntity, self).__init__(conflict)
        self._res_object = res_object
        self._entity_type = entity_type

    def execute(self):
        self._res_object.create()

    def get_summary(self):
        return "Create " + self._entity_type + " '" + self._res_object.name + "'"


class ActionsQueue:
    """
    The queue of actions.
    """

    def __init__(self):
        """
        Creates a new queue of actions.
        """

        self._no_conflict = True
        self._actions = []

    def add_action(self, action):
        """
        Adds an action to the queue.
        
        @param action: The action to queue.
        @type action: L{Action}
        """

        if action.conflict():
            self._no_conflict = False
        self._actions.append(action)

    def no_conflict(self):
        """
        Tells if the queue contains a conflicting action.

        @return: True if the queue contains conflicting actions, false otherwise.
        @rtype: bool
        """

        return self._no_conflict

    def apply_actions(self, skip_conflicts):
        """
        Applies queued actions.

        @param skip_conflicts: If true, conflicting actions are not applied.
        @type skip_conflicts: bool
        """

        if not self._no_conflict and not skip_conflicts:
            raise ImportException("Cannot apply actions, conflicts detected")

        for a in self._actions:
            print "-"*80
            if not a.conflict():
                print "Executing '" + a.get_summary() + "'"
                try:
                    a.execute()
                except Exception as e:
                    print "Error:", str(e)
            else:
                print "Skipping '" + a.get_summary() + "'"
        print "-"*80

    def display_actions(self, show_only_conflicts):
        """
        Displays queued actions.

        @param show_only_conflicts: If true, only conflicting actions are displayed.
        @type show_only_conflicts: bool
        """

        for a in self._actions:
            if not show_only_conflicts or a.conflict():
                print "-"*80
                a.display()
        print "-"*80
