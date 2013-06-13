# control.applications - Controller for comodit Applications entities.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

import completions

from comodit_client.control.exceptions import ArgumentException
from comodit_client.control.entity import EntityController
from comodit_client.control.doc import ActionDoc

class MonitoringAlertController(EntityController):

    def __init__(self):
        super(MonitoringAlertController, self).__init__()
        self._doc = "Host alerts handling."
        self._str_empty = "No alerts raised on this host at the moment."

        self._unregister("add")
        self._unregister("update")
        self._unregister("delete")
        self._unregister("show")

        self._register(["clear"], self._clear, self._print_collection_completions)
        self._register_action_doc(self._clear_doc())

        self._update_action_doc_params("list", "<org_name> <env_name> <host_name>")

    def get_collection(self, argv):
        if len(argv) < 3:
            raise ArgumentException("Wrong number of arguments");
        return self._client.get_host(argv[0], argv[1], argv[2]).get_instance().alerts()

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            completions.print_identifiers(self._client.organizations())
        elif len(argv) > 0 and param_num == 1:
            completions.print_identifiers(self._client.environments(argv[0]))
        elif len(argv) > 1 and param_num == 2:
            completions.print_identifiers(self._client.hosts(argv[0], argv[1]))

    def _print_entity_completions(self, param_num, argv):
        if param_num < 3:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > 2 and param_num == 3:
            alerts = self._client.get_host(argv[0], argv[1], argv[2]).alerts().list()
            for c in alerts:
                completions.print_escaped_string(c.identifier)

    def _get_name_argument(self, argv):
        if len(argv) < 4:
            raise ArgumentException("An organization, environment, host and timestamp must be provided");
        return argv[3]

    def _clear(self, argv):
        alerts = self.get_collection(argv)
        alerts.clear()

    def _clear_doc(self):
        return ActionDoc("clear", "<org_name> <env_name> <host_name>", """
        Clear all monitoring alerts.""")
