# coding: utf-8

import sys, argparse, traceback
import paths, completions

from bisect import insort

from comodit_client.util import prompt
from argparse import ArgumentError


# Generic super-classes

class Option(object):
    def __init__(self, short_opt, long_opt, doc = "", has_data = False):
        self._short = short_opt
        self._long = long_opt
        self._doc = doc
        self._has_data = has_data

    @property
    def short_opt(self):
        return self._short

    @property
    def long_opt(self):
        return self._long

    @property
    def has_value(self):
        return self._has_data

    @property
    def doc(self):
        return self._doc


class Command(object):
    def __init__(self, cmd, doc = ""):
        self._cmd = cmd
        self._options = []
        self._doc = doc

    @property
    def command(self):
        return self._cmd

    @property
    def options(self):
        return self._options

    def add_option(self, short_opt, long_opt, doc = "", has_data = False):
        self._options.append(Option(short_opt, long_opt, doc, has_data))

    @property
    def doc(self):
        return self._doc

    def call(self, current, opts, args):
        raise NotImplementedError()


# Actual commands

class List(Command):
    def __init__(self):
        super(List, self).__init__('ls', "Lists the content of target item")
        self.add_option('l', 'long', "Displays details related to each listed item")
        self.add_option('o', 'org', "Sets the organization name when listing a store", True)
        self.add_option('f', 'filter', "Sets the filter when listing a store; accepted values are public, featured and private", True)

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.list(opts)


class Show(Command):
    def __init__(self):
        super(Show, self).__init__('shw', "Displays target item")
        self.add_option('r', 'raw', "Displays data in their raw representation")
        self.add_option('o', 'org', "Sets the organization name when displaying a published entity", True)

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.show(opts)


class CurrentPath(Command):
    def __init__(self):
        super(CurrentPath, self).__init__('pwd', "Displays the absolute path to current item")

    def call(self, current, opts, args):
        print current.absolute_path


class ChangeDir(Command):
    def __init__(self):
        super(ChangeDir, self).__init__('cd', "Sets target item as current item")
        self.add_option('o', 'org', "Sets the organization name when accessing protected entities like privately published entities")

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        return target


class Add(Command):
    def __init__(self):
        super(Add, self).__init__('add', "Creates a new item in target container")
        self.add_option('r', 'raw', "Displays data in their raw representation")
        self.add_option('p', 'populate', "Populates newly created organization")
        self.add_option('d', 'default', "Pre-configures a newly created platform in function of selected driver")
        self.add_option('t', 'test', "Tests newly created platform, in particular provided credentials")
        self.add_option('f', 'flavor', "Provides the flavor of new distribution", True)

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.add(raw = opts.raw, populate = opts.populate, default = opts.default, test = opts.test, flavor = opts.flavor)


class Update(Command):
    def __init__(self):
        super(Update, self).__init__('upd', "Updates target item")

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.update()


class Delete(Command):
    def __init__(self):
        super(Delete, self).__init__('del', "Deletes target item")
        self.add_option('f', 'force', "Delete without without asking for a confirmation")

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)

        if opts.force or (prompt.confirm(prompt = "Delete target?", resp = False)) :
            target.delete()


class ShowFileContent(Command):
    def __init__(self):
        super(ShowFileContent, self).__init__('cat', "Shows a file's content")

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        if len(args) > 1:
            target.show_content(args[1])
        else:
            target.show_content()


class SetFileContent(Command):
    def __init__(self):
        super(SetFileContent, self).__init__('set', "Sets a file's content")

    def call(self, current, opts, args):
        if len(args) < 2:
            raise Exception("You must provide 2 arguments: a target and the path to a local file")

        target = paths.change(current, args, opts)
        target.set_content(args[1])


class StartInstance(Command):
    def __init__(self):
        super(StartInstance, self).__init__('strt', "Starts a host instance")

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.start()


class PauseInstance(Command):
    def __init__(self):
        super(PauseInstance, self).__init__('ps', "Pauses a host instance")

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.pause()


class ResumeInstance(Command):
    def __init__(self):
        super(ResumeInstance, self).__init__('rsm', "Resumes a host instance")

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.resume()


