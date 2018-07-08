# -*- coding: utf-8 -*-
import re
from _cffi_backend import string
from unicodedata import normalize

import scrapy
from lxml.html.clean import basestring, unicode

from scrapy_fundrazr.items import ScrapyFundrazrItem


class HealthFundrazrSpider(scrapy.Spider):
    name = 'health_fundrazr'
    allowed_domains = ['fundrazr.com']
    start_urls = ['https://fundrazr.com/find?category=Health']

    def parse(self, response):
        urls = response.xpath("//h2[contains(@class, 'title headline-font')]"
                                          "/a[contains(@class, 'campaign-link')]//@href").extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_details)
        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):

        item = ScrapyFundrazrItem()
        check = response.xpath("//div[contains(@class, 'stats-primary with-goal')]//span[contains(@class, "
                             "'stats-label hidden-phone')]/text()")

        if check:

            item['amount_raised'] = response.xpath("//span[contains(@class,'stat')]/span[contains(@class, 'amount-raised')]/descendant::text()").extract_first().strip() + ' ' + response.xpath("//div[contains(@class, 'stats-primary with-goal')]/@title").extract_first()
            item['goal'] = response.xpath("//div[contains(@class, 'stats-primary with-goal')]//span[contains(@class, 'stats-label hidden-phone')]/text()").extract()[1].strip()[3:][:-5]
        else:
            item['amount_raised'] = response.xpath("//span[contains(@class,'stat')]/span[contains(@class, 'amount-raised')]/descendant::text()").extract_first().strip() + ' ' + response.xpath("//div[contains(@class, 'stats-primary')]/@title").extract_first()
            item['goal'] = 'no goal amount set'

        item['title'] = response.xpath("//div[contains(@id, 'campaign-title')]/descendant::text()").extract_first().strip()
        item['number_of_contributors'] = response.xpath("//div[contains(@class, 'stats-secondary with-goal')]//span[contains(@class, 'donation-count stat')]/text()").extract_first()
        item['story'] = response.xpath("//div[contains(@id, 'full-story')]/p//text()").extract()
        # for story in item['story']:
        #     story.encode("utf-8")
        item['story'] = ' '.join(item['story']).strip(' \t\n\r')
        # item['story'] = item['story'].decode('unicode-escape')
        # item['story'] = item['story'].encode('ascii')
        # item['story'] = convertToString(item['story'])
        # item['story'] = normalize("NFKD", item['story']).encode('ascii', 'replace')
        # to_unicode_or_bust(item['story'])
        # item['story'] = item['story'].replace(u'\u00A0', ' ')
        # re.sub(r"\s+", " ", item['story'])
        # item['story'] = response.css('div.wysiwyg-content clearfix not-empty p::text').extract()
        yield item


# def to_unicode_or_bust(obj, encoding='utf-8'):
#     if isinstance(obj, basestring):
#         if not isinstance(obj, unicode):
#             obj = unicode(obj, encoding)
#     return obj


# def convertToString(encodedString):
#     return encodedString.encode("utf-8").decode('unicode_escape')