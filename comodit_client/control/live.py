# control.applications - Controller for comodit Applications entities.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

import completions

from comodit_client.control.abstract import AbstractController
from comodit_client.control.exceptions import ArgumentException
from comodit_client.control.doc import ActionDoc

class LiveController(AbstractController):

    def __init__(self):
        super(LiveController, self).__init__()
        self._doc = "Live management."

        self._register(["update-file"], self._update_file, self._print_file_completions)
        self._register(["restart-service"], self._restart_service, self._print_service_completions)
        self._register(["install-package"], self._install_package, self._print_package_completions)
        self._register(["help"], self._help)
        self._default_action = self._help

        self._register_action_doc(self._update_file_doc())
        self._register_action_doc(self._restart_service_doc())
        self._register_action_doc(self._install_package_doc())

    def _help(self, argv):
        self._print_doc()

    def _print_host_completions(self, param_num, argv):
        if param_num == 0:
            completions.print_entity_identifiers(self._client.organizations().list())
        elif len(argv) > 0 and param_num == 1:
            completions.print_entity_identifiers(self._client.environments(argv[0]).list())
        elif len(argv) > 1 and param_num == 2:
            completions.print_entity_identifiers(self._client.hosts(argv[0], argv[1]).list())
        elif len(argv) > 2 and param_num == 3:
            completions.print_entity_identifiers(self._client.get_host(argv[0], argv[1], argv[2]).applications())

    def _print_file_completions(self, param_num, argv):
        if param_num < 4:
            self._print_host_completions(param_num, argv)
        elif len(argv) > 3 and param_num == 4:
            app = self._client.get_application(argv[0], argv[3])
            for res in app.files_f:
                completions.print_escaped_string(res.name)

    def _print_service_completions(self, param_num, argv):
        if param_num < 4:
            self._print_host_completions(param_num, argv)
        elif len(argv) > 3 and param_num == 4:
            app = self._client.get_application(argv[0], argv[3])
            for res in app.services_f:
                completions.print_escaped_string(res.name)

    def _print_package_completions(self, param_num, argv):
        if param_num < 4:
            self._print_host_completions(param_num, argv)
        elif len(argv) > 3 and param_num == 4:
            app = self._client.get_application(argv[0], argv[3])
            for res in app.packages_f:
                completions.print_escaped_string(res.name)

    def _get_host(self, argv):
        return self._client.hosts(argv[0], argv[1]).get(argv[2])

    def _update_file(self, argv):
        if len(argv) < 4:
            raise ArgumentException("Wrong number of arguments")

        host = self._get_host(argv)
        app_name = argv[3]
        file_name = argv[4]
        host.live_update_file(app_name, file_name)

    def _update_file_doc(self):
        return ActionDoc("udpate-file", "<org_name> <env_name> <host_name> <app_name> <file_name>", """
        Updates file on given host.""")

    def _restart_service(self, argv):
        if len(argv) < 4:
            raise ArgumentException("Wrong number of arguments")

        host = self._get_host(argv)
        app_name = argv[3]
        svc_name = argv[4]
        host.live_restart_service(app_name, svc_name)

    def _restart_service_doc(self):
        return ActionDoc("restart-service", "<org_name> <env_name> <host_name> <app_name> <svc_name>", """
        Restarts service on given host.""")

    def _install_package(self, argv):
        if len(argv) < 4:
            raise ArgumentException("Wrong number of arguments")

        host = self._get_host(argv)
        app_name = argv[3]
        pkg_name = argv[4]
        host.live_install_package(app_name, pkg_name)

    def _install_package_doc(self):
        return ActionDoc("install-package", "<org_name> <env_name> <host_name> <app_name> <pkg_name>", """
        Install package on given host.""")
