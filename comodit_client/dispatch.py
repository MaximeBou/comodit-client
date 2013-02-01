# dispatch.py - Command line dispatching for Cortex.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from control.applications import ApplicationsController
from control.platforms import PlatformsController
from control.distributions import DistributionsController
from control.environments import EnvironmentsController
from control.exceptions import ControllerException, ArgumentException
from control.hosts import HostsController
from control.organizations import OrganizationsController
from control.flavors import FlavorsController

from rest.exceptions import ApiException
from util import globals
from util.editor import NotModifiedException
import os
import argparse
import traceback
import sys
import textwrap
import control.router
from config import Config, ConfigException
from api import Client
from api.exceptions import PythonApiException
from comodit_client.api.importer import ImportException
from comodit_client.api.exporter import ExportException
from comodit_client.control.store import AppStoreController, DistStoreController

def run(argv):
    # entities
    control.router.register(["flavors"], FlavorsController())
    control.router.register(["platforms"], PlatformsController())
    control.router.register(["applications"], ApplicationsController())
    control.router.register(["distributions"], DistributionsController())
    control.router.register(["organizations"], OrganizationsController())
    control.router.register(["environments"], EnvironmentsController())
    control.router.register(["hosts"], HostsController())
    control.router.register(["app-store"], AppStoreController())
    control.router.register(["dist-store"], DistStoreController())

    _parse(argv)

def _get_all_options(parser):
    options = []
    for o in parser._option_string_actions:
        options.append(o)
    return options

def _get_value_options(parser):
    # TODO : automatically detect value options
    options = [
                "-f", "--file",
                "-j", "--json",
                "--api",
                "--user",
                "--pass",
                "--templates",
                "--profile",
                "--completions",
                "--org",
                "--flavor"
                ]
    return options


def __get_parser(config):
    parser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter,
                                     description = "This is the ComodIT CLI.",
                                     epilog = """\
For additional help on a particular collection, just call the client giving
as argument the entity and/or see man page.

Available entities:
    platforms         Underlying infrastructure platforms
    applications      Recipes to provision and configure applications on a
                      host
    distributions     Recipes to provision and configure distributions on a
                      host
    organizations     Top-level organization
    environments      Environment defined within an organization
    hosts             Host defined within an environment
    flavors           Available flavors when creating a distribution
""")

    parser.add_argument("entity", help = "An entity")
    parser.add_argument("subentities", help = "Optional subentities", nargs = "*")
    parser.add_argument("action", help = "An action to perform on given (sub)entity", nargs = "?")

    parser.add_argument("-f", "--file", dest = "filename", help = "input file with a JSON object")
    parser.add_argument("-j", "--json", dest = "json", help = "input JSON object via command line")
    parser.add_argument("-d", "--default", dest = "default", help = "let driver setup platform upon creation", action = "store_true", default = False)
    parser.add_argument("-t", "--test", dest = "test", help = "let driver test platform upon creation", action = "store_true", default = False)
    parser.add_argument("-p", "--populate", dest = "populate", help = "organization is populated at creation time", action = "store_true", default = False)
    parser.add_argument("--raw", dest = "raw", help = "output the raw JSON results", action = "store_true", default = False)
    parser.add_argument("--flavor", dest = "flavor", help = "provide distribution's flavor upon creation", default = None)

    parser.add_argument("--skip-chown", dest = "skip_chown", help = "Do not chown files on render tree", action = "store_true", default = False)
    parser.add_argument("--skip-chmod", dest = "skip_chmod", help = "Do not chmod files on render tree", action = "store_true", default = False)

    parser.add_argument("--skip-conflict", dest = "skip_conflict", help = "Skip conflicts on import", action = "store_true", default = False)
    parser.add_argument("--dry-run", dest = "dry_run", help = "Dry-run for import", action = "store_true", default = False)

    parser.add_argument("--public", dest = "public", help = "List only public apps/dists", action = "store_true", default = False)
    parser.add_argument("--private", dest = "private", help = "List only private apps/dists", action = "store_true", default = False)
    parser.add_argument("--featured", dest = "featured", help = "List only featured apps/dists", action = "store_true", default = False)
    parser.add_argument("--org", dest = "org_name", help = "Set organization", default = None)

    parser.add_argument("--api", dest = "api", help = "endpoint for the API", default = None)
    parser.add_argument("--user", dest = "username", help = "username on comodit server", default = None)
    parser.add_argument("--pass", dest = "password", help = "password on comodit server", default = None)
    parser.add_argument("--templates", dest = "templates_path", help = "directory containing JSON templates", default = config.templates_path)
    parser.add_argument("--profile", dest = "profile_name", help = "Name of profile to use", default = None)

    parser.add_argument("--force", dest = "force", help = "bypass change management and update everything", action = "store_true", default = False)
    parser.add_argument("--debug", dest = "debug", help = "display debug information", action = "store_true", default = False)
    parser.add_argument("--version", dest = "version", help = "display version information", action = "store_true", default = False)

    return parser


def _parse(argv):

    # Load configuration file
    try:
        config = Config()
    except ConfigException, e:
        print "Configuration error:"
        print e.msg
        exit(-1)

    # Create parser
    parser = __get_parser(config)

    # Check for completion related call
    if "--options" in argv:
        for o in _get_all_options(parser):
            print o
        exit(0)

    if "--options-with-value" in argv:
        for o in _get_value_options(parser):
            print o
        exit(0)

    try:
        completions_index = argv.index("--completions")
        del argv[completions_index]
        globals.param_completions = int(argv[completions_index])
        del argv[completions_index]

        if globals.param_completions == 0:
            control.router.print_keywords()
            exit(0)

        globals.param_completions -= 1
    except Exception:
        globals.param_completions = -1

    if "--version" in argv:
        version = "NO_VERSION"
        release = "NO_RELEASE"
        try:
            import version as version_mod
            if version_mod.VERSION:
                version = version_mod.VERSION
            if version_mod.RELEASE:
                release = version_mod.RELEASE
        except ImportError:
            pass
        print "ComodIT command line client " + version + "-" + release + "."
        exit(0)

    # Parse arguments
    globals.options = parser.parse_known_args(args = argv)[0]

    # Use profile data to configure server API connector. Options provided
    # on command-line have priority.
    if globals.options.api:
        api = globals.options.api
    else:
        api = config.get_api(globals.options.profile_name)
        globals.options.api = api

    if globals.options.username:
        username = globals.options.username
    else:
        username = config.get_username(globals.options.profile_name)
        globals.options.username = username

    if globals.options.password:
        password = globals.options.password
    else:
        password = config.get_password(globals.options.profile_name)
        globals.options.password = password

    client = Client(api, username, password)

    entity_args = [] + globals.options.subentities

    if not globals.options.action is None:
        entity_args.append(globals.options.action)

    _dispatch(globals.options.entity, entity_args, client)

def _dispatch(entity, args, client):
    options = globals.options

    try:
        control.router.dispatch(entity, client, args)
        exit(0)
    except ControllerException as e:
        print e.msg
    except ArgumentException as e:
        print e.msg
    except ApiException as e:
        print "Error (%s): %s" % (e.code, e.message)
    except PythonApiException as e:
        print e
    except ImportException as e:
        print e
    except ExportException as e:
        print e
    except NotModifiedException:
        print "Command was canceled since you did not save the file"
    except Exception:
        if options.debug:
            print "Exception in user code."
        else :
            print "Oops, it seems something went wrong (use --debug to learn more)."

    if options.debug:
        print '-' * 60
        traceback.print_exc(file = sys.stdout)
        print '-' * 60
    exit(-1)
