import scrapy
from ..items import XianbaoItem

class XbSpider(scrapy.Spider):
    name = 'xb'
    # allowed_domains = ['xb.com']
    main_url = 'http://www.0818tuan.com/list-1-{}.html'

    start_urls = ['http://xb.com/']

    def start_requests(self):
        for page in range(0, 1):
            url = self.main_url.format(page)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        xbItem = XianbaoItem()
        item_lst = response.xpath('//div[@id="redtag"]/a')
        for item in item_lst:
            title = item.xpath('./@title').get()
            href = item.xpath('./@href').get()
            full_href = response.urljoin(href)
            releaseTime = item.xpath('./span[@class="badge badge-success red"]/text()').get()

            xbItem['title'] = title
            xbItem['href'] = full_href
            xbItem['releaseTime'] = releaseTime
            yield xbItem
