# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql as pymysql

from hotels.items import CitysItem, HotelsItem


class HotelsPipeline(object):

    def __init__(self):
        self.connect = pymysql.connect(host='114.116.15.154', user='root', password='fe1e796b07d35484', db='tripadvisor_yitsu', port=3306)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        # print("进入了Pipeline！！！")
        if isinstance(item, CitysItem):
            print("是CitysItem类型！！")
            # with open("citysItem.txt", 'a') as fp:
            #     fp.write(item['name'].encode("utf8") + '\n')
            #     print("写入了name数据到citysItem.txt中！")
            #     return item
            # res = dict(item)
            # name = res['name']
            # hotelsCount = res['hotelsCount']
            # self.file.write(name+' ')
            # self.file.write(hotelsCount + '\n')
            # print("写入了name数据到citysItem.txt中!")
            self.cursor.execute(
                'insert into citys(city_code,city_name,hotels_num)VALUES("{}","{}","{}")'.format(item['href'],
                                                                                                 item['name'],
                                                                                                 item['hotelsCount']))
            self.connect.commit()
            return item
        if isinstance(item, HotelsItem):
            print("是HotelsItem类型！！")
            self.cursor.execute(
                'insert into hotels(city_code, id, name, name_en, price_low, price_site, rating, comments, rank, address, address_sim, photos, feature, star, room_num, award, intro_text, room_type, hotel_type, website, email)VALUES("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(item['cityHref'],
                                                                                                 item['id'],
                                                                                                 item['name'],
                                                                                                 item['nameEn'],
                                                                                                 '',
                                                                                                 '',
                                                                                                 item['rating'],
                                                                                                 item['comments'],
                                                                                                 item['rank'],
                                                                                                 item['address'],
                                                                                                 item['addressSim'],
                                                                                                 item['photos'],
                                                                                                 item['feature'],
                                                                                                 item['star'],
                                                                                                 item['roomNum'],
                                                                                                 item['award'],
                                                                                                 item['introText'],
                                                                                                 item['roomType'],
                                                                                                 item['hotelType'],
                                                                                                 item['website'],
                                                                                                 item['email']))
            self.connect.commit()
            return item
            # res = dict(item)
            # name = res['name']
            # id = res['id']
            # nameEn = res['nameEn']
            # self.file.write(name + ' ' + id + ' ' + nameEn + ' ' + '\n')


    def open_spider(self,spider):
        # self.file = open('citysItem.txt', 'w', encoding='utf-8')
        pass

    def close_spider(self,spider):
        self.cursor.close()
        self.connect.close()


