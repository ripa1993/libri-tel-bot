import re
import urllib

from requests_html import HTMLSession, Element

result_selector = '#td-outer-wrap > div.td-main-content-wrap.td-container-wrap > div > div.td-pb-row > div.td-pb-span8.td-main-content > div > * > div > div.td-item-details > div.td-module-meta-info > h3 > a'
download_selector = 'div.td-post-content > #bf11 > strong > #url-shorthis'
download_xpath = '/html/body/div[7]/div[2]/div/div[2]/div[1]/div/article/div[3]/div[4]/p[7]/strong/a/button'
page_postfix = "?pag=2"
link_regex = 'https:\\/\\/libri\\.tel\\/wp-content\\/plugins\\/p-create-auto-post\\/index\\.php\\?url=([\\w\\d\\S]+)\\"'


class SearchResult:
    def __init__(self, url: str, name: str):
        self.url = url
        self.name = name

    def __repr__(self):
        return self.name + " @ " + self.url


def build_search_result(r: Element):
    attrs = r.attrs
    return SearchResult(attrs["href"], attrs["title"])


def get_download_link(s: SearchResult):
    session = HTMLSession()
    page = s.url + page_postfix
    r = session.get(page)
    match = re.search(link_regex, r.html.html)
    if match:
        link = match.groups()[0]
        return link
    else:
        return ""


def search(text):
    session = HTMLSession()
    search = urllib.parse.quote(text)
    search_results = session.get('https://libri.tel/?s=' + search)
    return [build_search_result(r) for r in search_results.html.find(result_selector)]


if __name__ == '__main__':
    session = HTMLSession()
    search_results = search("sherlock holmes")
    link = get_download_link(search_results[0])
