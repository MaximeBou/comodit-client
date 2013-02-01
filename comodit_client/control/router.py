# control.router - Organize routers and dispatch request to router based on keyword.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from comodit_client.control.exceptions import ControllerException

controllers = {}

def register(keyword, controller):
    '''
    Adds the controller to the list of active controller and link it to the
    keywords provided.
    '''

    global controllers

    if isinstance(keyword, (list, tuple)):
        for k in keyword:
            controllers[k] = controller
    else:
        controllers[keyword] = controller

def dispatch(keyword, client, argv):
    '''
    Dispatch the request to the controller associated with the keyword. Raise an
    exception if no matching controller is found.
    '''

    global controllers
    if controllers.has_key(keyword):
        controllers[keyword].run(client, argv)
    else:
        raise ControllerException("Unknown entity '" + keyword + "'")

def print_keywords():
    global controllers
    for k in controllers.keys():
        print k
