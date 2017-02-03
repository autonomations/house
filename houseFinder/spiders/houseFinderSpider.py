# System Installed
import scrapy
import urlparse
from scrapy.spiders import Spider

# Items
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from scrapy.loader import ItemLoader
from houseFinder.items import HouseFinderItem



class HouseItemLoader(ItemLoader):
    # Inherited Variables
    default_output_processor = TakeFirst()

    title_in = MapCompose(unicode.title)
    title_out = Join()

    price_in = MapCompose(unicode.title)
    price_out = Join()

    description_in = MapCompose(unicode.title)
    description_out = Join()

    address_in = MapCompose(unicode.title)
    address_out = Join()

    image_urls_in = MapCompose(unicode.title)
    image_urls_out = Join()

    # you can continue scraping here

    # Housekeeping fields
    # loader.add_value('urlSource', response.url)
    # l.add_value('project', self.settings.get('BOT_NAME'))
    # l.add_value('spider', self.name)
    # l.add_value('server', socket.gethostname())
    # l.add_value('date', datetime.datetime.now())

class houseFinderSpider(scrapy.Spider):
        name = 'house'

        start_urls = [
            'http://www.zillow.com/homes/san-diego_rb/'
        ]

        def parse(self, response):

            for sel in response.xpath('//ul[@class="photo-cards"]/li'):
                itemObject = HouseFinderItem()
                loader = HouseItemLoader(item=itemObject, response=response, select=sel)

                loader.add_xpath('title', '//*[@itemprop="name"][1]/text()', MapCompose(unicode.strip, unicode.title))
                loader.add_xpath('price', './/*[@itemprop="price"][1]/text()', MapCompose(lambda i: i.replace(',',''), float), re='[,.0-9]+')
                loader.add_xpath('description', '//*[@itemprop="description"][1]/text()', MapCompose(unicode.strip), Join())
                loader.add_xpath('address', '//*[@itemtype="http://schema.org/Place"][1]/text()', MapCompose(unicode.strip))
                loader.add_xpath('image_urls', '//*[@itemprop="image"][1]/@src', MapCompose(lambda i: urlparse.urljoin(response.url, i)))

                loader.add_xpath('streetAddress', './/span[@itemprop="streetAddress"]/text()', MapCompose(unicode.strip))
                loader.add_xpath('addressCity', './/span[@itemprop="addressLocality"]/text()', MapCompose(unicode.strip))
                loader.add_xpath('addressRegion', './/span[@itemprop="addressRegion"]/text()', MapCompose(unicode.strip))
                loader.add_xpath('postalCode', './/span[@itemprop="postalCode"]/text()'      , MapCompose(float))
                loader.add_xpath('longitude', './/meta[@itemprop="longitude"]/@content'      , MapCompose(float))
                loader.add_xpath('latitude', './/meta[@itemprop="latitude"]/@content'        , MapCompose(float))
                #loader.add_xpath('price', './/span[@class="zsg-photo-card-price"]/text()', MapCompose(unicode.strip, unicode.title))

                loader.add_xpath('beds', './/span[@class="zsg-photo-card-info"]/text()[1]'  , MapCompose(lambda i: i.replace(',',''), float), re='[,.0-9]+')
                loader.add_xpath('baths', './/span[@class="zsg-photo-card-info"]/text()[2]' , MapCompose(lambda i: i.replace(',',''), float), re='[,.0-9]+')
                loader.add_xpath('sqft', './/span[@class="zsg-photo-card-info"]/text()[3]'  , MapCompose(lambda i: i.replace(',',''), float), re='[,.0-9]+')

                loader.add_xpath('days_on_market', './/span[@class="zsg-photo-card-notification "]/text()', MapCompose(unicode.strip))
                loader.add_xpath('image_url', './/div[@class="zsg-photo-card-img"]/img/@src'              , MapCompose(lambda i: urlparse.urljoin(response.url, i)))
                loader.add_xpath('photo_count', './/div[@class="zsg-photo-card-img"]/li/text()'           , MapCompose(float))

                #loader.add_xpath('address', './/span[@class="zsg-photo-card-address"]/text()'             , MapCompose(unicode.strip))
                loader.add_xpath('status', './/span[@class="zsg-photo-card-status"]/text()'               , MapCompose(unicode.strip))

                item = loader.load_item()

                yield item


            # # JUMP TO NEXT PAGE
            next_page = response.xpath('//li[@class="zsg-pagination-next"]/a/@href').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)



        # def parse_item(self, itemObject, response, select):
        #     loader = HouseItemLoader(item=itemObject, response=response, select=select)

        #     loader.add_xpath('title', '//*[@itemprop="name"][1]/text()')
        #     loader.add_xpath('price', './/*[@itemprop="price"][1]/text()')
        #     loader.add_xpath('description', '//*[@itemprop="description"][1]/text()')
        #     loader.add_xpath('address', '//*[@itemtype="http://schema.org/Place"][1]/text()')
        #     loader.add_xpath('image_urls', '//*[@itemprop="image"][1]/@src')

        #     loader.add_xpath('streetAddress','.//span[@itemprop="streetAddress"]/text()')
        #     loader.add_xpath('addressCity', './/span[@itemprop="addressLocality"]/text()')
        #     loader.add_xpath('addressRegion', './/span[@itemprop="addressRegion"]/text()')
        #     loader.add_xpath('postalCode', './/span[@itemprop="postalCode"]/text()')
        #     loader.add_xpath('longitude', './/meta[@itemprop="longitude"]/@content')
        #     loader.add_xpath('latitude', './/meta[@itemprop="latitude"]/@content')
        #     loader.add_xpath('price', './/span[@class="zsg-photo-card-price"]/text()')

        #     loader.add_xpath('beds', './/span[@class="zsg-photo-card-info"]/text()[1]')
        #     loader.add_xpath('baths', './/span[@class="zsg-photo-card-info"]/text()[2]')
        #     loader.add_xpath('sqft', './/span[@class="zsg-photo-card-info"]/text()[3]')

        #     loader.add_xpath('days_on_market', './/span[@class="zsg-photo-card-notification "]/text()')
        #     loader.add_xpath('image_url', './/div[@class="zsg-photo-card-img"]/img/@src')
        #     loader.add_xpath('photo_count','.//div[@class="zsg-photo-card-img"]/li/text()')

        #     loader.add_xpath('address', './/span[@class="zsg-photo-card-address"]/text()')
        #     loader.add_xpath('status', './/span[@class="zsg-photo-card-status"]/text()')
           # loader.add_xpath('url', './article/div[1]/a/@href')
            
            # return loader.load_item()




            # # JUMP TO NEXT PAGE CALLBACKS
            # next_page = response.xpath('//li[@class="zsg-pagination-next"]/a/@href').extract_first()
            # if next_page is not None:
            #     #next_page = response.urljoin(next_page)
            #     yield Request(next_page, callback=self.parse_item, meta={'item': item})


            # item = HouseFinderItem()

            # #      Load fields using XPath expressions
            # item['title'] = sel.xpath('//*[@itemprop="name"][1]/text()').extract_first()
            # item['price'] = sel.xpath('.//*[@itemprop="price"][1]/text()').extract_first()
            # item['description'] = sel.xpath('//*[@itemprop="description"][1]/text()').extract_first()
            # item['address'] = sel.xpath('//*[@itemtype="http://schema.org/Place"][1]/text()').extract_first()
            # #item['url'] = Mapcompose.compose(sel.xpath('./article/div[1]/a/@href'))
            # item['image_url'] = sel.xpath('//*[@itemprop="image"][1]/@src').extract_first()


            # item['streetAddress'] = sel.xpath('.//span[@itemprop="streetAddress"]/text()').extract_first()
            # item['addressCity'] = sel.xpath('.//span[@itemprop="addressLocality"]/text()').extract_first()
            # item['addressRegion'] = sel.xpath('.//span[@itemprop="addressRegion"]/text()').extract_first()
            # item['postalCode'] = sel.xpath('.//span[@itemprop="postalCode"]/text()').extract_first()
            # item['longitude'] = sel.xpath('.//meta[@itemprop="longitude"]/@content').extract_first()
            # item['latitude'] = sel.xpath('.//meta[@itemprop="latitude"]/@content').extract_first()
            # item['price'] = sel.xpath('.//span[@class="zsg-photo-card-price"]/text()').extract_first()

            # item['beds'] = sel.xpath('.//span[@class="zsg-photo-card-info"]/text()[1]').extract_first()
            # item['baths'] = sel.xpath('.//span[@class="zsg-photo-card-info"]/text()[2]').extract_first()
            # item['sqft'] = sel.xpath('.//span[@class="zsg-photo-card-info"]/text()[3]').extract_first()

            # item['days_on_market'] = sel.xpath('.//span[@class="zsg-photo-card-notification "]/text()').extract_first()
            # # item['image_url'] = sel.xpath('.//div[@class="zsg-photo-card-img"]/img/@src')
            # item['photo_count'] = sel.xpath('.//div[@class="zsg-photo-card-img"]/li/text()').extract_first()

            # #item['address'] = sel.xpath('.//span[@class="zsg-photo-card-address"]/text()').extract_first()
            # item['status'] = sel.xpath('.//span[@class="zsg-photo-card-status"]/text()').extract_first()
            

            # Housekeeping fields
            # item['urlSource'] = sel.xpath(response.url)
            # item['project']   = self.settings.get('BOT_NAME')
            # item['spider']    = self.name
            # item['server']    = socket.gethostname
            # item['date']      = datetime.datetime.now

            #     yield item


            # # JUMP TO NEXT PAGE
            # next_page = response.xpath('//li[@class="zsg-pagination-next"]/a/@href').extract_first()
            # if next_page is not None:
            #     next_page = response.urljoin(next_page)
            #     yield scrapy.Request(next_page, callback=self.parse)

                # yield {
                #     'streetAddress': sel.xpath('.//span[@itemprop="streetAddress"]/text()').extract_first(),
                #     'addressCity': sel.xpath('.//span[@itemprop="addressLocality"]/text()').extract_first(),
                #     'addressRegion': sel.xpath('.//span[@itemprop="addressRegion"]/text()').extract_first(),
                #     'postalCode': sel.xpath('.//span[@itemprop="postalCode"]/text()').extract_first(),
                #     'longitude': sel.xpath('.//meta[@itemprop="longitude"]/@content').extract_first(),
                #     'latitude': sel.xpath('.//meta[@itemprop="latitude"]/@content').extract_first(),
                #     'price': sel.xpath('.//span[@class="zsg-photo-card-price"]/text()').extract_first(),
        
                #     'beds': sel.xpath('.//span[@class="zsg-photo-card-info"]/text()[1]').extract_first(),
                #     'baths': sel.xpath('.//span[@class="zsg-photo-card-info"]/text()[2]').extract_first(),
                #     'sqft': sel.xpath('.//span[@class="zsg-photo-card-info"]/text()[3]').extract_first(),

                #     'days on Market' : sel.xpath('.//span[@class="zsg-photo-card-notification "]/text()').extract_first(),
                #     'image_url': sel.xpath('.//div[@class="zsg-photo-card-img"]/img/@src').extract_first(),
                #     'photo_count': sel.xpath('.//div[@class="zsg-photo-card-img"]/li/text()').extract_first(),

                #     'address': sel.xpath('.//span[@class="zsg-photo-card-address"]/text()').extract_first(),
                #     'status': sel.xpath('.//span[@class="zsg-photo-card-status"]/text()').extract_first(),
                #     'url': sel.xpath('./article/div[1]/a/@href').extract_first(),

                # }  




