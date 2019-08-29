# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import JobItem
import bloomfilter
import os
from scrapy_redis.spiders import RedisSpider


# class JobSpider(RedisSpider):
class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['51job.com']
    start_urls = ['https://search.51job.com/list/010000%252C020000%252C030200%252C040000,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=']

    # redis_key = 'job51'

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "CONCURRENT_REQUESTS": 16,
        "DOWNLOAD_DELAY": 1,
        "COOKIES_ENABLED": False,
        "DOWNLOADER_MIDDLEWARES": {
            # 'job51Spider.middlewares.Job51SpiderDownloaderMiddleware': 543,
            'job51Spider.rand_agent.UserAgentMiddleware': 543,
            "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
        },
        "ITEM_PIPELINES": {
            # 'job51Spider.pipelines.Job51SpiderPipeline': 300,
            'job51Spider.pipelines.SqlitePipeline': 300,
            # Store scraped item in redis for post-processing. 分布式redispipeline
            # 'scrapy_redis.pipelines.RedisPipeline': 299,
        },
        "DB_NAME": "job51.sqlite",

        # """ scrapy-redis配置 """
        # Enables scheduling storing requests queue in redis.
        # "SCHEDULER": "scrapy_redis.scheduler.Scheduler",
        # # Ensure all spiders share same duplicates filter through redis.
        # "DUPEFILTER_CLASS": "scrapy_redis.dupefilter.RFPDupeFilter",
        # "REDIS_HOST": "192.168.52.225",
        # "REDIS_PORT": "6379"
    }

    # def __init__(self):
    #     if os.path.exists("job.quchong"):
    #         self.bloom = bloomfilter.Bloomfilter("job.quchong")
    #     else:
    #         self.bloom = bloomfilter.Bloomfilter(5000)

    def parse(self, response):
        print("111111111")
        job_type = ["python", "php", "java", "c", "html"]
        for job in job_type:
            job_url = response.url.replace("python", job)
            yield scrapy.Request(
                url=job_url,
                callback=self.parse_all_page,
                dont_filter=True,
                meta={
                    "job_type": job
                }
            )
            # break

    def parse_all_page(self, response):
        meta = response.meta
        all_page = response.xpath("//span[contains(text(), '页，到第')]/text()").get()
        pattern = re.compile("\d+")
        all_page = pattern.search(all_page).group()
        print(all_page)
        if all_page:
            for page in range(1, int(all_page) + 1):
                page_url = response.url.replace("1.html", f"{page}.html")
                print(page_url)
                yield scrapy.Request(
                    url=page_url,
                    callback=self.parse_one_page,
                    dont_filter=True,
                    meta=meta
                )

    def parse_one_page(self, response):
        meta = response.meta
        job_infos = response.xpath("//div[@id='resultList']/div[@class='el']")
        for job_info in job_infos:
            job_href = job_info.xpath("p/span/a/@href").get()
            # if self.bloom.test(job_href):
            #     print("数据已存在")
            #     continue
            # self.bloom.add(job_href)
            # self.bloom.save("job.quchong")
            job_name = job_info.xpath("p/span/a/@title").get()
            job_company = job_info.xpath("span[@class='t2']/a/@title").get()
            job_place = job_info.xpath("span[@class='t3']/text()").get()
            if "-" in job_place:
                job_place = job_place.split("-")[0]
            job_salary = job_info.xpath("span[@class='t4']/text()").get()
            job_min_salary = 0.0
            job_max_salary = 0.0
            if not job_salary:
                job_salary = "薪资面议"
            elif "-" in job_salary:
                job_min_salary, job_max_salary = self.parse_salary(job_salary)
            job_time = job_info.xpath("span[@class='t5']/text()").get()
            # print(job_name, job_href, job_company, job_place, job_salary, job_time)
            item = JobItem()
            item["job_name"] = job_name
            item["job_href"] = job_href
            item["job_company"] = job_company
            item["job_place"] = job_place
            item["job_salary"] = job_salary
            item["job_min_salary"] = job_min_salary
            item["job_max_salary"] = job_max_salary
            item["job_time"] = job_time
            item["job_type"] = meta["job_type"]
            # yield item
            yield scrapy.Request(
                url=job_href,
                callback=self.parse_detail,
                dont_filter=True,
                meta={
                    "item": item
                }
            )

    def parse_detail(self, response):
        detail_infos = response.xpath("//div[@class='tCompany_main']/div[@class='tBorderTop_box']")
        job_detail = {}
        for detail_info in detail_infos:
            title = detail_info.xpath("h2/span/text()").get()
            detail = detail_info.xpath("div//text()").getall()
            job_detail[title] = detail
        # print(job_detail)
        job_information = ""
        job_contact = ""
        job_company_info = ""
        for key, value in job_detail.items():
            if key == "职位信息":
                job_information = map(str.strip, value)
                job_information = [a for a in job_information if a != ""]
                job_information = "\n".join(job_information)
            elif key == "联系方式":
                job_contact = map(str.strip, value)
                job_contact = [a for a in job_contact if a != ""]
                job_contact = "\n".join(job_contact)
            elif key == "公司信息":
                job_company_info = map(str.strip, value)
                job_company_info = [a for a in job_company_info if a != ""]
                job_company_info = "\n".join(job_company_info)
        # print(job_information, job_contact, job_company_info)
        item = response.meta["item"]
        item["job_information"] = job_information
        item["job_contact"] = job_contact
        item["job_company_info"] = job_company_info
        # item["job_href"] = response.url
        # item["job_type_"] = 2
        yield item

    def parse_salary(self, salary):
        job_min_salary = 0
        job_max_salary = 0
        pattern = re.compile("千|万|/|月|年|-")
        job_salary = pattern.split(salary)
        # print("11111111", job_salary)
        if "千" in salary:
            job_min_salary = float(job_salary[0]) * 1000
            job_max_salary = float(job_salary[1]) * 1000
        if "万" in salary:
            job_min_salary = float(job_salary[0]) * 10000
            job_max_salary = float(job_salary[1]) * 10000
        if "年" in salary:
            job_min_salary = float(job_min_salary) / 12
            job_max_salary = float(job_max_salary) / 12
        # job_min_salary, job_max_salary = ("%.2f", "%.2f") % (job_min_salary, job_max_salary)
        # round(job_min_salary, 1)
        # round(job_max_salary, 1)
        # print("111111", job_min_salary, job_max_salary)
        return job_min_salary, job_max_salary

