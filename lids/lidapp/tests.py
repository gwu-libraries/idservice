from django.utils import unittest
from lidapp.models import Requester, Minter, ID
from datetime import datetime
import re

class MintTestCase(unittest.TestCase):
    def setUp(self):
        
        self.minter = Minter.objects.create(name='gwark',authority_number='38989',
                                            prefix='c01',template='eeddeeddk',
                                            minter_type='a',date_created=str(datetime.now()),
                                            description='Our primary minter')
        self.requester = Requester.objects.create(name='Gelman',organization='GWU',
                                                  date_created=str(datetime.now()),
                                                  description='Primary user')
        ark_hex = 'bcdfghjkmnpqrstvwxyz0-9'
        ark_pattern = '38989/c01['+ark_hex+']{2}[0-9]{2}['+ark_hex+']{2}[0-9]{2}['+ark_hex+']'
        self.regex = re.compile(ark_pattern)

    def test_mint_one(self):
        ids = ID.mint(requester_name=self.requester.name, minter_name=self.minter.name, quantity=1)
        self.one_id = ids[0]
        self.assertTrue(self.regex.match(self.one_id))
    
    def test_mint_many(self):
        ids = ID.mint(requester_name=self.requester.name, minter_name=self.minter.name, quantity=12)
        for id in ids:
            self.assertTrue(self.regex.match(id))

class BindTestCase(unittest.TestCase):
    def setUp(self):
        ids = ID.mint(requester_name='Gelman', minter_name='gwark', quantity=1)
        self.one_id = ids[0]        

    def test_bind(self):
        bound_id = ID.bind(identifier=self.one_id, object_type='i',
                           object_url='digital.library.gwu.edu/item/'+self.one_id,
                           description='Our first object!')
        self.assertEqual(bound_id.identifier, self.one_id)
        self.assertEqual(bound_id.requester_name, self.requester.name)
        self.assertEqual(bound_id.requester_ip, '127.0.0.1')
        self.assertEqual(bound_id.id_type, self.minter.minter_type)
        self.assertEqual(bound_id.object_type, 'i')
        self.assertEqual(bound_id.object_url, 'digital.library.gwu.edu/item/'+self.one_id)
        self.assertEqual(bound_id.description, 'Our first object!')
class LookupTestCase(unittest.TestCase):
    def setUp(self):
        ids = ID.mint(requester_name='Gelman', minter_name='gwark', quantity=1)
        self.one_id = ids[0]
        bound_id = ID.bind(identifier=self.one_id, object_type='i',
                           object_url='digital.library.gwu.edu/item/'+self.one_id,
                           description='Our first object!')
        
    def test_lookup(self):
        lookup_id = ID.lookup(identifier=self.one_id)
        self.assertEqual(lookup_id.identifier, self.one_id)
        self.assertEqual(lookup_id.requester_name, self.requester.name)
        self.assertEqual(lookup_id.requester_ip, '127.0.0.1')
        self.assertEqual(lookup_id.id_type, self.minter.minter_type)
        self.assertEqual(lookup_id.object_type, 'i')
        self.assertEqual(lookup_id.object_url, 'digital.library.gwu.edu/item/'+self.one_id)
        self.assertEqual(lookup_id.description, 'Our first object!')
    
