import scrapy
from TestScraper.testdev256com.testdev256com.items import TestDev256ComItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class SpiderTestDev256Com( CrawlSpider ):
    name = "test.dev256.com"
    allowed_domains = [ "test.dev256.com" ]
    start_urls = [ "https://test.dev256.com/tests/forScraping/objs/" ]

    rules = (
        # # Extract links matching "category.php" (but not matching "subsection.php")
        # # and follow links from them (since no callback means follow=True by default).
        # Rule( LinkExtractor( allow = ("category\.php",), deny = ("subsection\.php",) ) ),

        # Extract links matching "item.php" and parse them with the spider's method parse_item
        Rule( LinkExtractor(), callback = "parse_item", follow = True ),
        # Rule( LinkExtractor( allow = () ), callback = "parse_item" ),
    )

    # https://stackoverflow.com/questions/13724730/how-to-get-the-scrapy-failure-urls
    handle_httpstatus_list = [ 404, 500, 503, 403 ]

    # если нужно парсить и записывать исходные страницы с 301 и кодом, то решение здесь:
    # Can't get Scrapy to parse and follow 301, 302 redirects
    # https://stackoverflow.com/questions/39776377/cant-get-scrapy-to-parse-and-follow-301-302-redirects

    def parse_item( self, response ):
        if response.status == 404:
            pass

        item = TestDev256ComItem()  # scrapy.Item()
        item[ "url" ] = response.url
        item[ "status" ] = response.status
        item[ "referer" ] = response.request.headers.get( "Referer" )
        item[ "title" ] = response.xpath( "//html/head/title/text()" ).extract()
        item[ "h1" ] = response.xpath( "//html/body/h1/text()" ).extract()
        item[ "ahref" ] = response.xpath( "//a/@href" ).extract()
        # self.logger.info( "Страница: %s", response.url )
        # self.logger.info( "Title: %s", item[ "title" ] )
        # self.logger.info( "h1: %s", item[ "h1" ] )
        return item
