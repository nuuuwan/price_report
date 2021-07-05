"""Implements cargills."""

from bs4 import BeautifulSoup

from utils import dt
from utils.browserx import Browser
from utils.cache import cache
from utils import tsv, timex

from price_report._constants import CACHE_NAME
from price_report._utils import log

SOURCE = 'cargills'


@cache(CACHE_NAME, timex.SECONDS_IN.HOUR)
def _scrape(product_name):
    url = 'https://cargillsonline.com/web/product?PS={product_name}'.format(
        product_name=product_name,
    )
    browser = Browser(url)
    html = browser.get_source()
    browser.quit()
    return html


def _parse_unit(unit_str):
    for unit_name0 in ['kg', 'g', 'ml', 'l', 'pcs']:
        if unit_name0 in unit_str:
            unit_name = unit_name0
            unit_str = unit_str.replace(unit_name0, '')
    units = (float)(unit_str)
    return unit_name, units


def _get_si_price(price, units, unit_name):
    if unit_name in ['kg', 'l']:
        return price / units
    if unit_name in ['g', 'ml']:
        return 1000 * price / units
    return price / units


def _get_subcategory(item_name):
    for subcats in [
        ['Suduru'],
        ['Samba'],
        ['Basmati'],
        ['Kuruluthuda'],
        ['Pachchaperumal'],
        ['Suwandel'],
        ['Nadu'],
        ['Kalu Heeneti', 'Kalu Heenati'],
        ['Ma Vee', 'Ma Wee'],

        ['Gram Dhal'],
        ['Wattana Dhal'],
        ['Dhal', 'Red Dhal'],

        ['Dried Fish'],
        ['Thalapath', 'Sword Fish Slices'],
        ['Tinned Fish', 'Tess Mackerel', 'Delmege Mackerel',
            'Classic Mackerel', 'My Choice Mackerel'],
    ]:
        for subcat in subcats:
            if subcat in item_name:
                return subcats[0]
    log.info('Unknown item: %s', item_name)
    return None


def _parse(html, product_name):
    date_id = timex.get_date_id()
    soup = BeautifulSoup(html, 'html.parser')
    price_list = []
    for div in soup.find_all('div', class_='cargillProdNeed'):
        p_titles = div.find_all('p')
        for p_title in p_titles:
            if ' - ' in p_title.text:
                item_name, unit = p_title.text.split(' - ')
                break
        h4_prices = div.find_all('h4')
        for h4_price in h4_prices:
            if 'Rs.' in h4_price.text:
                price = dt.parse_float(
                    h4_price.text.replace('Rs.', '').replace(',', ''),
                )
                break
        unit_name, units = _parse_unit(unit)
        subcategory = _get_subcategory(item_name)
        if subcategory:
            price_list.append({
                'date_id': date_id,
                'source': SOURCE,
                'item_name': item_name,
                'item_category': product_name,
                'item_subcategory': subcategory,
                'unit_name': unit_name,
                'units': units,
                'price': price,
                'price_per_si_unit': _get_si_price(price, units, unit_name),
            })

    data_file = '/tmp/price_list.%s.%s.tsv' % (product_name, date_id)
    tsv.write(data_file, price_list)
    log.info('Wrote {n_price_list} items to {data_file}'.format(
        n_price_list=len(price_list),
        data_file=data_file,
    ))


def _dump(product_name):
    html = _scrape(product_name)
    _parse(html, product_name)