# class Basketspider(BaseSpider, errorLog):
#     name = "basketsp_test"
#     download_delay = 0.5

#     def start_requests(self):

#         item = WhateverYourOutputItemIs()
#         yield Request("http://www.euroleague.net/main/results/by-date", callback=self.parseSeasonsLinks, meta={'item':item})

#     def parseSeaseonsLinks(self, response):

#         item = response.meta['item'] 

#         hxs = HtmlXPathSelector(response)

#         html = hxs.extract()
#         roundLinkList = list()

#         roundLinkPttern = re.compile(r'http://www\.euroleague\.net/main/results/by-date\?gamenumber=\d+&phasetypecode=RS')

#         for (roundLink) in re.findall(roundLinkPttern, html):
#             if roundLink not in roundLinkList:
#                 roundLinkList.append(roundLink)        

#         for i in range(len(roundLinkList)):

#             #if you wanna output this info in the final item
#             item['RoundLink'] = roundLinkList[i]

#             # Generate new request for round page
#             yield Request(stockpageUrl, callback=self.parseStockItem, meta={'item':item})


#     def parseRoundPAge(self, response):

#         item = response.meta['item'] 
#         #Do whatever you need to do in here call more requests if needed or return item here

#         item['Thing'] = 'infoOnPage'
#         #....
#         #....
#         #....

