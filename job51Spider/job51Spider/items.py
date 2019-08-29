# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Job51SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobItem(scrapy.Item):
    job_name = scrapy.Field()
    job_href = scrapy.Field()
    job_company = scrapy.Field()
    job_place = scrapy.Field()
    job_salary = scrapy.Field()
    job_min_salary = scrapy.Field()
    job_max_salary = scrapy.Field()
    job_time = scrapy.Field()
    job_type = scrapy.Field()

    # job_type_ = scrapy.Field()


# class JobDetailItem(scrapy.Item):
    job_information = scrapy.Field()
    job_contact = scrapy.Field()
    job_company_info = scrapy.Field()

    # job_href = scrapy.Field()
    # job_type_ = scrapy.Field()


