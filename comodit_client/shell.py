import code, sys

from api import Client

def connect(api, username, password):
    return Client(api, username, password)

sys.ps1 = '> '
sys.ps2 = '. '

console = code.interact(banner = "Welcome to ComodIT client shell!", local = locals())
