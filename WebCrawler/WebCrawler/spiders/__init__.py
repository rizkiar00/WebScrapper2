# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import string
import scrapy
from scrapy import Request

class AdaptSpider(scrapy.Spider):
    name = "Adapt"
    start_urls = ['https://www.adapt.io/directory/industry/telecommunications/A-1']
    def parse(self, response):


        cssclass = ".DirectoryList_seoDirectoryList__aMaj8 a::attr(href)"
        next_urls = response.css(cssclass).extract()
        print(next_urls)
        return (Request(url, callback=self.parse_company) for url in next_urls)

    def getinformation(self, info,):
        infodict = {}
        # try:
        #     infodict["Company_Name"] = nameurl[0]
        # except IndexError:
        #     infodict["Company_Name"] = 0
        # try:
        #     infodict["Company_URL"] = nameurl[1]
        # except IndexError:
        #     infodict["Company_URL"] = 0
        try:
            idxRV = info.index("Revenue")
            infodict["Revenue"] = info[idxRV+1]
        except ValueError:
            infodict["Revenue"] = 0

        try:
            idxHC = info.index("Head Count")
            infodict["Head Count"] = info[idxHC+1]
        except ValueError:
            infodict["Head Count"] = 0

        try:
            idxIN = info.index("Industry")
            infodict["Industry"] = info[idxIN+1]
        except ValueError:
            infodict["Industry"] = 0

        try:
            idxLC = info.index("Location")
            infodict["Location"] = "".join(info[idxLC+1:])
        except ValueError:
            infodict["Location"] = 0
        return infodict

    def parse_company(self, response):
        nameurl = response.css(".CompanyTopInfo_leftContentWrap__3gIch ::text").extract()
        information = response.css(".CompanyTopInfo_contentWrapper__2Jkic ::text").extract()
        url = response.request.url
        procesinfo = self.getinformation(information)
        yield {
            "Company_Name": nameurl[0],
            "Company_URL":  nameurl[1],
            "Revenue" : procesinfo["Revenue"],
            "Head_Count" : procesinfo["Head Count"],
            "Industry" : procesinfo["Industry"],
            "Location" : procesinfo["Location"]
        }
        # next_urls = response.css(".DirectoryList_seoDirectoryList__aMaj8").xpath('//a/@href').extract()[0:-5]
        # for next_url in next_urls:
        #     yield Request(response.urljoin(next_url), callback=self.parse_company)
        NEXT_PAGE_SELECTOR = ".DirectoryList_actionBtnLink__Seqhh a::attr(href)"
        next_page = response.css(NEXT_PAGE_SELECTOR).extract()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page[-1]),
                callback=self.parse
            )