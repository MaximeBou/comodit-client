# coding: utf-8

import completions

from comodit_client.control.entity import EntityController
from comodit_client.control.exceptions import ArgumentException

class AbstractParametersController(EntityController):

    _template = "parameter.json"

    def __init__(self):
        super(AbstractParametersController, self).__init__()

        self._doc = "Parameters handling."

    def get_collection(self, argv):
        res = self._get_owning_entity(argv)
        return res.parameters()

    def _print_entity_completions(self, param_num, argv):
        file_pos = self._get_parameter_position()
        if param_num < file_pos:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > file_pos - 1 and param_num == file_pos:
            res = self._get_owning_entity(argv)
            completions.print_identifiers(res.parameters())


class ApplicationParametersController(AbstractParametersController):

    def __init__(self):
        super(ApplicationParametersController, self).__init__()

        self._update_action_doc_params("list", "<org_name> <app_name>")
        self._update_action_doc_params("add", "<org_name> <app_name>")
        self._update_action_doc_params("delete", "<org_name>  <app_name> <param_name>")
        self._update_action_doc_params("update", "<org_name> <app_name> <param_name>")
        self._update_action_doc_params("show", "<org_name> <app_name> <param_name>")

    def _get_parameter_position(self):
        return 2

    def _get_name_argument(self, argv):
        if len(argv) < 3:
            raise ArgumentException("An organization, an application and a parameter name must be provided");
        return argv[2]

    def _get_owning_entity(self, argv):
        if len(argv) < 2:
            raise ArgumentException("An organization and an application name must be provided");

        return self._client.get_application(argv[0], argv[1])

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            completions.print_identifiers(self._client.organizations())
        elif len(argv) > 0 and param_num == 1:
            completions.print_identifiers(self._client.applications(argv[0]))


class DistributionParametersController(AbstractParametersController):

    def __init__(self):
        super(DistributionParametersController, self).__init__()

        self._update_action_doc_params("list", "<org_name> <dist_name>")
        self._update_action_doc_params("add", "<org_name> <dist_name>")
        self._update_action_doc_params("delete", "<org_name>  <dist_name> <param_name>")
        self._update_action_doc_params("update", "<org_name> <dist_name> <param_name>")
        self._update_action_doc_params("show", "<org_name> <dist_name> <param_name>")

    def _get_parameter_position(self):
        return 2

    def _get_name_argument(self, argv):
        if len(argv) < 3:
            raise ArgumentException("An organization, a distribution and a parameter name must be provided");
        return argv[2]

    def _get_owning_entity(self, argv):
        if len(argv) < 2:
            raise ArgumentException("An organization and a distribution name must be provided");

        return self._client.get_distribution(argv[0], argv[1])

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            completions.print_identifiers(self._client.organizations())
        elif len(argv) > 0 and param_num == 1:
            completions.print_identifiers(self._client.distributions(argv[0]))


class PlatformParametersController(AbstractParametersController):

    def __init__(self):
        super(PlatformParametersController, self).__init__()

        self._update_action_doc_params("list", "<org_name> <plat_name>")
        self._update_action_doc_params("add", "<org_name> <plat_name>")
        self._update_action_doc_params("delete", "<org_name>  <plat_name> <param_name>")
        self._update_action_doc_params("update", "<org_name> <plat_name> <param_name>")
        self._update_action_doc_params("show", "<org_name> <plat_name> <param_name>")

    def _get_parameter_position(self):
        return 2

    def _get_name_argument(self, argv):
        if len(argv) < 3:
            raise ArgumentException("An organization, a platform and a parameter must be provided");
        return argv[2]

    def _get_owning_entity(self, argv):
        if len(argv) < 2:
            raise ArgumentException("An organization and a platform name must be provided");

        return self._client.get_platform(argv[0], argv[1])

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            completions.print_identifiers(self._client.organizations())
        elif len(argv) > 0 and param_num == 1:
            completions.print_identifiers(self._client.platforms(argv[0]))
