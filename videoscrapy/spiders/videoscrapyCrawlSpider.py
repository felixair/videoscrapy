# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from videoscrapy.items import VideoscrapyItem
import urllib

class ExampleSpider(CrawlSpider):
    name = "videoscrapyCrawlSpider"
    download_delay = 2
    allowed_domains = ["wangzhan.com"]
    start_urls = [
        'http://wangzhan.com/vodlist/?5.html',
        'http://wangzhan.com/vodlist/?6.html',
        'http://wangzhan.com/vodlist/?7.html',
        'http://wangzhan.com/vodlist/?8.html',
        'http://wangzhan.com/vodlist/?9.html'
    ]
    rules = [
        Rule(LxmlLinkExtractor(allow=('/vodlist/'), restrict_xpaths=('//div[@class="page"]'), process_value='process_value'), callback='parse_item', follow=True)
    ]
  
    def process_value(value):
        print('value is ', value)
        #value = value[:-1]
        return value
  
    def parse_item(self, response):
        item = VideoscrapyItem()
        sel = Selector(response)
        print(sel)
        mp4url = str(response.url)
        print('mp4url is ', mp4url)
        ''''' blog_name = sel.xpath('/a[@id="cb_post_title_url"]/text()').extract()
        '''
        mp4name = 'mp4name'#sel.xpath('//div[@id="article_details"]/div/h1/span/a/text()').extract()
        item['mp4name'] = [n.encode('utf-8') for n in mp4name]
        item['mp4url'] = mp4url.encode('utf-8')
        #yield item
        #print response.xpath('//div[@class="thumb"]/a/@href')
        for href in response.xpath('//div[@class="thumb"]/a/@href'):
            #print href.extract()
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        body = response.body
        for url in body.split("'"):
           if(url.startswith("http") and url.endswith(".mp4")):
               print('real url is ', url)
               local = url.split('/')[-1]
               urllib.urlretrieve(url, local)
        #sel = Selector(response)
        #print sel.xpath('//div[@id="a1"]')
        #print sel.xpath('//div[@class="pl"]')
        #print sel.xpath('//div[@id="pl1111"]')
        #print sel.xpath('//video[@id="ckplayer_a1"]')
        #print 'hahahahahahah' + response.url
        #for sel in response.xpath('//ul/li'):
        #yield item