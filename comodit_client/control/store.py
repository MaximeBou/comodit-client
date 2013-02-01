import json, os, completions

from comodit_client.control.root_entity import RootEntityController
from comodit_client.control.exceptions import ArgumentException
from comodit_client.config import Config
from comodit_client.util.editor import edit_text
from comodit_client.util import globals

class StoreController(RootEntityController):

    def __init__(self):
        super(StoreController, self).__init__()

        self._template = "purchased_entity.json"

        self._unregister("add")
        self._unregister("update")
        self._unregister("delete")

        self._register("purchase", self._purchase, self._print_purchase_completions)

    def _get_filter(self):
        if globals.options.private:
            return "private"
        elif globals.options.featured:
            return "featured"
        else:
            return "public"

    def _get_filter_parameters(self):
        list_filter = self._get_filter()
        param = {"filter": list_filter}
        if globals.options.org_name:
            param["org_name"] = globals.options.org_name
        elif list_filter == "private":
            raise ArgumentException("An organization name must be provided with private filter")
        return param

    def _get_list_parameters(self, argv):
        return self._get_filter_parameters()

    def _print_entity_completions(self, param_num, argv):
        if param_num == 0:
            completions.print_identifiers(self.get_collection(argv), parameters = self._get_filter_parameters())

    def _get_show_parameters(self, argv):
        return self._get_filter_parameters()

    def _print_purchase_completions(self, param_num, argv):
        if param_num == 0:
            completions.print_identifiers(self.get_collection(argv), parameters = self._get_filter_parameters())
        elif param_num == 1:
            completions.print_identifiers(self._client.organizations())

    def _purchase(self, argv):
        if len(argv) < 2:
            raise ArgumentException("A published entity UUID and an organization name must be provided")

        org = self._client.organizations().get(argv[1])
        pub = self.get_collection(argv).get(argv[0], parameters = {"org_name" : argv[1]})

        template_json = json.load(open(os.path.join(Config()._get_templates_path(), self._template)))
        template_json["published"] = pub.uuid
        template_json["name"] = pub.name
        updated = edit_text(json.dumps(template_json, indent = 4))

        pur_app = self.get_purchased_collection(org)._new(json.loads(updated))
        pur_app.create()

class AppStoreController(StoreController):

    def __init__(self):
        super(AppStoreController, self).__init__()
        self._doc = "Application store handling."

    def get_collection(self, argv):
        return self._client.app_store()

    def get_purchased_collection(self, org):
        return org.purchased_apps()

class DistStoreController(StoreController):

    def __init__(self):
        super(DistStoreController, self).__init__()
        self._doc = "Distribution store handling."

    def get_collection(self, argv):
        return self._client.dist_store()

    def get_purchased_collection(self, org):
        return org.purchased_dists()
