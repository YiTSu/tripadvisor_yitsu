# -*- coding: utf-8 -*-
import scrapy

from hotels.items import CitysItem, HotelsItem, CommentsItem


class TripadvisorhotelsSpider(scrapy.Spider):
    # 爬虫名称
    name = 'tripadvisorhotels'
    # 允许爬取的域名
    # allowed_domains = ['tripadvisor.com']
    # 爬虫入口爬取地址
    start_urls = ['http://www.meijutt.com/new100.html']
    # start_urls = ['https//www.baidu.com/']
    base_url = 'https://www.tripadvisor.cn'
    start_urls = ['https://www.tripadvisor.cn/Hotels-g294211-China-Hotels.html']

    # 爬虫爬取页数控制初始值
    count = 1
    # 爬虫爬取页数
    page_end = 110

    def parse(self, response):
        self.logger.debug(response.text)
        print("Hello parse!")
        # cityList = response.xpath('//ul[@class="top-list fn-clear"]/li')
        # page_end = response.xpath('//div[@class="unified ui_pagination leaf_geo_pagination"]/@data-numPages')
        cityList = response.xpath('//div[@class="geo_wrap"]/a')
        # print(cityList)
        for city in cityList:
            citysItem = CitysItem()
            name = city.xpath('./text()').extract()
            if name:
                citysItem['name'] = name[0]
            else:
                citysItem['name'] = ''

            href = city.xpath('./@href').extract()
            if href:
                citysItem['href'] = self.base_url + href[0]
            else:
                citysItem['href'] = ''

            citysItem['hotelsCount'] = ''
            yield scrapy.Request(citysItem['href'], meta={'citysItemPass': citysItem}, callback=self.hotels_parse)
            # print("遍历city")
            # print(city.xpath('./h5/a/@title').extract())
            print(citysItem['name'])
            # print(city.xpath('./@data-geoId').extract()[0])
            # print(citysItem['href'])
            yield citysItem
        print("End parse!")

        # 循环爬取翻页
        nextPage = response.xpath('//div[@class="unified ui_pagination leaf_geo_pagination"]/a[text()="下一页"]/@href').extract()[0]
        # print(nextPage)
        # 爬取页数控制及末页控制
        if self.count < self.page_end and nextPage != 'javascript:;':
            if nextPage is not None:
                # 爬取页数控制值自增
                self.count = self.count + 1
                # print("count++!!!")
                # 翻页请求
                yield scrapy.Request(self.base_url + nextPage, callback=self.othercitys_parse)
                # print("已调用scrapy.Request()方法，进入othercitys_parse!")
        else:
            # 爬虫结束
            # print("爬虫结束")
            return None

    def othercitys_parse(self, response):
        # print("Hello othercitys_parse!")
        # cityList = response.xpath('//ul[@class="top-list fn-clear"]/li')
        # page_end = response.xpath('//div[@class="unified ui_pagination leaf_geo_pagination"]/@data-numPages')
        cityList = response.xpath('//li[@class="ui_column is-12-mobile is-4-tablet is-3-desktop"]/a')
        # print(cityList)
        for city in cityList:
            citysItem = CitysItem()
            name = city.xpath('./div[@class ="info"]/span[@class="name"]/text()').extract()
            if name:
                citysItem['name'] = name[0]
            else:
                citysItem['name'] = ''
            # citysItem['name'] = city.xpath('./div[@class ="info"]/span[@class="name"]/text()').extract()[0]
            href = city.xpath('./@href').extract()
            if href:
                citysItem['href'] = self.base_url + href[0]
            else:
                citysItem['href'] = ''

            hotelsCount =  city.xpath('./div[@class ="info"]/span[@class="name"]/span[@class="count"]/text()').extract()
            if hotelsCount:
                citysItem['hotelsCount'] = hotelsCount[0]
            else:
                citysItem['hotelsCount'] = ''
            # citysItem['hotelsCount'] = city.xpath('./div[@class ="info"]/span[@class="name"]/span[@class="count"]/text()').extract()[0]
            yield scrapy.Request(citysItem['href'], meta={'citysItemPass': citysItem}, callback=self.hotels_parse)
            # print("遍历city")
            # print(city.xpath('./h5/a/@title').extract())
            print(citysItem['name'])
            # print(city.xpath('./@data-geoId').extract()[0])
            # print(citysItem['href'])
            print(citysItem['hotelsCount'])
            yield citysItem
        # print("End othercitys_parse!")

        # 循环爬取翻页
        nextPage = response.xpath('//div[@class="unified ui_pagination leaf_geo_pagination"]/a[text()="下一页"]/@href').extract()[0]
        # print(nextPage)
        # 爬取页数控制及末页控制
        if self.count < self.page_end and nextPage != 'javascript:;':
            if nextPage is not None:
                # 爬取页数控制值自增
                self.count = self.count + 1
                # print("count++!!!")
                # 翻页请求
                yield scrapy.Request(self.base_url + nextPage, callback=self.othercitys_parse)
        else:
            # 爬虫结束
            # print("爬虫结束")
            return None


    def hotels_parse(self,response):
        print("Hello hotels_parse!")
        hotelList = response.xpath('//div[@class="ui_column is-8 main_col allowEllipsis "]/div[@class="prw_rup prw_meta_hsx_listing_name listing-title"]/div[@class="listing_title"]/a')
        # print(hotelList)
        citysItemPass = response.meta['citysItemPass']
        for hotel in hotelList:
            # print("进入了hotels_parse的for循环！")
            hotelsItem = HotelsItem()
            id = hotel.xpath('./@id').extract()
            if id:
                hotelsItem['id'] = id[0]
            else:
                hotelsItem['id'] = ''
            href = hotel.xpath('./@href').extract()
            if href:
                hotelsItem['href'] = self.base_url + href[0]
            else:
                hotelsItem['href'] = ''
            # hotelsItem['id'] = hotel.xpath('./@id').extract()[0]
            # hotelsItem['href'] = self.base_url + hotel.xpath('./@href').extract()[0]
            name = hotel.xpath('./text()').extract()
            if name:
                hotelsItem['name'] = name[0]
            else:
                hotelsItem['name'] = ''
            # hotelsItem['name'] = hotel.xpath('./text()').extract()[0]
            hotelsItem['cityHref'] = citysItemPass['href']
            yield scrapy.Request(hotelsItem['href'], meta={'hotelsItemPass': hotelsItem}, callback=self.hotels_parse_details)

            # print(hotelsItem['id'])
            # print(hotelsItem['href'])
            # print(hotelsItem['name'])
            # print(hotelsItem['city'])
            # print("退出了hotels_parse的for循环！")

        print("End hotels_parse!")

        # 循环爬取网页
        nextPage = response.xpath('//div[@class="unified ui_pagination standard_pagination ui_section listFooter"]/a[text()="下一页"]/@href').extract()[0]
        # print(nextPage)
        # 爬取页数控制及末页控制
        if self.count < self.page_end and nextPage != 'javascript:;':
            if nextPage is not None:
                # 爬取页数控制值自增
                self.count = self.count + 1
                # print("count++!!!")
                # 翻页请求
                yield scrapy.Request(self.base_url + nextPage, callback=self.hotels_parse)
        else:
            # 爬虫结束
            # print("爬虫结束")
            return None

    def hotels_parse_details(self, response):

        print("Hello hotels_parse_details!")
        hotelsItemPass = response.meta['hotelsItemPass']
        print("接收到了hotelsItemPass！")
        hotelsItem = HotelsItem()
        hotelsItem['id'] = hotelsItemPass['id']
        print(hotelsItem['id'])
        hotelsItem['href'] = hotelsItemPass['href']
        hotelsItem['name'] = hotelsItemPass['name']
        print(hotelsItem['name'])
        hotelsItem['cityHref'] = hotelsItemPass['cityHref']
        nameEn = response.xpath('//div[@class="ui_column is-12-tablet is-10-mobile hotelDescription"]/h1/div/text()').extract()
        if nameEn:
            hotelsItem['nameEn'] = nameEn[0]
        else:
            hotelsItem['nameEn'] = ''
        # hotelsItem['nameEn'] = response.xpath('//div[@class="ui_column is-12-tablet is-10-mobile hotelDescription"]/h1/div/text()').extract()[0]
        print(hotelsItem['nameEn'])
        rating = response.xpath('//div[@class="prw_rup prw_common_bubble_rating rating"]/span/@alt').extract()
        if rating:
            hotelsItem['rating'] = rating[0]
        else:
            hotelsItem['rating'] = ''
        # hotelsItem['rating'] = response.xpath('//div[@class="prw_rup prw_common_bubble_rating rating"]/span/@alt').extract()[0]
        print(hotelsItem['rating'])
        comments = response.xpath('//span[@class="reviewCount "]/text()').extract()
        if comments:
            hotelsItem['comments'] = comments[0]
        else:
            hotelsItem['comments'] = ''
        # hotelsItem['comments'] = response.xpath('//span[@class="reviewCount "]/text()').extract()[0]
        print(hotelsItem['comments'])
        rank = response.xpath('//b[@class="rank"]/text()').extract()
        if rank:
            hotelsItem['rank'] = rank[0]
        else:
            hotelsItem['rank'] = ''
        # hotelsItem['rank'] = response.xpath('//b[@class="rank"]/text()').extract()[0]
        print(hotelsItem['rank'])
        address = response.xpath('//div[@class="hpCTAPlaceholder hidden"]/@data-address').extract()
        if address:
            hotelsItem['address'] = address[0]
        else:
            hotelsItem['address'] = ''
        # hotelsItem['address'] = response.xpath('//div[@class="hpCTAPlaceholder hidden"]/@data-address').extract()[0]
        addressSim = response.xpath('//div[@class="ui_column is-12-mobile is-6-tablet"]/div[@class="sub_content"]/div[@class="textitem"]/text()').extract()
        if addressSim:
            hotelsItem['addressSim'] = addressSim[1]
        else:
            hotelsItem['addressSim'] = ''
        # hotelsItem['addressSim'] = response.xpath('//div[@class="ui_column is-12-mobile is-6-tablet"]/div[@class="sub_content"]/div[@class="textitem"]/text()').extract()[1]
        print(hotelsItem['addressSim'])
        photos = response.xpath('//div[@class="hotels-media-album-parts-PhotoCount__textWrapper--30uL8"]/span[@class="is-hidden-tablet hotels-media-album-parts-PhotoCount__text--3OXuH"]/text()').extract()
        if photos:
            hotelsItem['photos'] = photos[0]
        else:
            hotelsItem['photos'] = ''
        # hotelsItem['photos'] = response.xpath('//div[@class="hotels-media-album-parts-PhotoCount__textWrapper--30uL8"]/span[@class="is-hidden-tablet hotels-media-album-parts-PhotoCount__text--3OXuH"]/text()').extract()[0]
        star = response.xpath('//div[@class="hotels-hotel-review-overview-HighlightedAmenities__amenityItem--3E_Yg"]/div/text()').extract()
        if star:
            hotelsItem['star'] = star[0]
        else:
            hotelsItem['star'] = ''
        # hotelsItem['star'] = response.xpath('//div[@class="hotels-hotel-review-overview-HighlightedAmenities__amenityItem--3E_Yg"]/div/text()').extract()[0]
        roomNum = response.xpath('//div[@class="ui_column is-12-mobile is-6-tablet"]/div[@class="sub_content"]/div[@class="textitem"]/text()').extract()
        if roomNum:
            hotelsItem['roomNum'] = roomNum[0]
        else:
            hotelsItem['roomNum'] = ''
        # hotelsItem['roomNum'] = response.xpath('//div[@class="ui_column is-12-mobile is-6-tablet"]/div[@class="sub_content"]/div[@class="textitem"]/text()').extract()[0]
        award = response.xpath('//div[@class="ui_column is-3 is-shown-at-desktop"]/div[@class="section_content"]/div[@class="sub_content"]/div[@class="prw_rup prw_common_location_badges"]/div[@class="sub_content badges is-shown-at-desktop"]/div[@class="badgeWrapper"]/span[@class="award award-coe"]/span[@class="ui_icon certificate-of-excellence"]/text()').extract()
        if award:
            hotelsItem['award'] = award[0]
        else:
            hotelsItem['award'] = ''
        # hotelsItem['award'] = response.xpath('//div[@class="ui_column is-3 is-shown-at-desktop"]/div[@class="section_content"]/div[@class="sub_content"]/div[@class="prw_rup prw_common_location_badges"]/div[@class="sub_content badges is-shown-at-desktop"]/div[@class="badgeWrapper"]/span[@class="award award-coe"]/span[@class="ui_icon certificate-of-excellence"]/text()').extract()[0]
        roomType = response.xpath('//div[@class="ui_column is-6-tablet is-hidden-mobile"]/div[@class="sub_content"]/div[@class="textitem"]/text()').extract()
        if roomType:
            hotelsItem['roomType'] = roomType[0]
        else:
            hotelsItem['roomType'] = ''
        # hotelsItem['roomType'] = response.xpath('//div[@class="ui_column is-6-tablet is-hidden-mobile"]/div[@class="sub_content"]/div[@class="textitem"]/text()').extract()[0]
        hotelsItem['hotelType'] = response.xpath('//div[@class="ui_column is-6-tablet is-hidden-mobile"]/div[@class="sub_content"]/div[@class="textitem style"]/text()').extract()
        print(hotelsItem['hotelType'])
        hotelsItem['website'] = response.xpath('//div[@class="blRow is-hidden-mobile "]/div[@class="is-hidden-mobile blEntry website ui_link btfAbout "]/@data-ahref').extract()
        hotelsItem['email'] = response.xpath('//div[@class="blRow is-hidden-mobile "]/div[@class="is-hidden-mobile blEntry email ui_link btfAbout"]/@data-olr').extract()
        print(hotelsItem['email'])
        # 这是一个数组
        hotelsItem['feature'] = response.xpath(
            '//div[@class="sub_content ui_columns is-multiline is-gapless is-mobile"]/div[@class="entry ui_column is-4-tablet is-6-mobile is-4-desktop"]/div[@class="textitem"]/text()').extract()
        print(hotelsItem['feature'])
        hotelsItem['introText'] = response.xpath('//div[@class="ui_column is-8-tablet is-3-desktop is-12-mobile rightSepDesktop"]/div[@class="prw_rup prw_common_responsive_collapsible_text"]/span/text()').extract()
        print("End hotels_parse_details!")
        nears = response.xpath('//div[@class="grids is-shown-at-tablet"]/div[@class="prw_rup prw_common_btf_nearby_poi_grid grid-widget"]/a/@href').extract()
        if nears:
            hotelsItem['hotelsNear'] = nears[0]
            hotelsItem['restaurantsNear'] = nears[1]
            hotelsItem['attractionsNear'] = nears[2]
        else:
            hotelsItem['hotelsNear'] = ''
            hotelsItem['restaurantsNear'] = ''
            hotelsItem['attractionsNear'] = ''

        yield scrapy.Request(hotelsItem['href'], meta={'hotelsItemPass': hotelsItem}, callback=self.hotel_comments_parse)

        yield hotelsItem

    def hotel_comments_parse(self,response):
        commentsItem = CommentsItem()
        hotelsItemPass = response.meta['hotelsItemPass']
        commentsItem['hotelId'] = hotelsItemPass['id']