#         return  item

    # allowed_domains = ["web"]

    # urls = UrlGenerator('args')
    # urls.generate_url_zipcodes_from_arguments()
    # start_urls = urls.getUrlList()

    # Rules for horizontal and vertical crawling
    # rules = (
    #     Rule(LinkExtractor(restrict_xpaths='//*[contains(@class,"next")]')),
    #     Rule(LinkExtractor(restrict_xpaths='//*[@itemprop="url"]'), callback='parse_item')
    # )



    # def parse(self, response):
    #     # Get item URLs and yield Requests
    #     # for sel in response.xpath('//ul[@class="photo-cards"]/li'):
    #     #     #yield scrapy.Request(urlparse.urljoin(response.url, sel), callback=self.parse_item)
    #     #     l = parse_item(item=HouseFinderItem(), response=response, selection=sel)
    #     #     yield l

    #     # # Get the next index URLs and yield Requests
    #     # next_selector = response.xpath('//*[contains(@class,"next")]//@href')
    #     # for url in next_selector.extract():
    #     #     yield Request(urlparse.urljoin(response.url, url))

    #     # # Get item URLs and yield Requests
    #     # item_selector = response.xpath('//*[@itemprop="url"]/@href')
    #     # for url in item_selector.extract():
    #     #     yield Request(urlparse.urljoin(response.url, url),
    #     #                   callback=self.parse_item)


    #     for sel in response.xpath('//ul[@class="photo-cards"]/li'):

    #         yield {
    #             'streetAddress': sel.xpath('.//span[@itemprop="streetAddress"]/text()').extract_first(),
    #             'addressCity': sel.xpath('.//span[@itemprop="addressLocality"]/text()').extract_first(),
    #             'addressRegion': sel.xpath('.//span[@itemprop="addressRegion"]/text()').extract_first(),
    #             'postalCode': sel.xpath('.//span[@itemprop="postalCode"]/text()').extract_first(),
    #             'longitude': sel.xpath('.//meta[@itemprop="longitude"]/@content').extract_first(),
    #             'latitude': sel.xpath('.//meta[@itemprop="latitude"]/@content').extract_first(),
    #             'price': sel.xpath('.//span[@class="zsg-photo-card-price"]/text()').extract_first(),

    #             'beds': sel.xpath('.//span[@class="zsg-photo-card-info"]/text()[1]').extract_first(),
    #             'baths': sel.xpath('.//span[@class="zsg-photo-card-info"]/text()[2]').extract_first(),
    #             'sqft': sel.xpath('.//span[@class="zsg-photo-card-info"]/text()[3]').extract_first(),

    #             'days on Market' : sel.xpath('.//span[@class="zsg-photo-card-notification "]/text()').extract_first(),
    #             'image_url': sel.xpath('.//div[@class="zsg-photo-card-img"]/img/@src').extract_first(),
    #             'photo_count': sel.xpath('.//div[@class="zsg-photo-card-img"]/li/text()').extract_first(),

    #             'address': sel.xpath('.//span[@class="zsg-photo-card-address"]/text()').extract_first(),
    #             'status': sel.xpath('.//span[@class="zsg-photo-card-status"]/text()').extract_first(),
    #             'url': sel.xpath('./article/div[1]/a/@href').extract_first()
    #         }


    #     # JUMP TO NEXT PAGE
    #     next_page = response.xpath('//li[@class="zsg-pagination-next"]/a/@href').extract_first()
    #     if next_page is not None:
    #         next_page = response.urljoin(next_page)
    #         yield scrapy.Request(next_page = response.urljoin(next_page), callback=self.parse)
    
  





    # def parse_items_yield(self, response):

    #     'streetAddress': sel.xpath('.//span[@itemprop="streetAddress"]/text()').extract_first(),
    #     'addressCity': sel.xpath('.//span[@itemprop="addressLocality"]/text()').extract_first(),
    #     'addressRegion': sel.xpath('.//span[@itemprop="addressRegion"]/text()').extract_first(),
    #     'postalCode': sel.xpath('.//span[@itemprop="postalCode"]/text()').extract_first(),
    #     'longitude': sel.xpath('.//meta[@itemprop="longitude"]/@content').extract_first(),
    #     'latitude': sel.xpath('.//meta[@itemprop="latitude"]/@content').extract_first(),
    #     'price': sel.xpath('.//span[@class="zsg-photo-card-price"]/text()').extract_first(),

    #     'beds': sel.xpath('.//span[@class="zsg-photo-card-info"]/text()[1]').extract_first(),
    #     'baths': sel.xpath('.//span[@class="zsg-photo-card-info"]/text()[2]').extract_first(),
    #     'sqft': sel.xpath('.//span[@class="zsg-photo-card-info"]/text()[3]').extract_first(),

    #     'days on Market' : sel.xpath('.//span[@class="zsg-photo-card-notification "]/text()').extract_first(),
    #     'image_url': sel.xpath('.//div[@class="zsg-photo-card-img"]/img/@src').extract_first(),
    #     'photo_count': sel.xpath('.//div[@class="zsg-photo-card-img"]/li/text()').extract_first(),

    #     'address': sel.xpath('.//span[@class="zsg-photo-card-address"]/text()').extract_first(),
    #     'status': sel.xpath('.//span[@class="zsg-photo-card-status"]/text()').extract_first(),
    #     'url': sel.xpath('./article/div[1]/a/@href').extract_first(),

    #     'lot-size': sel.xpath('.//li[@data-label="property-meta-lotsize"]/span/text()').extract(),
    #     'garage': sel.xpath('.//li[@data-label="property-meta-garage"]/span/text()').extract(),

    #     pass


