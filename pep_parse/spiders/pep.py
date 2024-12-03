import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/', ]

    def parse(self, response):
        links = response.css('a[href^="pep-"]::attr(href)').getall()
        for link in links:
            full_url = response.urljoin(link)
            yield response.follow(full_url, callback=self.parse_pep)

    def parse_pep(self, response):
        pep_number = response.css(
            'h1.page-title::text').re_first(r'PEP (\d+)')
        pep_name = response.css(
            'h1.page-title::text').re_first(r'PEP \d+ – (.+)')
        pep_status = response.css('dd.field-even abbr::text').get()
        data = {
            'number': pep_number,
            'name': pep_name,
            'status': pep_status,
        }
        yield PepParseItem(data)
