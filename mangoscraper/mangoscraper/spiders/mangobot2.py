# -*- coding: utf-8 -*-
import scrapy


class MangobotSpider(scrapy.Spider):
    name = 'mangobot'
    start_urls = ['https://www.mangoplate.com/search/서울대입구']
    
    def parse(self, response):
        name = response.xpath('/html/body/main/article/div[2]/div/div/section/div[3]/ul/li/div[1]/figure/figcaption/div/a/h2/text()').extract()
        address = response.xpath('/html/body/main/article/div[2]/div/div/section/div[3]/ul/li/div[1]/figure/a/div/img/@alt').extract()
        food_type= response.xpath('/html/body/main/article/div[2]/div/div/section/div[3]/ul/li/div[1]/figure/figcaption/div/p[1]/span/text()').extract()
        ratings = response.xpath('/html/body/main/article/div[2]/div/div/section/div[3]/ul/li/div[1]/figure/figcaption/div/strong/text()').extract()
        images = response.xpath('/html/body/main/article/div[2]/div/div/section/div[3]/ul/li/div[1]/figure/a/div/img/@data-original').extract()
        
        for item in zip(name, address, food_type, ratings, images):
            
            output = {
                'name':item[0].strip(),
                'address':item[1].strip(),
                'food_type':item[2].strip(),
                'ratings':item[3].strip(),
                'images':item[4].strip()
                    }

            yield output
