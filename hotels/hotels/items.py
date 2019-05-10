# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelsItem(scrapy.Item):
    # define the fields for your item here like:
    cityHref = scrapy.Field()
    id = scrapy.Field()
    href = scrapy.Field()
    name = scrapy.Field()
    nameEn = scrapy.Field()
    rating = scrapy.Field()
    comments = scrapy.Field()
    rank = scrapy.Field()
    address = scrapy.Field()
    addressSim = scrapy.Field()
    photos = scrapy.Field()
    # 这是一个数组
    feature = scrapy.Field()
    star = scrapy.Field()
    roomNum = scrapy.Field()
    award = scrapy.Field()
    # 这是一个数组
    introText = scrapy.Field()
    roomType = scrapy.Field()
    # 这是一个数组
    hotelType = scrapy.Field()
    # 这是一个数组
    website = scrapy.Field()
    # 这是一个数组
    email = scrapy.Field()
    hotelsNear = scrapy.Field()
    restaurantsNear = scrapy.Field()
    attractionsNear = scrapy.Field()


class CitysItem(scrapy.Item):
    name = scrapy.Field()
    href = scrapy.Field()
    hotelsCount = scrapy.Field()


class CommentsItem(scrapy.Item):
    commentId = scrapy.Field()
    commentHotelId = scrapy.Field()
    checkInDate = scrapy.Field()
    commentDate = scrapy.Field()
    commentUserId = scrapy.Field()
    commentUserName = scrapy.Field()
    commentUserProvin = scrapy.Field()
    commentBeThankTimes = scrapy.Field()
    commentTitle = scrapy.Field()
    commentContent = scrapy.Field()
    commentResponse = scrapy.Field()


class HotelsNearItem(scrapy.Item):
    hotelId = scrapy.Field()
    name = scrapy.Field()
    distance = scrapy.Field()


class RestaurantsNearItem(scrapy.Item):
    hotelId = scrapy.Field()
    name = scrapy.Field()
    distance = scrapy.Field()


class AttractionsNearItem(scrapy.Item):
    hotelId = scrapy.Field()
    name = scrapy.Field()
    distance = scrapy.Field()
