# coding: utf-8

import completions

from comodit_client.control.entity import EntityController
from comodit_client.control.exceptions import ArgumentException

class GroupsController(EntityController):

    def __init__(self):
        super(GroupsController, self).__init__()

        # Unregister unsupported actions
        self._unregister(["add", "delete"])

        self._doc = "Groups handling."

    def get_collection(self, argv):
        if len(argv) < 1:
            raise ArgumentException("Wrong number of arguments");

        return self._client.get_organization(argv[0]).groups()

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            completions.print_identifiers(self._client.organizations())

    def _print_entity_completions(self, param_num, argv):
        if param_num == 0:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > 0 and param_num == 1:
            completions.print_identifiers(self.get_collection(argv))

    def _get_name_argument(self, argv):
        if len(argv) < 2:
            raise ArgumentException("An organization name and a group name must be provided")
        return argv[1]
