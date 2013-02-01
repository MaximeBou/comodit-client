# path.py - Utility functions for filesystem and paths
# coding: utf-8
# 
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior 
# authorization from Guardis.
import os

def ensure(path):
    try:
        os.makedirs(path)
    except:
        pass