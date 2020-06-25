import requests


from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from lxml import etree
from constants import URL_SEARCH, XPATH_URLS


class MedParse:
    __url_search = URL_SEARCH
    _xpath_urls = XPATH_URLS

    def __init__(self, region, area, search_str):
        self.__region = region
        self.__area = area
        self._search_str = search_str

    def __str__(self):
        return 'Class for parse med'

    def get_inform(self):
        # search_str - search string
        # sreg - city (region)
        # dist - district
        data = {
            'free_str': self._search_str,
            'sreg': self.__region,
            'dist': self.__area
        }
        response = self.request_with_retry('POST', self.__url_search, data)
        soup = BeautifulSoup(response, 'lxml')
        options = soup.select('option')
        if options:
            href = options[1]['value']
            url_next = urljoin(self.__url_search, href)
            response = self.request_with_retry('GET', request_url=url_next)
        results = self.get_data_from_table(response, data)
        return results

    def get_data_from_table(self, response, data):
        items = list()
        soup = BeautifulSoup(response, 'lxml')
        divs = soup.select('div.trow')
        for div in divs:
            div = str(div)
            tree = etree.XML(div)
            res = dict()
            for key, value in self._xpath_urls.items():
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

    def request_with_retry(self, method, request_url, data=None):
        session = requests.Session()

        session.mount('https://', HTTPAdapter(max_retries=5))

        if method == 'GET':
            return requests.get(
                url=request_url,
                timeout=1,
                allow_redirects=True).content.decode('utf-8')
        elif method == 'POST':
            return requests.post(
                url=request_url,
                timeout=1,
                allow_redirects=True,
                data=data).content.decode('utf-8')


if __name__ == '__main__':
    url = URL_SEARCH
    sreg = 78
    dist = 9
    search_str = 'парацетамол'
    med_parse = MedParse(sreg, dist, search_str)
    print(med_parse)
    print(med_parse.get_inform())
