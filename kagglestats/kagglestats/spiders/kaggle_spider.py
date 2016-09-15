import scrapy
import re
#import ast
import demjson

p=re.compile('.*datasetListItems\":(.*)\,\"selection.*')
file_patt=re.compile('.*files\":(\[[^\]]*\])\,.*')
#js_patt=re.compile('.*DatasetContainer, (\{.*\})\), document')

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

            #need to do something with the URL
            url = response.urljoin(ds['datasetUrl'])
            #print(url)
            request= scrapy.Request(url,callback=self.parse_datasetpage)
            request.meta['item']=item
            yield request

    def parse_datasetpage(self,response):

        item = response.meta['item']

        text=response.xpath('//script[7]').extract()[0]
        text=text.replace('\n',' ')
        #print (text)
        try:
            m=file_patt.match(text)
            objtext=m.group(1)
            #print ("MATCHED: "+objtext)
        except:
            print ("Regular expression for dataset info NOT matched")
            objtext='[]'

        dataset = demjson.decode(objtext)
        names=[]
        for f in dataset:
            name=f['name']
            names.append(name)
        #print(dataset)
        #files=dataset['files']
        #print(files)
        item['filename']=names
        yield item


