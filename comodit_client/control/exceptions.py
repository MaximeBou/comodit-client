# control.exceptions - Exceptions for the application controllers.
# coding: utf-8
# 
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior 
# authorization from Guardis.

class ControllerException(Exception):  
    def __init__(self, message):
        self.msg = message

class ArgumentException(Exception):
    def __init__(self, message):
        self.msg = message

class NotFoundException(ArgumentException):
    pass

class MissingException(ArgumentException):
    pass

