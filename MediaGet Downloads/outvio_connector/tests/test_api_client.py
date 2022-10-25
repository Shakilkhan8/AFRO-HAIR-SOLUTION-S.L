from unittest.mock import patch
from odoo.tests.common import SingleTransactionCase
import requests


class test_order_sending(SingleTransactionCase):

  partner_id = None

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    test_order_sending.partner_id = cls.env['res.partner'].create(
        vals_list={'name': 'John Smith'}).id

  def test_not_sent_when_draft(self):
    with patch('requests.post'):
      draft_order = self.env['sale.order'].create(
          {'partner_id': test_order_sending.partner_id})
      self.assertEqual('draft', draft_order.state)
      requests.post.assert_not_called()

  def test_sent_when_status_is_not_draft(self):
    order = self.env['sale.order'].create(
        {'partner_id': test_order_sending.partner_id})
    with patch('requests.post'):
      order.write({'state': 'sent'})
      self.assertEqual('sent', order.state)
      requests.post.assert_called_once()
