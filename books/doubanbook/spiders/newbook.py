# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from doubanbook.items import DoubanbookItem

class NewbookSpider(CrawlSpider):
    name = 'newbook'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=']
    # 每一页的匹配规则
    pagelink = LinkExtractor(allow = ("type=4"))
    #print(pagelink)
    # 每一页里的每个帖子的匹配规则
    contentlink = LinkExtractor(allow =(r"/html/question/\d+/\d+.shtml"))
    #print(contentlink)
    rules = (
        Rule(pagelink, process_links = "deal_links"),
        Rule(contentlink, callback = "parse_item")
    )
 
    def deal_links(self, links):
       
        for each in links:
            each.url = each.url.replace("?","&").replace("Type&","Type?")
            print("!!!!!!!!!!!!!!!!!!!!!!!!")
            print(each.url)
       
        return links

    def parse_item(self, response):
    
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        item = DoubanbookItem()
        # 标题
        item['title'] = response.xpath('//div[contains(@class, "pagecenter p3")]//strong/text()').extract()[0]
        # 编号
        item['author'] = item['title'].split(' ')[-1].split(":")[-1]
        # 内容，先使用有图片情况下的匹配规则，如果有内容，返回所有内容的列表集合
        content = response.xpath('//div[@class="contentext"]/text()').extract()
        # 如果没有内容，则返回空列表，则使用无图片情况下的匹配规则
        if len(content) == 0:
            content = response.xpath('//div[@class="c1 text14_2"]/text()').extract()
            item['info'] = "".join(content).strip()
        else:
            item['info'] = "".join(content).strip()
        # 链接
        item['url'] = response.url

        yield item
