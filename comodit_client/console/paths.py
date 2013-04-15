# coding: utf-8

import items

from comodit_client.config import singleton


ROOT = (items.RootItem, '/')
ORGS = (items.OrganizationsItem, ROOT[1] + '/organizations')
ORG = (items.OrganizationItem, ORGS[1] + '/%org_name%')
GROUPS = (items.GroupsItem, ORG[1] + '/groups')
GROUP = (items.GroupItem, GROUPS[1] + '/%group_name%')
ENVS = (items.EnvironmentsItem, ORG[1] + '/environments')
ENV = (items.EnvironmentItem, ENVS[1] + '/%env_name%')
APPS = (items.ApplicationsItem, ORG[1] + '/applications')
APP = (items.ApplicationItem, APPS[1] + '/%app_name%')
DISTS = (items.DistributionsItem, ORG[1] + '/distributions')
DIST = (items.DistributionItem, DISTS[1] + '/%dist_name%')
PLATS = (items.PlatformsItem, ORG[1] + '/platforms')
PLAT = (items.PlatformItem, PLATS[1] + '/%plat_name%')
HOSTS = (items.HostsItem, ENV[1] + '/hosts')
HOST = (items.HostItem, HOSTS[1] + '/%host_name%')
HOST_APPS = (items.HostAppsItem, HOST[1] + '/applications')
HOST_APP = (items.HostAppItem, HOST_APPS[1] + '/%app_name%')
HOST_DIST = (items.HostDistItem, HOST[1] + '/distribution')
HOST_PLAT = (items.HostPlatItem, HOST[1] + '/platform')
HOST_INSTANCE = (items.HostInstanceItem, HOST[1] + '/instance')

HOST_CHANGES = (items.HostChangesItem, HOST[1] + '/changes')
HOST_CHANGE = (items.HostChangeItem, HOST_CHANGES[1] + '/%task_num%')

HOST_COMPLIANCES = (items.RootCompliancesItem, HOST[1] + '/compliances')
HOST_APP_COMPLIANCES = (items.HostAppCompliancesItem, HOST_COMPLIANCES[1] + '/%app_name%')
COMPLIANCES = (items.CompliancesItem, HOST_APP_COMPLIANCES[1] + '/%col_type%')
COMPLIANCE = (items.ComplianceItem, COMPLIANCES[1] + '/%comp_id%')

ORG_SETTINGS = (items.OrgSettingsItem, ORG[1] + '/settings')
ORG_SETTING = (items.OrgSettingItem, ORG[1] + '/settings/%key%')
ENV_SETTINGS = (items.EnvSettingsItem, ENV[1] + '/settings')
ENV_SETTING = (items.EnvSettingItem, ENV[1] + '/settings/%key%')
HOST_SETTINGS = (items.HostSettingsItem, HOST[1] + '/settings')
HOST_SETTING = (items.HostSettingItem, HOST[1] + '/settings/%key%')
DIST_SETTINGS = (items.DistSettingsItem, DIST[1] + '/settings')
DIST_SETTING = (items.DistSettingItem, DIST[1] + '/settings/%key%')
PLAT_SETTINGS = (items.PlatSettingsItem, PLAT[1] + '/settings')
PLAT_SETTING = (items.PlatSettingItem, PLAT[1] + '/settings/%key%')
HOST_APP_SETTINGS = (items.HostAppSettingsItem, HOST_APP[1] + '/settings')
HOST_APP_SETTING = (items.HostAppSettingItem, HOST_APP[1] + '/settings/%key%')
HOST_DIST_SETTINGS = (items.HostDistSettingsItem, HOST_DIST[1] + '/settings')
HOST_DIST_SETTING = (items.HostDistSettingItem, HOST_DIST[1] + '/settings/%key%')
HOST_PLAT_SETTINGS = (items.HostPlatSettingsItem, HOST_PLAT[1] + '/settings')
HOST_PLAT_SETTING = (items.HostPlatSettingItem, HOST_PLAT[1] + '/settings/%key%')

APP_PARAMETERS = (items.AppParamsItem, APP[1] + '/parameters')
APP_PARAMETER = (items.AppParamItem, APP[1] + '/parameters/%param_name%')
DIST_PARAMETERS = (items.DistParamsItem, DIST[1] + '/parameters')
DIST_PARAMETER = (items.DistParamItem, DIST[1] + '/parameters/%param_name%')
PLAT_PARAMETERS = (items.PlatParamsItem, PLAT[1] + '/parameters')
PLAT_PARAMETER = (items.PlatParamItem, PLAT[1] + '/parameters/%param_name%')

