# control.organizations - Controller for comodit Organizations entities.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

import json, completions

from comodit_client.util import globals
from comodit_client.control.root_entity import RootEntityController
from comodit_client.control.exceptions import ArgumentException
from comodit_client.control.settings import OrganizationSettingsController
from comodit_client.control.groups import GroupsController
from comodit_client.control.doc import ActionDoc
from comodit_client.control.audit import AuditHelper
from comodit_client.api.exporter import Export
from comodit_client.api.importer import Import


class OrganizationsController(RootEntityController):

    _template = "organization.json"

    def __init__(self):
        super(OrganizationsController, self).__init__()
        self._audit = AuditHelper(self, "<res_name>")

        # actions
        self._register(["import"], self._import, self._print_import_completions)
        self._register(["export"], self._export, self._print_export_completions)
        self._register(["reset-secret"], self._reset_secret, self._print_entity_completions)
        self._register(["audit"], self._audit.audit, self._print_entity_completions)
        self._register_action_doc(self._audit.audit_doc())

        self._register_action_doc(self._export_doc())
        self._register_action_doc(self._import_doc())
        self._register_action_doc(self._reset_secret_doc())
        self._register_action_doc(self._audit.audit_doc())

        # subcontrollers
        self._register_subcontroller(["settings"], OrganizationSettingsController())
        self._register_subcontroller(["groups"], GroupsController())

        self._doc = "Organizations handling."

    def get_collection(self, argv):
        return self._client.organizations()

    def _prune_json_update(self, json_wrapper):
        super(OrganizationsController, self)._prune_json_update(json_wrapper)
        json_wrapper._del_field("settings")
        json_wrapper._del_field("groups")
        json_wrapper._del_field("environments")

    def _reset_secret(self, argv):
        org = self._get_entity(argv)
        org.reset_secret()

    def _reset_secret_doc(self):
        return ActionDoc("reset-secret", self._list_params(), """
        Resets the secret key associated to the organization.""")

    # Import/export

    def __set_root_folder(self, argv):
        if len(argv) < 1:
            raise ArgumentException("Wrong number of arguments")

        self._root = argv[0]  # By default, use organization name as folder name
        if len(argv) > 1:
            self._root = argv[1]

    def _print_export_completions(self, param_num, argv):
        if param_num == 0:
            self._print_entity_completions(param_num, argv)
        elif param_num == 1:
            completions.print_dir_completions()

    def _export(self, argv):
        self._options = globals.options

        self.__set_root_folder(argv)

        org = self._client.get_organization(argv[0])
        export = Export(globals.options.force)
        export.export_organization(org, self._root)

    def _export_doc(self):
        return ActionDoc("export", "<org_name> [<output_folder>] [--force]", """
        Export organization onto disk. --force option causes existing files to
        be overwritten.""")

    def _print_import_completions(self, param_num, argv):
        if param_num == 0:
            completions.print_dir_completions()

    def _import(self, argv):
        """
        Pushes local data to comodit server. Data may include applications,
        distributions, platforms, organizations, environments and hosts.
        Local data are automatically imported if no collision with remote data
        is detected. In case of collision, 'force' option can be used to still
        import data.
        """
        self._options = globals.options

        if len(argv) < 1:
            raise ArgumentException("Wrong number of arguments")
        self._root = argv[0]

        importer = Import(globals.options.skip_conflict, True)
        importer.import_organization(self._client, self._root)

        if (importer.no_conflict() or globals.options.skip_conflict) and not globals.options.dry_run:
            importer.execute_queue()
        else:
            importer.display_queue(show_only_conflicts = True)

    def _import_doc(self):
        return ActionDoc("import", "<src_folder>] [--skip-conflict] [--dry-run]", """
        Import organization from disk. With --skip-conflict, conflicting actions
        are skipped. With --dry-run, actions are displayed but not applied.""")
