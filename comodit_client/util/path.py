# path.py - Utility functions for filesystem and paths
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.
import os, platform

if platform.system() == 'Linux':
    import pwd, grp


def ensure(path):
    try:
        os.makedirs(path)
    except:
        pass


def chmod(path, mode):
    os.chmod(path, int(mode, 8))


def chown(path, owner, group):
    if platform.system() == 'Linux':
        owner_id = pwd.getpwnam(owner)[2]
        group_id = grp.getgrnam(group)[2]
        os.chown(path, owner_id, group_id)
