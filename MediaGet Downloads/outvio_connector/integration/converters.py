from itertools import filterfalse


def order_to_json(order, invoicing_addr, delivery_addr, payment, description_by_order_line_id):
  shipping_product_id = None
  if order.carrier_id:
    shipping_product_id = order.carrier_id.product_id.id

  def is_shipping_line(ol):
    return ol.product_id.id == shipping_product_id

  shipping_lines = list(filter(is_shipping_line, order.order_line))
  product_lines = filterfalse(is_shipping_line, order.order_line)
  products = [order_line_to_product(p, description_by_order_line_id) for p in product_lines]

  shipping = {}
  if shipping_lines:
    # I assume there can be only one shipping
    shipping['method'] = shipping_lines[0].name
    shipping['price'] = shipping_lines[0].price_total

  order_json = {
      'id': order.name,
      'client': {
          'invoicing': invoicing_addr,
          'delivery': delivery_addr
      },
      'currency': order.currency_id.name,
      'dateTime': order.create_date.isoformat() + 'Z',
      'state': order.state,
      'products': products,
      'total': order.amount_total,
      'tax': order.amount_tax,
      'shipping': shipping
  }

  if payment:
    order_json['payment'] = payment

  return order_json


def order_line_to_product(order_line, description_by_order_line_id):
  product = {
      'name': order_line.name,
      'price': order_line.price_total,
      'quantity': order_line.product_uom_qty,
      'vat': order_line.price_tax,
      'sku': order_line.product_id.default_code
  }
  if description_by_order_line_id[order_line.id]:
    product['description'] = description_by_order_line_id[order_line.id]

  optional_fields = {
      'barcode': order_line.product_id.barcode,
      'weight': order_line.product_id.weight
  }

  for k in optional_fields:
    if optional_fields[k]:
      product[k] = optional_fields[k]

  return remove_empty_keys(product)


def partner_to_address(partner):
  if not partner:
    return {}

  address = partner.street
  if partner.street2:
    address = '%s %s' % (address, partner.street2)

  address = {
      'postcode': partner.zip,
      'countryCode': partner.country_id.code,
      'city': partner.city,
      'address': address,
      'name': partner.name,
      'email': partner.email,
      'phone': partner.mobile or partner.phone
  }

  if partner.state_id:
    address['state'] = partner.state_id.name

  return address


def remove_empty_keys(a_dict):
  res = {}
  for k, v in a_dict.items():
    if isinstance(v, dict):
      res[k] = remove_empty_keys(v)
    elif v:
      res[k] = v
  return res
