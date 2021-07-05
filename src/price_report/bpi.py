"""Bath packet index."""

from price_report.cargills import _load

BPI_RICE_G = 200
BPI_DHAL = 50
BPI_MACKEREL_G = 85


def _get_cheapest(product_name, date_id, item_subcategory=None):
    data_list = _load(product_name, date_id)
    if item_subcategory:
        data_list = list(filter(
            lambda d: d['item_subcategory'] == item_subcategory,
            data_list,
        ))
    data_list = sorted(data_list, key=lambda d: d['price_per_si_unit'])
    return data_list[0]


def _compute_index(date_id):
    rice = _get_cheapest('rice', date_id, 'Samba')
    dhal = _get_cheapest('dhal', date_id)
    mackerel = _get_cheapest('mackerel', date_id)

    bpi_price = (float)(rice['price_per_si_unit']) * BPI_RICE_G / 1000 \
        + (float)(dhal['price_per_si_unit']) * BPI_DHAL / 1000 \
        + (float)(mackerel['price_per_si_unit']) * BPI_MACKEREL_G / 1000

    return {
        'rice': rice,
        'dhal': dhal,
        'mackerel': mackerel,
        'bpi_price': bpi_price,
    }


if __name__ == '__main__':
    print(_compute_index('20210705'))
