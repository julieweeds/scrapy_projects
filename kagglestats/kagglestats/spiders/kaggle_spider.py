import scrapy
import re
#import ast
import demjson

p=re.compile('.*datasetListItems\":(.*)\,\"selection.*')

from kagglestats.items import KagglestatsItem

class KaggleSpider(scrapy.Spider):
    name="kaggle"
    allowed_domains=["kaggle.com"]
    start_urls=["https://www.kaggle.com/datasets?sortBy=hottest&group=all"]

    def parse(self, response):

        text=response.xpath('//script[7]').extract()[0]
        text=text.replace('\n',' ')
        try:
            m=p.match(text)
            objtext=m.group(1)
        except:
            print ("Regular expression for datasetListItems NOT matched")
            objtext='[]'

        dataset_list=demjson.decode(objtext)
        for ds in dataset_list:
            item = KagglestatsItem()
            item['title']=ds['overview']
            item['link']=ds['datasetUrl']
            item['popularity']=ds['downloadCount']
            yield item



