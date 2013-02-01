# control.abstract - Parent class for all controllers. Implements basic flow usage.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

import re

from comodit_client.util import globals
from comodit_client.control.exceptions import ControllerException
from comodit_client.control.doc import ActionDoc

class AbstractController(object):
    '''The default (abstract) controller'''

    def __init__(self):
        self._actions = {}
        self._subcontrollers = {}
        self._completions = {}
        self._docs = {}
        self._register("__available_actions", self._available_actions)
        self._default_action = lambda x : self._error("No default action defined", -1)

    def run(self, client, argv):
        '''Execute the action (first argument in argv with other arguments) from this controller'''
        self._client = client
        self._pre(argv)

        param_num = globals.param_completions
        if param_num >= 0:
            if len(argv) == 0 or param_num == 0:
                self._available_actions()
            elif self._subcontrollers.has_key(argv[0]):
                globals.param_completions -= 1
                self._subcontrollers[argv[0]].run(client, argv[1:])
            elif self._completions.has_key(argv[0]):
                self._completions[argv[0]](param_num - 1, argv[1:])
        else:
            if len(argv) == 0:
                self._default_action(argv)
            else:
                action = argv[0]
                if self._actions.has_key(action):
                    self._actions[action](argv[1:])
                elif self._subcontrollers.has_key(action):
                    self._subcontrollers[action].run(client, argv[1:])
                else:
                    raise ControllerException("Unknown action or collection '" + action + "'")

        self._post(argv)
        self._client = None

    def _pre(self, argv):
        pass

    def _post(self, argv):
        pass

    def _error(self, message, code = -1):
        print(message)
        exit(code)

    def _register(self, action, command, print_complete = None):
        if isinstance(action, (list, tuple)):
            for a in action:
                self._actions[a] = command
                if print_complete:
                    self._completions[a] = print_complete
        else:
            self._actions[action] = command
            if print_complete:
                self._completions[action] = print_complete

    def _register_action_doc(self, doc):
        self._docs[doc.get_action()] = doc

    def _update_action_doc_params(self, action, params):
        self._docs[action].set_param_string(params)

    def _unregister(self, action):
        if isinstance(action, (list, tuple)):
            for a in action:
                if self._actions.has_key(a):
                    del self._actions[a]
                if self._completions.has_key(a):
                    del self._completions[a]
                if self._docs.has_key(a):
                    del self._docs[a]
        else:
            if self._actions.has_key(action):
                del self._actions[action]
            if self._completions.has_key(action):
                del self._completions[action]
            if self._docs.has_key(action):
                del self._docs[action]

    def _register_subcontroller(self, action, controller):
        if isinstance(action, (list, tuple)):
            for a in action:
                self._subcontrollers[a] = controller
        else:
            self._subcontrollers[action] = controller

    def _available_actions(self):
        for k in self._actions.keys():
            if k[0] != '_':
                print k
        for k in self._subcontrollers.keys():
            if k[0] != '_':
                print k

    def _print_doc(self):
        if self._doc:
            print self._doc
        print
        print "Available actions:"
        for doc in self._docs.values():
            doc.print_doc()
        print
        for (action, ctrl) in self._subcontrollers.items():
            doc = ActionDoc(action, "<...>", """
        """ + ctrl._doc)
            doc.print_doc()
