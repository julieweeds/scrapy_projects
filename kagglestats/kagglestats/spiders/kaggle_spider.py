import scrapy
import re
import json

p=re.compile('.*datasetListItems\":(.*)\,\"selection.*')
file_patt=re.compile('.*files\":(\[[^\]]*\])\,.*')

from kagglestats.items import KagglestatsItem

class KaggleSpider(scrapy.Spider):
    name="kaggle"
    allowed_domains=["kaggle.com"]
    start_urls=["https://www.kaggle.com/datasets?sortBy=hottest&group=all"]

    def parse(self, response):

        text=response.xpath('//script[7]').extract()[0]     #match the 7th javascript element on the page
        text=text.replace('\n',' ')                         #replace newlines with spaces
        try:
            m=p.match(text)                                 #match the regular expression p
            objtext=m.group(1)                              #extract the first group in ()
        except:
            print ("Regular expression for datasetListItems NOT matched")
            objtext='[]'

        dataset_list=json.loads(objtext)                    #read the string as json
        for ds in dataset_list:
            item = KagglestatsItem()
            item['title']=ds['title']
            item['desc']=ds['overview']
            item['link']=ds['datasetUrl']
            item['popularity']=ds['downloadCount']

            #need to do something with the URL
            url = response.urljoin(ds['datasetUrl'])
            request= scrapy.Request(url,callback=self.parse_datasetpage)
            request.meta['item']=item
            yield request

    def parse_datasetpage(self,response):

        item = response.meta['item']

        text=response.xpath('//script[7]').extract()[0]
        text=text.replace('\n',' ')
        try:
            m=file_patt.match(text)
            objtext=m.group(1)
        except:
            print ("Regular expression for dataset info NOT matched")
            objtext='[]'

        dataset = json.loads(objtext)
        names=[]
        for f in dataset:
            name=f['name']
            names.append(name)
        item['filename']=names
        yield item