class ShutdownInstance(Command):
    def __init__(self):
        super(ShutdownInstance, self).__init__('shtd', "Shuts down a host instance")

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.shutdown()


class PoweroffInstance(Command):
    def __init__(self):
        super(PoweroffInstance, self).__init__('pwroff', "Powers off a host instance")

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.poweroff()


class ShowProperties(Command):
    def __init__(self):
        super(ShowProperties, self).__init__('prps', "Shows properties a host instance")

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.show_properties()


class Publish(Command):
    def __init__(self):
        super(Publish, self).__init__('pub', "Publishes an application or a distribution")
        self.add_option('o', 'orgs', "Provides a comma-separated list of authorized organizations; application or distribution is then privately published", True)

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.publish(opts)


class Unpublish(Command):
    def __init__(self):
        super(Unpublish, self).__init__('unpub', "Unpublishes an application or a distribution")

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.unpublish(opts)


class Purchase(Command):
    def __init__(self):
        super(Purchase, self).__init__('pur', "Purchases an application or a distribution from the store")
        self.add_option('o', 'org', "Provides the target organization name for purchased application or distribution", True)
        self.add_option('n', 'name', "Provides a name for purchased application or distribution", True)

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.purchase(opts)


class Export(Command):
    def __init__(self):
        super(Export, self).__init__('exp', "Exports an entity")
        self.add_option('f', 'force', "If option is provided, the content of the output folder will be overwritten")
        self.add_option('p', 'path', "Provides the path to output folder", True)

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.export(opts)


class Import(Command):
    def __init__(self):
        super(Import, self).__init__('imp', "Imports an entity")
        self.add_option('s', 'skip_conflicts', "Conflicting entities are skipped")
        self.add_option('d', 'dry_run', "Nothing is actually imported, actions queue is only displayed")
        self.add_option('p', 'path', "Provides the path to output folder", True)

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.import_entity(opts)


class SyncPull(Command):
    def __init__(self):
        super(SyncPull, self).__init__('sync-pull', "Pulls changes from a remote entity into a local folder")
        self.add_option('d', 'dry_run', "No change is actually executed")
        self.add_option('p', 'path', "Provides the path to local folder", True)

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.sync_pull(opts)


class SyncPush(Command):
    def __init__(self):
        super(SyncPush, self).__init__('sync-push', "Pushes changes from a local folder into a remote entity")
        self.add_option('d', 'dry_run', "No change is actually executed")
        self.add_option('p', 'path', "Provides the path to local folder", True)

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.sync_push(opts)


class StorePull(Command):
    def __init__(self):
        super(StorePull, self).__init__('store-pull', "Pulls changes from a published entity into its purchased copy")

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.store_pull(opts)


class StorePush(Command):
    def __init__(self):
        super(StorePush, self).__init__('store-push', "Pushes changes from a source entity into its published copy")

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.store_push(opts)


class LiveUpdate(Command):
    def __init__(self):
        super(LiveUpdate, self).__init__('live-update', "Updates a file on a host instance")

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.live_update(opts)


class LiveRestart(Command):
    def __init__(self):
        super(LiveRestart, self).__init__('live-restart', "Restarts a service on a host instance")

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.live_restart(opts)


class LiveInstall(Command):
    def __init__(self):
        super(LiveInstall, self).__init__('live-install', "(Re)-installs a package on a host instance")

    def call(self, current, opts, args):
        target = paths.change(current, args, opts)
        target.live_install(opts)


# Commands handling classes

class Help(Command):
    def __init__(self, cmds):
        super(Help, self).__init__('help', "Shows help")
        self._cmds = cmds

    def call(self, current, opts, args):
        self._cmds.print_help(args)