APP_FILES = (items.AppFilesItem, APP[1] + '/files')
APP_FILE = (items.AppFileItem, APP[1] + '/files/%file_name%')
DIST_FILES = (items.DistFilesItem, DIST[1] + '/files')
DIST_FILE = (items.DistFileItem, DIST[1] + '/files/%file_name%')
PLAT_FILES = (items.PlatFilesItem, PLAT[1] + '/files')
PLAT_FILE = (items.PlatFileItem, PLAT[1] + '/files/%file_name%')

HOST_APP_FILES = (items.HostAppFilesItem, HOST_APP[1] + '/files')
HOST_APP_FILE = (items.HostAppFileItem, HOST_APP[1] + '/files/%file_name%')
HOST_APP_PACKAGES = (items.HostAppPackagesItem, HOST_APP[1] + '/packages')
HOST_APP_PACKAGE = (items.HostAppPackageItem, HOST_APP[1] + '/packages/%pkg_name%')
HOST_APP_SERVICES = (items.HostAppServicesItem, HOST_APP[1] + '/services')
HOST_APP_SERVICE = (items.HostAppServiceItem, HOST_APP[1] + '/services/%svc_name%')
HOST_DIST_FILES = (items.HostDistFilesItem, HOST_DIST[1] + '/files')
HOST_DIST_FILE = (items.HostDistFileItem, HOST_DIST[1] + '/files/%file_name%')
HOST_PLAT_FILES = (items.HostPlatFilesItem, HOST_PLAT[1] + '/files')
HOST_PLAT_FILE = (items.HostPlatFileItem, HOST_PLAT[1] + '/files/%file_name%')

ORG_AUDITS = (items.OrgAudits, ORG[1] + '/audit')
ENV_AUDITS = (items.EnvAudits, ENV[1] + '/audit')
HOST_AUDITS = (items.HostAudits, HOST[1] + '/audit')

STORES = (items.Item, ROOT[1] + '/stores')
APP_STORE = (items.AppStoreItem, STORES[1] + '/applications')
PUB_APP = (items.PubAppItem, APP_STORE[1] + '/%pub_uuid%')
DIST_STORE = (items.DistStoreItem, STORES[1] + '/distributions')
PUB_DIST = (items.PubDistItem, DIST_STORE[1] + '/%pub_uuid%')


