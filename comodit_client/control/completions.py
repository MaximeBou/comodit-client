import re

#
# Utility functions
#

def __match_replacement(match):
        return "\\" + match.group(0)

def print_file_completions():
    exit(1)

def print_dir_completions():
    exit(2)

def print_escaped_string(name):
    if name is None:
        return
    name = re.sub(r'[ \\ ()<>\']', __match_replacement, name)
    print name.encode("utf-8")

def print_escaped_strings(name_list):
    for name in name_list:
        print_escaped_string(name)

def print_escaped_names(res_list):
        for r in res_list:
            print_escaped_string(r.name)

def print_entity_identifiers(res_list):
        for r in res_list:
            print_escaped_string(r.identifier)

def print_identifiers(collection):
    print_entity_identifiers(collection.list())

#
# Entity specific functions
#

def org_completions(client, param_num, argv):
    if param_num == 0:
        print_identifiers(client.organizations())

def app_completions(client, param_num, argv):
    if param_num == 0:
        org_completions(client, param_num, argv)
    elif param_num == 1 and len(argv) > 0:
        print_identifiers(client.applications(argv[0]))

def dist_completions(client, param_num, argv):
    if param_num == 0:
        org_completions(client, param_num, argv)
    elif param_num == 1 and len(argv) > 0:
        print_identifiers(client.distributions(argv[0]))

def app_sync_completions(client, param_num, argv):
    if param_num == 0:
        org_completions(client, param_num, argv)
    elif param_num == 1:
        app_completions(client, param_num, argv)
    elif param_num == 2:
        print_dir_completions()

def dist_sync_completions(client, param_num, argv):
    if param_num == 0:
        org_completions(client, param_num, argv)
    elif param_num == 1:
        dist_completions(client, param_num, argv)
    elif param_num == 2:
        print_dir_completions()
