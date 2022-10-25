from odoo.tests.common import BaseCase
from ..integration.converters import remove_empty_keys


class test_product_converter(BaseCase):

  def test_foo(self):
    a_dict = {
        'name': 'test',
        'code': None,
        'barcode': False,
        'options': {
            'weight': False,
            'sku': 'ABC123'
        }
    }

    clean_dict = remove_empty_keys(a_dict)

    self.assertEqual(clean_dict, {
        'name': 'test',
        'options': {'sku': 'ABC123'}
    })