@singleton
class PathModel(object):

    def __init__(self):
        self._root = None

        self._register_path(*ROOT)
        self._register_path(*ORGS)
        self._register_path(*ORG)
        self._register_path(*GROUPS)
        self._register_path(*GROUP)
        self._register_path(*ENVS)
        self._register_path(*ENV)
        self._register_path(*APPS)
        self._register_path(*APP)
        self._register_path(*DISTS)
        self._register_path(*DIST)
        self._register_path(*PLATS)
        self._register_path(*PLAT)
        self._register_path(*HOSTS)
        self._register_path(*HOST)
        self._register_path(*HOST_APPS)
        self._register_path(*HOST_APP)
        self._register_path(*HOST_DIST)
        self._register_path(*HOST_PLAT)
        self._register_path(*HOST_INSTANCE)

        self._register_path(*HOST_CHANGES)
        self._register_path(*HOST_CHANGE)

        self._register_path(*HOST_COMPLIANCES)
        self._register_path(*HOST_APP_COMPLIANCES)
        self._register_path(*COMPLIANCES)
        self._register_path(*COMPLIANCE)

        self._register_path(*ORG_SETTINGS)
        self._register_path(*ORG_SETTING)
        self._register_path(*ENV_SETTINGS)
        self._register_path(*ENV_SETTING)
        self._register_path(*HOST_SETTINGS)
        self._register_path(*HOST_SETTING)
        self._register_path(*DIST_SETTINGS)
        self._register_path(*DIST_SETTING)
        self._register_path(*PLAT_SETTINGS)
        self._register_path(*PLAT_SETTING)
        self._register_path(*HOST_APP_SETTINGS)
        self._register_path(*HOST_APP_SETTING)
        self._register_path(*HOST_DIST_SETTINGS)
        self._register_path(*HOST_DIST_SETTING)
        self._register_path(*HOST_PLAT_SETTINGS)
        self._register_path(*HOST_PLAT_SETTING)

        self._register_path(*APP_PARAMETERS)
        self._register_path(*APP_PARAMETER)
        self._register_path(*DIST_PARAMETERS)
        self._register_path(*DIST_PARAMETER)
        self._register_path(*PLAT_PARAMETERS)
        self._register_path(*PLAT_PARAMETER)

        self._register_path(*APP_FILES)
        self._register_path(*APP_FILE)
        self._register_path(*DIST_FILES)
        self._register_path(*DIST_FILE)
        self._register_path(*PLAT_FILES)
        self._register_path(*PLAT_FILE)
        self._register_path(*HOST_APP_FILES)
        self._register_path(*HOST_APP_FILE)
        self._register_path(*HOST_APP_PACKAGES)
        self._register_path(*HOST_APP_PACKAGE)
        self._register_path(*HOST_APP_SERVICES)
        self._register_path(*HOST_APP_SERVICE)
        self._register_path(*HOST_DIST_FILES)
        self._register_path(*HOST_DIST_FILE)
        self._register_path(*HOST_PLAT_FILES)
        self._register_path(*HOST_PLAT_FILE)

        self._register_path(*ORG_AUDITS)
        self._register_path(*ENV_AUDITS)
        self._register_path(*HOST_AUDITS)

        self._register_path(*STORES)
        self._register_path(*APP_STORE)
        self._register_path(*PUB_APP)
        self._register_path(*DIST_STORE)
        self._register_path(*PUB_DIST)

    def _register_path(self, node_label, path):
        elems = path.strip().split('/')
        self._insert_node(elems, node_label)

    def create_node(self, node_label):
        return {'label': node_label, 'links': {}}

    def add_child(self, parent, link_label, leaf):
        parent['links'][link_label] = leaf

    def get_child(self, node, link_label):
        return node['links'].get(link_label)

    def is_wildcard(self, label):
        return len(label) > 2 and label[0] == '%' and label[-1] == '%'

    def get_static_child_leaves(self, node):
        labels = []
        for link in node['links']:
            if not self.has_children(node['links'][link]) and not self.is_wildcard(link):
                labels.append(link)
        return labels

    def get_static_child_subroots(self, node):
        labels = []
        for link in node['links']:
            if self.has_children(node['links'][link]) and not self.is_wildcard(link):
                labels.append(link)
        return labels

    def get_label(self, node):
        return node['label']

    def has_label(self, node):
        return node['label'] != None

    def has_children(self, node):
        return len(node['links']) > 0

    def set_label(self, node, label):
        node['label'] = label

    def _insert_node(self, elements, label):
        if self._root == None:
            self._root = self.create_node(None)

        current = self._root
        for elem in elements:
            if elem == '':
                continue
            child = self.get_child(current, elem)
            if child == None:
                child = self.create_node(None)
                self.add_child(current, elem, child)
            current = child

        if self.has_label(current):
            raise Exception('Node has already been labeled')

        self.set_label(current, label)

    def resolve(self, elements):
        resolved_vars = {}
        current_node = self._root
        for elem in elements:
            if elem == '':
                continue
            next_node = None
            for (label, node) in current_node['links'].iteritems():
                if len(label) > 2 and label[0] == '%' and label[-1] == '%':
                    resolved_vars[label[1:-1]] = elem
                    next_node = node
                    break
                elif elem == label:
                    next_node = node
                    break

            if next_node == None:
                raise Exception("Invalid path")

            current_node = next_node

        return (resolved_vars, current_node)


def change_with_elems(client, elements, opts):
    (resolved_vars, current_node) = PathModel().resolve(elements)
    abs_path = '/' + '/'.join(elements)

    item_class = PathModel().get_label(current_node)
    item_child_leaves = PathModel().get_static_child_leaves(current_node)
    item_child_subroots = PathModel().get_static_child_subroots(current_node)

    item = item_class(client, abs_path, item_child_subroots, item_child_leaves)
    item.set_path_vars(resolved_vars, opts)

    return item

def resolve_dots(elements):
    new_elems = []
    i = 0
    while i < len(elements):
        if elements[i] != '..' and elements[i] != '.':
            new_elems.append(elements[i])
            i += 1
        elif elements[i] == '.':
            i += 1
        else:
            num_of_ddot = 0
            while i < len(elements) and elements[i] == '..':
                num_of_ddot += 1
                i += 1

            for j in xrange(min(len(new_elems), num_of_ddot)):
                new_elems.pop()

    return new_elems


def absolute_elems(current, path):
    if not path.startswith('/'):
        path = current.absolute_path + '/' + path

    path = path.strip('/')
    if path == '':
        return []

    return resolve_dots(path.split('/'))


def change(current, args, opts):
    if len(args) < 1:
        return current

    try:
        return change_with_elems(current._client, absolute_elems(current, args[0]), opts)
    except Exception as e:
        raise Exception("Unable to change to item " + args[0] + ": " + str(e))