class Commands(object):
    def __init__(self, client):
        self._current = paths.change_with_elems(client, [], None)
        self._cmd_table = {}
        self._cmds = []
        self._parsers = {}
        self._debug = False

        self._register_command(List())
        self._register_command(Show())
        self._register_command(CurrentPath())
        self._register_command(ChangeDir())
        self._register_command(Add())
        self._register_command(Update())
        self._register_command(Delete())
        self._register_command(ShowFileContent())
        self._register_command(SetFileContent())
        self._register_command(StartInstance())
        self._register_command(PauseInstance())
        self._register_command(ResumeInstance())
        self._register_command(ShutdownInstance())
        self._register_command(PoweroffInstance())
        self._register_command(ShowProperties())
        self._register_command(Publish())
        self._register_command(Unpublish())
        self._register_command(Purchase())
        self._register_command(Export())
        self._register_command(Import())
        self._register_command(SyncPull())
        self._register_command(SyncPush())
        self._register_command(StorePull())
        self._register_command(StorePush())
        self._register_command(LiveUpdate())
        self._register_command(LiveRestart())
        self._register_command(LiveInstall())
        self._register_command(Help(self))

    def set_debug(self, flag):
        self._debug = flag

    def _register_command(self, cmd):
        insort(self._cmds, cmd.command)
        self._cmd_table[cmd.command] = cmd
        self._parsers[cmd.command] = self._get_parser(cmd.options)

    def get_commands(self):
        return self._cmds

    def get_options(self, cmd):
        entry = self._cmd_table.get(cmd)
        if entry == None:
            return []

        opts = []
        for opt in entry.options:
            if opt.short_opt != None:
                opts.append('-' + opt.short_opt)
            if opt.long_opt != None:
                opts.append('--' + opt.long_opt)
        return opts

    def has_value(self, cmd, opt):
        entry = self._cmd_table.get(cmd)
        if entry == None:
            return False

        for opt_ob in entry.options:
            if opt_ob.short_opt == opt or opt_ob.long_opt == opt:
                return opt_ob.has_value

        return False

    def _print_parser_error(self, msg):
        raise Exception(msg)

    def _get_parser(self, options):
        parser = argparse.ArgumentParser(usage = '')
        parser.error = self._print_parser_error

        for opt in options:
            opts = []
            opt_id = None
            if opt.short_opt != None:
                opts.append('-' + opt.short_opt)
                opt_id = opt.short_opt
            if opt.long_opt != None:
                opts.append('--' + opt.long_opt)
                opt_id = opt.long_opt

            kwargs = {'dest' : opt_id, 'help' : opt.doc}
            if not opt.has_value:
                kwargs['action'] = 'store_true'
                kwargs['default'] = False
            else:
                kwargs['default'] = None

            parser.add_argument(*opts, **kwargs)

        return parser

    def _parse_args(self, entry, args):
        parser = self._parsers[args[0]]
        if parser == None:
            return None, args

        opts, args = parser.parse_known_args(args)
        for a in args:
            if a.startswith('-'):
                raise Exception("Unsupported option " + a)
        return opts, args

    def print_help(self, args):
        if len(args) == 0:
            for cmd in self._cmds:
                self.print_cmd_help(cmd)
                print ""
        else:
            self.print_cmd_help(args[0])

    def print_cmd_help(self, cmd):
        entry = self._cmd_table.get(cmd)
        if entry == None:
            print "Unknown command '%s'" % cmd
            return

        print cmd, "-", entry.doc
        opts_help = self._parsers[cmd].format_help()

        # Filter help message generated by parser
        for line in opts_help.splitlines():
            if not line.startswith('usage:') and len(line) > 0 and not line.startswith('optional arguments:') and not ('-h, --help' in line):
                print line

    def prompt(self):
        return self._current.prompt()

    def get_completer(self):
        return completions.Completer(self, self._current)

    def call(self, args):
        entry = self._cmd_table.get(args[0])
        if entry == None:
            raise Exception("Unknown command '" + args[0] + "'")
        else:
            opts, args = self._parse_args(entry, args)
            try:
                next_it = entry.call(self._current, opts, args[1:])
                if next_it != None:
                    self._current = next_it
            except AttributeError as e:
                if self._debug:
                    traceback.print_tb(sys.exc_info()[2])
                    raise Exception(str(e))
                else:
                    raise Exception("Target does not support this command")
            except Exception as e:
                if self._debug:
                    traceback.print_tb(sys.exc_info()[2])
                raise e
