# -*- coding: utf-8 -*-
import scrapy

from hotels.items import CitysItem, HotelsItem, CommentsItem, RestaurantsNearItem, AttractionsNearItem, \
    HotelsNearItem


class TripadvisorhotelsSpider(scrapy.Spider):
    # 爬虫名称
    name = 'tripadvisorhotels'
    # 允许爬取的域名
    # allowed_domains = ['tripadvisor.com']
    # 爬虫入口爬取地址
    # start_urls = ['http://www.meijutt.com/new100.html']
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
            # print(citysItem['name'])
            # print(city.xpath('./@data-geoId').extract()[0])
            # print(citysItem['href'])
            yield citysItem
        print("End parse!")

        # 循环爬取翻页
        nextPage = \
        response.xpath('//div[@class="unified ui_pagination leaf_geo_pagination"]/a[text()="下一页"]/@href').extract()[0]
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

            hotelsCount = city.xpath('./div[@class ="info"]/span[@class="name"]/span[@class="count"]/text()').extract()
            if hotelsCount:
                citysItem['hotelsCount'] = hotelsCount[0]
            else:
                citysItem['hotelsCount'] = ''
            # citysItem['hotelsCount'] = city.xpath('./div[@class ="info"]/span[@class="name"]/span[@class="count"]/text()').extract()[0]
            yield scrapy.Request(citysItem['href'], meta={'citysItemPass': citysItem}, callback=self.hotels_parse)
            # print("遍历city")
            # print(city.xpath('./h5/a/@title').extract())
            # print(citysItem['name'])
            # print(city.xpath('./@data-geoId').extract()[0])
            # print(citysItem['href'])
            # print(citysItem['hotelsCount'])
            yield citysItem
        # print("End othercitys_parse!")

        # 循环爬取翻页
        nextPage = \
        response.xpath('//div[@class="unified ui_pagination leaf_geo_pagination"]/a[text()="下一页"]/@href').extract()[0]
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

    def hotels_parse(self, response):
        # print("Hello hotels_parse!")
        hotelList = response.xpath(
            '//div[@class="ui_column is-8 main_col allowEllipsis "]/div[@class="prw_rup prw_meta_hsx_listing_name listing-title"]/div[@class="listing_title"]/a')
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
            yield scrapy.Request(hotelsItem['href'], meta={'hotelsItemPass': hotelsItem},
                                 callback=self.hotels_parse_details)

            # print(hotelsItem['id'])
            # print(hotelsItem['href'])
            # print(hotelsItem['name'])
            # print(hotelsItem['city'])
            # print("退出了hotels_parse的for循环！")

        # 循环爬取网页
        nextPage = response.xpath(
            '//div[@class="unified ui_pagination standard_pagination ui_section listFooter"]/a[text()="下一页"]/@href').extract()
        # print(nextPage)
        # 爬取页数控制及末页控制
        if nextPage:
            if nextPage is not None:
                # 爬取页数控制值自增
                # self.count = self.count + 1
                # print("count++!!!")
                # 翻页请求
                yield scrapy.Request(self.base_url + nextPage[0], meta={'citysItemPass': citysItemPass},
                                     callback=self.hotels_parse)
        else:
            # 爬虫结束
            # print("爬虫结束")
            return None

        # print("End hotels_parse!")

    def hotels_parse_details(self, response):

        # print("Hello hotels_parse_details!")
        hotelsItemPass = response.meta['hotelsItemPass']
        # print("接收到了hotelsItemPass！")
        hotelsItem = HotelsItem()
        hotelsItem['id'] = hotelsItemPass['id']
        # print(hotelsItem['id'])
        hotelsItem['href'] = hotelsItemPass['href']
        hotelsItem['name'] = hotelsItemPass['name']
        # print(hotelsItem['name'])
        hotelsItem['cityHref'] = hotelsItemPass['cityHref']
        nameEn = response.xpath(
            '//div[@class="ui_column is-12-tablet is-10-mobile hotelDescription"]/h1/div/text()').extract()
        if nameEn:
            hotelsItem['nameEn'] = nameEn[0]
        else:
            hotelsItem['nameEn'] = ''
        # hotelsItem['nameEn'] = response.xpath('//div[@class="ui_column is-12-tablet is-10-mobile hotelDescription"]/h1/div/text()').extract()[0]
        # print(hotelsItem['nameEn'])
        rating = response.xpath('//div[@class="prw_rup prw_common_bubble_rating rating"]/span/@alt').extract()
        if rating:
            hotelsItem['rating'] = rating[0]
        else:
            hotelsItem['rating'] = ''
        # hotelsItem['rating'] = response.xpath('//div[@class="prw_rup prw_common_bubble_rating rating"]/span/@alt').extract()[0]
        # print(hotelsItem['rating'])
        comments = response.xpath('//span[@class="reviewCount "]/text()').extract()
        if comments:
            hotelsItem['comments'] = comments[0]
        else:
            hotelsItem['comments'] = ''
        # hotelsItem['comments'] = response.xpath('//span[@class="reviewCount "]/text()').extract()[0]
        # print(hotelsItem['comments'])
        rank = response.xpath('//b[@class="rank"]/text()').extract()
        if rank:
            hotelsItem['rank'] = rank[0]
        else:
            hotelsItem['rank'] = ''
        # hotelsItem['rank'] = response.xpath('//b[@class="rank"]/text()').extract()[0]
        # print(hotelsItem['rank'])
        address = response.xpath('//div[@class="hpCTAPlaceholder hidden"]/@data-address').extract()
        if address:
            hotelsItem['address'] = address[0]
        else:
            hotelsItem['address'] = ''
        # hotelsItem['address'] = response.xpath('//div[@class="hpCTAPlaceholder hidden"]/@data-address').extract()[0]
        addressSim = response.xpath(
            '//div[@class="ui_column is-12-mobile is-6-tablet"]/div[@class="sub_content"]/div[@class="textitem"]/text()').extract()
        if addressSim:
            hotelsItem['addressSim'] = ''
            # hotelsItem['addressSim'] = addressSim[1]
        else:
            hotelsItem['addressSim'] = ''
        # hotelsItem['addressSim'] = response.xpath('//div[@class="ui_column is-12-mobile is-6-tablet"]/div[@class="sub_content"]/div[@class="textitem"]/text()').extract()[1]
        # print(hotelsItem['addressSim'])
        photos = response.xpath(
            '//div[@class="hotels-media-album-parts-PhotoCount__textWrapper--30uL8"]/span[@class="is-hidden-tablet hotels-media-album-parts-PhotoCount__text--3OXuH"]/text()').extract()
        if photos:
            hotelsItem['photos'] = photos[0]
        else:
            hotelsItem['photos'] = ''
        # hotelsItem['photos'] = response.xpath('//div[@class="hotels-media-album-parts-PhotoCount__textWrapper--30uL8"]/span[@class="is-hidden-tablet hotels-media-album-parts-PhotoCount__text--3OXuH"]/text()').extract()[0]
        star = response.xpath(
            '//div[@class="hotels-hotel-review-overview-HighlightedAmenities__amenityItem--3E_Yg"]/div/text()').extract()
        if star:
            hotelsItem['star'] = star[0]
        else:
            hotelsItem['star'] = ''
        # hotelsItem['star'] = response.xpath('//div[@class="hotels-hotel-review-overview-HighlightedAmenities__amenityItem--3E_Yg"]/div/text()').extract()[0]
        roomNum = response.xpath(
            '//div[@class="ui_column is-12-mobile is-6-tablet"]/div[@class="sub_content"]/div[@class="textitem"]/text()').extract()
        if roomNum:
            hotelsItem['roomNum'] = roomNum[0]
        else:
            hotelsItem['roomNum'] = ''
        # hotelsItem['roomNum'] = response.xpath('//div[@class="ui_column is-12-mobile is-6-tablet"]/div[@class="sub_content"]/div[@class="textitem"]/text()').extract()[0]
        award = response.xpath(
            '//div[@class="ui_column is-3 is-shown-at-desktop"]/div[@class="section_content"]/div[@class="sub_content"]/div[@class="prw_rup prw_common_location_badges"]/div[@class="sub_content badges is-shown-at-desktop"]/div[@class="badgeWrapper"]/span[@class="award award-coe"]/span[@class="ui_icon certificate-of-excellence"]/text()').extract()
        if award:
            hotelsItem['award'] = award[0]
        else:
            hotelsItem['award'] = ''
        # hotelsItem['award'] = response.xpath('//div[@class="ui_column is-3 is-shown-at-desktop"]/div[@class="section_content"]/div[@class="sub_content"]/div[@class="prw_rup prw_common_location_badges"]/div[@class="sub_content badges is-shown-at-desktop"]/div[@class="badgeWrapper"]/span[@class="award award-coe"]/span[@class="ui_icon certificate-of-excellence"]/text()').extract()[0]
        roomType = response.xpath(
            '//div[@class="ui_column is-6-tablet is-hidden-mobile"]/div[@class="sub_content"]/div[@class="textitem"]/text()').extract()
        if roomType:
            hotelsItem['roomType'] = roomType[0]
        else:
            hotelsItem['roomType'] = ''
        # hotelsItem['roomType'] = response.xpath('//div[@class="ui_column is-6-tablet is-hidden-mobile"]/div[@class="sub_content"]/div[@class="textitem"]/text()').extract()[0]
        hotelsItem['hotelType'] = response.xpath(
            '//div[@class="ui_column is-6-tablet is-hidden-mobile"]/div[@class="sub_content"]/div[@class="textitem style"]/text()').extract()
        # print(hotelsItem['hotelType'])
        hotelsItem['website'] = response.xpath(
            '//div[@class="blRow is-hidden-mobile "]/div[@class="is-hidden-mobile blEntry website ui_link btfAbout "]/@data-ahref').extract()
        hotelsItem['email'] = response.xpath(
            '//div[@class="blRow is-hidden-mobile "]/div[@class="is-hidden-mobile blEntry email ui_link btfAbout"]/@data-olr').extract()
        # print(hotelsItem['email'])
        # 这是一个数组
        hotelsItem['feature'] = response.xpath(
            '//div[@class="sub_content ui_columns is-multiline is-gapless is-mobile"]/div[@class="entry ui_column is-4-tablet is-6-mobile is-4-desktop"]/div[@class="textitem"]/text()').extract()
        # print(hotelsItem['feature'])
        hotelsItem['introText'] = response.xpath(
            '//div[@class="ui_column is-8-tablet is-3-desktop is-12-mobile rightSepDesktop"]/div[@class="prw_rup prw_common_responsive_collapsible_text"]/span/text()').extract()

        # 附近的酒店、餐厅和景点
        nears = response.xpath(
            '//div[@class="grids is-shown-at-tablet"]/div[@class="prw_rup prw_common_btf_nearby_poi_grid grid-widget"]/a/@href').extract()

        yield hotelsItem

        if hotelsItem['href']:
            yield scrapy.Request(hotelsItem['href'], meta={'hotelsItemPass': hotelsItem},
                                 callback=self.hotel_comments_parse, dont_filter=True)
            print("调用了hotel_comments_parse")
        else:
            pass

        if nears:
            yield scrapy.Request(self.base_url + nears[0], meta={'hotelsItemPass': hotelsItem},
                                 callback=self.hotel_hotels_near_parse)
            yield scrapy.Request(self.base_url + nears[1], meta={'hotelsItemPass': hotelsItem},
                                 callback=self.hotel_restaurants_near_parse)
            yield scrapy.Request(self.base_url + nears[2], meta={'hotelsItemPass': hotelsItem},
                                 callback=self.hotel_attractions_near_parse)
        else:
            pass

        # print("End hotels_parse_details!")

    def hotel_comments_parse(self, response):

        print("Hello hotel_comments_parse")

        hotelsItemPass = response.meta['hotelsItemPass']
        commentList = response.xpath(
            '//div[@class="listContainer hide-more-mobile"]/div/div[@class="review-container"]')
        for comment in commentList:
            commentsItem = CommentsItem()
            commentsItem['commentHotelId'] = hotelsItemPass['id']
            commentId = comment.xpath(
                './div[@class="prw_rup prw_reviews_review_resp"]/div[@class="reviewSelector"]/@id').extract()
            if commentId:
                commentsItem['commentId'] = commentId[0]
            else:
                commentsItem['commentId'] = ''
            commentUserId = comment.xpath(
                './div[@class="prw_rup prw_reviews_review_resp"]/div[@class="reviewSelector"]/div[@class="rev_wrap ui_columns is-multiline "]/div[@class="ui_column is-2"]/div[@class="prw_rup prw_reviews_member_info_resp"]/div[@class="member_info"]/div[@class="memberOverlayLink clickable"]/@id').extract()
            if commentUserId:
                commentsItem['commentUserId'] = commentUserId[0]
            else:
                commentsItem['commentUserId'] = ''
            commentUserName = comment.xpath(
                './div[@class="prw_rup prw_reviews_review_resp"]/div[@class="reviewSelector"]/div[@class="rev_wrap ui_columns is-multiline "]/div[@class="ui_column is-2"]/div[@class="prw_rup prw_reviews_member_info_resp"]/div[@class="member_info"]/div[@class="memberOverlayLink clickable"]/div[@class="info_text"]/div/text()').extract()
            if commentUserName:
                commentsItem['commentUserName'] = commentUserName[0]
            else:
                commentsItem['commentUserName'] = ''
            commentUserProvin = comment.xpath(
                './div[@class="prw_rup prw_reviews_review_resp"]/div[@class="reviewSelector"]/div[@class="rev_wrap ui_columns is-multiline "]/div[@class="ui_column is-2"]/div[@class="prw_rup prw_reviews_member_info_resp"]/div[@class="member_info"]/div[@class="memberOverlayLink clickable"]/div[@class="info_text"]/div[@class="userLoc"]/strong/text()').extract()
            if commentUserProvin:
                commentsItem['commentUserProvin'] = commentUserProvin[0]
            else:
                commentsItem['commentUserProvin'] = ''
            checkInDate = comment.xpath(
                './div[@class="prw_rup prw_reviews_review_resp"]/div[@class="reviewSelector"]/div[@class="rev_wrap ui_columns is-multiline "]/div[@class="ui_column is-9"]/div[@class="prw_rup prw_reviews_stay_date_hsx"]/text()').extract()
            if checkInDate:
                commentsItem['checkInDate'] = checkInDate[0]
            else:
                commentsItem['checkInDate'] = ''
            commentDate = comment.xpath(
                './div[@class="prw_rup prw_reviews_review_resp"]/div[@class="reviewSelector"]/div[@class="rev_wrap ui_columns is-multiline "]/div[@class="ui_column is-9"]/span[@class="ratingDate"]/@title').extract()
            if commentDate:
                commentsItem['commentDate'] = commentDate[0]
            else:
                commentsItem['commentDate'] = ''
            commentBeThanksTimes = comment.xpath(
                './div[@class="prw_rup prw_reviews_review_resp"]/div[@class="reviewSelector"]/div[@class="rev_wrap ui_columns is-multiline "]/div[@class="ui_column is-9"]/div[@class="prw_rup prw_reviews_vote_line_hsx"]/div[@class="helpful redesigned hsx_helpful"]/span[@class="thankButton hsx_thank_button"]/span[@class="helpful_text"]/span[@class="numHelp emphasizeWithColor"]/text()').extract()
            if commentBeThanksTimes:
                commentsItem['commentBeThankTimes'] = commentBeThanksTimes[0]
            else:
                commentsItem['commentBeThankTimes'] = ''
            commentTitle = comment.xpath(
                './div[@class="prw_rup prw_reviews_review_resp"]/div[@class="reviewSelector"]/div[@class="rev_wrap ui_columns is-multiline "]/div[@class="ui_column is-9"]/div[@class="quote"]/a[@class="title "]/span/text()').extract()
            if commentTitle:
                commentsItem['commentTitle'] = commentTitle[0]
            else:
                commentsItem['commentTitle'] = ''
            commentContent = comment.xpath(
                './div[@class="prw_rup prw_reviews_review_resp"]/div[@class="reviewSelector"]/div[@class="rev_wrap ui_columns is-multiline "]/div[@class="ui_column is-9"]/div[@class="prw_rup prw_reviews_text_summary_hsx"]/div[@class="entry"]/p/text()').extract()
            if commentContent:
                commentsItem['commentContent'] = commentContent[0]
            else:
                commentsItem['commentContent'] = ''
            commentResponse = comment.xpath(
                './div[@class="prw_rup prw_reviews_review_resp"]/div[@class="reviewSelector"]/div[@class="rev_wrap ui_columns is-multiline "]/div[@class="ui_column is-9"]/div[@class="mgrRspnInline"]/div[@class="prw_rup prw_reviews_text_summary_hsx"]/div[@class="entry"]/p[@class="partial_entry"]/text()').extract()
            if commentResponse:
                commentsItem['commentResponse'] = commentResponse[0]
            else:
                commentsItem['commentResponse'] = ''

            # print(commentsItem)
            yield commentsItem

        # 循环爬取网页
        nextPage = response.xpath(
            '//div[@class="prw_rup prw_common_responsive_pagination"]/div[@class="unified ui_pagination "]/a[text()="下一页"]/@href').extract()
        # print(nextPage)
        # 爬取页数控制及末页控制
        if nextPage:
            if nextPage is not None:
                # 爬取页数控制值自增
                # 翻页请求
                yield scrapy.Request(self.base_url + nextPage[0], meta={'hotelsItemPass': hotelsItemPass},
                                     callback=self.hotel_comments_parse, dont_filter=True)
                # print("进入了递归的hotel_comments_parse")
                # print(self.base_url + nextPage[0])

        else:
            # 爬虫结束
            # print("爬虫结束")
            return None

        print("End hotel_comments_parse")

    def hotel_hotels_near_parse(self, response):

        # print("Hello hotel_hotels_near_parse")

        hotelsItemPass = response.meta['hotelsItemPass']

        hotelsNearList = response.xpath('//div[@class="ui_column is-8 main_col allowEllipsis "]')

        for hotel in hotelsNearList:
            hotelsNearItem = HotelsNearItem()
            hotelsNearItem['hotelId'] = hotelsItemPass['id']
            name = hotel.xpath(
                './div[@class="prw_rup prw_meta_hsx_listing_name listing-title"]/div[@class="listing_title"]/a/text()').extract()
            if name:
                hotelsNearItem['name'] = name[0]
            else:
                hotelsNearItem['name'] = ''
            distance = hotel.xpath(
                './div[@class="main-cols"]/div[@class="info-col"]/div[@class="distance linespace is-shown-at-mobile"]/div[@class="distWrapper"]/b/text()').extract()
            if distance:
                hotelsNearItem['distance'] = distance[0]
            else:
                hotelsNearItem['distance'] = ''

            yield hotelsNearItem

        # 循环爬取网页
        nextPage = response.xpath(
            '//div[@class="unified ui_pagination standard_pagination ui_section listFooter"]/a[text()="下一页"]/@href').extract()
        # print(nextPage)
        # 爬取页数控制及末页控制
        if nextPage:
            if nextPage is not None:
                # 爬取页数控制值自增
                # 翻页请求
                yield scrapy.Request(self.base_url + nextPage[0], meta={'hotelsItemPass': hotelsItemPass},
                                     callback=self.hotel_hotels_near_parse)
        else:
            # 爬虫结束
            # print("爬虫结束")
            return None

        # print("End hotel_hotels_near_parse")

    def hotel_restaurants_near_parse(self, response):

        # print("Hello hotel_restaurants_near_parse")

        hotelsItemPass = response.meta['hotelsItemPass']

        restaruantsNearList = response.xpath(
            '//div[@class="ppr_rup ppr_priv_restaurants_near_list"]/div[@class="near_listing"]')

        for restaurant in restaruantsNearList:
            restaruantsNearItem = RestaurantsNearItem()
            restaruantsNearItem['hotelId'] = hotelsItemPass['id']
            name = restaurant.xpath('./div[@class="location_name"]/a/text()').extract()
            if name:
                restaruantsNearItem['name'] = name[0]
            else:
                restaruantsNearItem['name'] = ''
            distance = restaurant.xpath(
                './div[@class="entry wrap"]/div[@class="description"]/div/div[@class="distance"]/b/text()').extract()
            if distance:
                restaruantsNearItem['distance'] = distance[0]
            else:
                restaruantsNearItem['distance'] = ''

            yield restaruantsNearItem

        # 循环爬取网页
        nextPage = response.xpath(
            '//div[@class="pagination"]/div[@class="pgLinks"]/a[@class="guiArw sprite-pageNext false"]/@href').extract()
        # print(nextPage)
        # 爬取页数控制及末页控制
        if nextPage:
            if nextPage is not None:
                # 爬取页数控制值自增
                # 翻页请求
                yield scrapy.Request(self.base_url + nextPage[0], meta={'hotelsItemPass': hotelsItemPass},
                                     callback=self.hotel_restaurants_near_parse)
        else:
            # 爬虫结束
            # print("爬虫结束")
            return None

        # print("End hotel_restaurants_near_parse")

    def hotel_attractions_near_parse(self, response):

        # print("Hello hotel_attractions_near_parse")

        hotelsItemPass = response.meta['hotelsItemPass']

        attractionsNearList = response.xpath(
            '//div[@class="ppr_rup ppr_priv_attractions_near_list"]/div[@class="near_listing_2017"]/div[@class="near_listing_content"]')

        for attraction in attractionsNearList:
            attractionsNearItem = AttractionsNearItem()
            attractionsNearItem['hotelId'] = hotelsItemPass['id']
            name = attraction.xpath('./div[@class="location_name"]/a/text()').extract()
            if name:
                attractionsNearItem['name'] = name[0]
            else:
                attractionsNearItem['name'] = ''

            distance = attraction.xpath(
                './div[@class="entry wrap"]/div[@class="description"]/div/div[@class="distance"]/b/text()').extract()
            if distance:
                attractionsNearItem['distance'] = distance[0]
            else:
                attractionsNearItem['distance'] = ''

            yield attractionsNearItem

        # 循环爬取网页
        nextPage = response.xpath(
            '//div[@class="pagination"]/div[@class="pgLinks"]/a[@class="guiArw sprite-pageNext false"]/@href').extract()
        # print(nextPage)
        # 爬取页数控制及末页控制
        if nextPage:
            if nextPage is not None:
                # 爬取页数控制值自增
                # 翻页请求
                yield scrapy.Request(self.base_url + nextPage[0], meta={'hotelsItemPass': hotelsItemPass},
                                     callback=self.hotel_attractions_near_parse)
        else:
            # 爬虫结束
            # print("爬虫结束")
            return None

        # print("End hotel_attractions_near_parse")
