# coding: utf-8

from comodit_client.control.root_entity import RootEntityController

class FlavorsController(RootEntityController):

    _template = "user.json"

    def __init__(self):
        super(FlavorsController, self).__init__()

        self._doc = "Flavors handling."

        self._unregister("add")
        self._unregister("update")
        self._unregister("delete")

    def get_collection(self, argv):
        return self._client.flavors()
