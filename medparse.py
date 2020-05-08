import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from lxml import etree
from constants import URL_SEARCH


def get_data_from_table(response, data):
    items = list()
    soup = BeautifulSoup(response, 'lxml')
    divs = soup.select('div.trow')
    xpath_urls = {
        'name': '//div[contains(@class, "name")]//text()',
        'country': '//div[contains(@class, "country")]//text()',
        'name_pharm': '//div[contains(@class, "pharm")]//text()',
        'address': '//div[contains(@class, "address")]/a/text()',
        'address_coord': '//div[contains(@class, "address")]/a/@href',
        'phone': '//div[contains(@class, "address")]/text()',
        'date': '//div[contains(@class, "date")]//text()',
        'pricefull': '//div[contains(@class, "pricefull")]//text()'
    }
    for div in divs:
        div = str(div)
        tree = etree.XML(div)
        res = dict()
        for key, value in xpath_urls.items():
            item = tree.xpath(value)
            if item:
                if len(item) > 1:
                    item = ''.join(item).replace(',', '').strip()
                    item = [item]
                res[key] = item[0]
        if res.keys():
            items.append(res)
    data['results'] = items
    return data


def get_inform(url: str, search_str: str, sreg: int, dist: int):
    # search_str - search string
    # sreg - city
    # dist - district
    data = {
        'free_str': search_str,
        'sreg': sreg,
        'dist': dist
    }
    response = requests.post(url, data, allow_redirects=True).content.decode('utf-8')
    soup = BeautifulSoup(response, 'lxml')
    options = soup.select('option')
    if options:
        href = options[1]['value']
        url_next = urljoin(url, href)
        response = requests.get(url_next).content.decode('utf-8')
    results = get_data_from_table(response, data)
    return results


if __name__ == '__main__':
    url = URL_SEARCH
    sreg = 78
    dist = 9
    search_str = 'парацетамол'
    results = get_inform(url=url, search_str=search_str, sreg=sreg, dist=dist)
    print(results)
