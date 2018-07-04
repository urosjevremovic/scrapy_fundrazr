# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyFundrazrItem(scrapy.Item):
    title = scrapy.Field()
    amount_raised = scrapy.Field()
    goal = scrapy.Field()
    number_of_contributors = scrapy.Field()
    story = scrapy.Field()