# class UrlGenerator():

#     def __init__(self, urlSourceLocation):
#         self.urlSourceLocation = urlSourceLocation
#         self.urlList = []
#         self.args =  ''
#         self.csv = ''
#         #self.urlList = generate_url_zipcodes_from_arguments(sys.argv[1:])


#         # if urlType = 'csv'
#         #     pass
#         # elif urlType = 'args'
#         #     self.urlList = generate_url_zipcodes_from_arguments(sys.argv[1:])
#         # else
#         #     pass
    
#     def generate_url_zipcodes_from_arguments(self, argv):
#         try:
#             opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
#         except getopt.GetoptError:
#             print 'test.py -i <inputfile> -o <outputfile>'
#             sys.exit(2)
#         for opt, arg in opts:
#             if opt == '-h':
#                 print 'test.py -i <inputfile> -o <outputfile>'
#                 sys.exit()
#             elif opt in ("-i", "--ifile"):
#                 self.urlList.append('http://www.zillow.com/homes/'+argv+'_rb/')

#         print 'Zipcodes Entered are: "', self.urlList
#         print

#     def getUrlList(self):
#         return self.urlList

    # def start_requests(self):
    # with open(getattr(self, "file", "todo.csv"), "rU") as f:
    #     reader = csv.DictReader(f)
    #     for line in reader:
    #         request = Request(line.pop('url'))
    #         request.meta['fields'] = line
    #         yield request

    # def parse(self, response):
    #     item = Item()
    #     l = ItemLoader(item=item, response=response)
    #     for name, xpath in response.meta['fields'].iteritems():
    #         if xpath:
    #             item.fields[name] = Field()
    #             l.add_xpath(name, xpath)

    #     return l.load_item()




