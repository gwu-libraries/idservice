import arkpy
import arks_config as cfg
from idapp.models import ID

def generate_ark():
    ark = arkpy.mint(authority=cfg.auth_id, template=cfg.ark_template)
    return ark

def exists(ark):
    return ID.exists(ark)

def mint(quantity=1, owner=cfg.default_owner):
    arks = []
    for range(1, quantity):
        ark = generate_ark()
        while exists(ark):
            ark = generate_ark()
        ID.new(identifier=ark, owner=owner)
        arks.append(ark)
    return arks

def bind(ark, id_type='', path='', description='', owner=''):
    return ID.update(ark, id_type, path, description, owner)  

def lookup(ark):
    return ID.lookup(ark)

