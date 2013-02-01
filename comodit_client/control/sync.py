# control.applications - Controller for comodit Applications entities.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from comodit_client.control.abstract import AbstractController
from comodit_client.control.doc import ActionDoc
from comodit_client.api.sync import SyncEngine
from comodit_client.control import completions
from comodit_client.control.exceptions import ArgumentException
from comodit_client.util import globals

class SyncController(AbstractController):

    def __init__(self, doc_params):
        super(SyncController, self).__init__()
        self._doc = "Sync."
        self._doc_params = doc_params

        self._register(["pull"], self._pull, self._print_sync_completions)
        self._register(["push"], self._push, self._print_sync_completions)
        self._register(["help"], self._help)
        self._default_action = self._help

        self._register_action_doc(self._pull_doc())
        self._register_action_doc(self._push_doc())

    def _print_sync_completions(self, argv):
        pass

    def _get_and_folder(self, argv):
        return (None, None)

    def _help(self, argv):
        self._print_doc()

    def _pull(self, argv):
        (remote_res, folder) = self._get_and_folder(argv)
        sync = SyncEngine(folder)

        sync.pull(remote_res, globals.options.dry_run)

    def _pull_doc(self):
        return ActionDoc("pull", self._doc_params, """
        Pulls changes from remote entity and updates local files.""")

    def _push(self, argv):
        (remote_res, folder) = self._get_and_folder(argv)
        sync = SyncEngine(folder)

        sync.push(remote_res, globals.options.dry_run)

    def _push_doc(self):
        return ActionDoc("push", self._doc_params, """
        Push changes from local entity to server.""")

class AppSyncController(SyncController):
    def __init__(self):
        super(AppSyncController, self).__init__("<org_name> <app_name> <local_folder>")

    def _print_sync_completions(self, param_num, argv):
        completions.app_sync_completions(self._client, param_num, argv)

    def _get_and_folder(self, argv):
        if len(argv) != 3:
            raise ArgumentException("Expected org name, app name and folder path")
        res = self._client.get_application(argv[0], argv[1])
        return (res, argv[2])

class DistSyncController(SyncController):
    def __init__(self):
        super(DistSyncController, self).__init__("<org_name> <dist_name> <local_folder>")

    def _print_sync_completions(self, param_num, argv):
        completions.dist_sync_completions(self._client, param_num, argv)

    def _get_and_folder(self, argv):
        if len(argv) != 3:
            raise ArgumentException("Expected org name, dist name and folder path")
        res = self._client.get_distribution(argv[0], argv[1])
        return (res, argv[2])
