class ActionDoc(object):
    def __init__(self, action, param_string, doc_string):
        self._action = action
        self._param_string = param_string
        self._doc_string = doc_string

    def get_action(self):
        return self._action

    def set_param_string(self, param_string):
        self._param_string = param_string

    def print_doc(self):
        print " "*2, self._action, self._param_string, self._doc_string
