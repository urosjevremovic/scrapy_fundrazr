# -*- coding: utf-8 -*-
import scrapy


class HealthFundrazrSpider(scrapy.Spider):
    name = 'health_fundrazr'
    allowed_domains = ['fundrazr.com']
    start_urls = ['https://fundrazr.com/find?category=Health']

    def parse(self, response):
        urls = response.xpath("//h2[contains(@class, 'title headline-font')]"
                                          "/a[contains(@class, 'campaign-link')]//@href").extract()
        for url in urls:
            url = response.urljoin(url)
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_details)
        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):
        yield {
            'title': response.xpath("//div[contains(@id, 'campaign-title')]/descendant::text()").extract_first().strip(),
        }