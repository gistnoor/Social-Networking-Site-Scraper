import scrapy
import pdb
from scrapy import Selector
from socialNetwork.items import SocialnetworkItem
import lxml.html as HTML

class SocialNetworkSpider(scrapy.Spider):
    name = "social"
    allowed_domains = ["wikipedia.org"]
    start_urls = [
            "https://en.wikipedia.org/wiki/List_of_social_networking_websites"
            ]
    
    def parse(self, response):
        body = response.xpath("//div[contains(@id, 'mw-content-text')]//table[contains(@class, 'wikitable sortable') and contains(@style, 'width: 100%')]")[0].extract()
        selectors = Selector(text=body.encode('utf-8'), type="html")
        sites = selectors.xpath('//table//tr').extract()

        for site in sites[1:]:
            table_row = Selector(text=site.encode('utf-8'), type="html")
            description = table_row.xpath("//tr/td[1]/text()").extract_first()

            yield {
                'description': description,
                'site': self._site_name(site.encode('utf-8'), table_row)
            }

    def _site_name(self, content, row):
        if self._valid_path(content, "//tr/th[1]/a"):
            return row.xpath("//tr/th[1]/a/text()").extract_first()

    def _valid_path(self, content, xpath):
        root = HTML.fromstring(content)
        if root.xpath(xpath):
            return True
        return False
