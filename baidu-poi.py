#!/usr/bin/python
# -*- coding:utf-8 -*-
# vim:fenc=utf-8

import os
import sys
#import rtree
import httplib
import json
import time
import copy
import pandas as pd
import numpy as np
import logging
from osgeo import ogr
import time

# World Borders DataSet download from http://thematicmapping.org/downloads/world_borders.php
country_shape_file = "/home/test/baidu_poi/data/TM_WORLD_BORDERS-0.3.shp"
time_format = "%Y-%m-%d %X"
#lat_range = [18.1, 53.55]
#lng_range = [73.666667, 135.041667]
lng_lat_interval = 0.4
AK = "zLu6ZGTuNZfkksbTSDpa1etc"
#AK = "3YaGMTqh4HyVbU71Ozzla5v9"
class BaiduPoi(object):

    def __init__(self, data_file, log_file, poi_tag_file, country_shape_file=country_shape_file):
        driver = ogr.GetDriverByName('ESRI Shapefile')
        self.country_file = driver.Open(country_shape_file)
        self.layer = self.country_file.GetLayer()
        self.china = self.layer.GetFeature(29)
        self.china_shape = self.china.GetGeometryRef()
        self.conn = httplib.HTTPConnection("api.map.baidu.com")
        self.poi_tag = pd.read_csv(poi_tag_file, header=None)
        self.poi_tag.columns=['tag']
        self.query_count = 0
        self.file_obj = open(data_file, "w+")
        logging.basicConfig(level=logging.INFO, filename=log_file, format="%(asctime)s %(message)s")

    @staticmethod
    def create_point(lng, lat):
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(lng, lat)
        return point

    def is_in_china(self, lng, lat):
        return self.china_shape.Contains(self.create_point(lng, lat))

    def get_poi(self, uid, lng, lat):
        try:
            url = "/geocoder/v2/?ak=%s&location=%s,%s&output=json&pois=1" % (AK,lat,lng)
            self.conn.request("GET", url)
            if self.query_count%100==0:
                logging.info('sleep 1s, %s',self.query_count)
                time.sleep(1)
            res = self.conn.getresponse()
            if res.status == 200:
                data = None
                try:
                    data = res.read()
                    self.write_file('%s##%s' % (uid,data))
                except Exception,e:
                    logging.error('data error %s %s' % (data, e))
            else :
                self.conn = httplib.HTTPConnection("api.map.baidu.com")
                self.get_poi(lng,lat) 
        except Exception,e:
            logging.error('get poi error %s' % e)
            self.conn = httplib.HTTPConnection("api.map.baidu.com")
            self.get_poi(lng,lat)   
    
    def get_poi_wgs(self, uid, lng, lat):
        try:
            url = "/geocoder/v2/?ak=%s&location=%s,%s&output=json&pois=1&coordtype=wgs84ll" % (AK,lat,lng)
            self.conn.request("GET", url)
            if self.query_count%100==0:
                logging.info('sleep 1s, %s',self.query_count)
                time.sleep(1)
            res = self.conn.getresponse()
            if res.status == 200:
                data = None
                try:
                    data = res.read()
                    self.write_file('%s##%s' % (uid,data))
                except Exception,e:
                    logging.error('data error %s %s' % (data, e))
            else :
                self.conn = httplib.HTTPConnection("api.map.baidu.com")
                self.get_poi(lng,lat) 
        except Exception,e:
            logging.error('get poi error %s' % e)
            self.conn = httplib.HTTPConnection("api.map.baidu.com")
            self.get_poi(lng,lat)   

    def get_bounds_poi_first_page(self, keyword, lng1, lat1, lng2, lat2):
        try :
            url = "/place/v2/search?ak=%s&query=%s&bounds=%s,%s,%s,%s&output=json&page_size=20&scope=2" % (AK,keyword,lat1,lng1,lat2,lng2)
            self.conn.request("GET", url)
            res = self.conn.getresponse()
            self.query_count += 1
            logging.info(" status:%s page:0" % res.status)
            if res.status == 200:
                data = res.read()
                json_data = json.loads(data)
                total = json_data['total']
                if total > 0 and total != 400:
                    # page 0
                    result = json.loads(data)['results']
                    if result:
                        for poi in result:
                            line = "%s##%s" % (keyword, json.dumps(poi))
                            self.write_file(line)
                    #other page
                    #self.write_file('%s##%s' % (keyword,json.dumps(data)))
                    page = total / 20
                    if total % 20 != 0:
                        page += 1
                    for i in range(1,page):
                        self.get_bounds_poi_page_num(keyword, lng1, lat1, lng2, lat2, i)
                logging.info("%s %s,%s,%s,%s %s %s" % (keyword, lat1, lng1, lat2, lng2, total, self.query_count))
            else:
                logging.info("reconnection server")
                self.conn = httplib.HTTPConnection("api.map.baidu.com")
                self.get_bounds_poi_first_page(keyword, lng1, lat1, lng2, lat2)
        except Exception,e:
            print e

    def get_bounds_poi_page_num(self, keyword, lng1, lat1, lng2, lat2, page_num):
        try :
            url = "/place/v2/search?ak=%s&query=%s&bounds=%s,%s,%s,%s&output=json&page_size=20&scope=2&page_num=%d" % (AK,keyword,lat1,lng1,lat2,lng2,page_num)
            #logging.info(url)
            self.conn.request("GET", url)
            res = self.conn.getresponse()
            self.query_count += 1
            logging.info(" status:%s page:%s" % ( res.status, page_num))
            if res.status == 200:
                data = res.read() 
                #self.write_file('%s##%s' % (keyword,json.dumps(data)))
                result = json.loads(data)['results']
                if result:
                    for poi in result:
                        line = "%s##%s" % (keyword, json.dumps(poi))
                        self.write_file(line)
            else:
                logging.info("reconnection server")
                self.conn = httplib.HTTPConnection("api.map.baidu.com")
                self.get_bounds_poi_page_num(keyword, lng1, lat1, lng2, lat2, page_num)
        except Exception,e:
            print e

    def write_file(self, line):
        self.file_obj.write(line)
        self.file_obj.write('\n')

    @staticmethod
    def get_lat_range(lat_range):
        return np.arange(lat_range[0], lat_range[1], lng_lat_interval)

    @staticmethod
    def get_lng_range(lng_range):
        return np.arange(lng_range[0], lng_range[1], lng_lat_interval)

    def get_baidu_poi(self,cood_file):
        with open(cood_file) as f:
            lines = f.readlines()
            for line in lines:
                try:
                    arr = line.strip().split(' ')
                    uid = arr[0]
                    lnglat = arr[1].split(',')
                    self.get_poi(uid, lnglat[0], lnglat[1])
                    self.query_count+=1
                except Exception,e:
                    logging.error("line error %s" % e)
            logging.info("total %s" % self.query_count) 
    
    def get_baidu_poi_wgs(self,cood_file):
        with open(cood_file) as f:
            lines = f.readlines()
            for line in lines:
                try:
                    lnglat = line.strip().split(',')
                    uid='1'
                    self.get_poi_wgs(uid, lnglat[0], lnglat[1])
                    self.query_count+=1
                except Exception,e:
                    logging.error("line error %s" % e)
            logging.info("total %s" % self.query_count) 

    def get_bounds_poi(self, keyword, lat_range, lng_range):
        lat1 = lat_range[0]
        while lat1 <= lat_range[1]:
            lng1 = lng_range[0]
            lat2 = lat1 + lng_lat_interval
            while lng1 <= lng_range[1]:
                lng2 = lng1 + lng_lat_interval
                is_china = self.is_in_china(lng1, lat1)
                if is_china:
                    self.get_bounds_poi_first_page(keyword, lng1, lat1, lng2, lat2)
                lng1 = lng2
            lat1 = lat2

    def get_poi_loop_tag(self, lat_range, lng_range):
        for key in self.poi_tag['tag']:
            #logging.info(key)
            #logging.info(lng_lat_interval)
            _lat = copy.deepcopy(lat_range)
            _lng = copy.deepcopy(lng_range)
            self.get_bounds_poi(key, _lat, _lng)

    def loop_lnglat_getpoi(self, poly_file):
        f = open(poly_file)
        lines = f.readlines()
        for line in lines:
            logging.info(line)
            lng_lat = line.strip().split(',')
            lats = [float(lng_lat[0]),float(lng_lat[2])]
            lngs = [float(lng_lat[1]),float(lng_lat[3])]
            self.get_poi_loop_tag(lats, lngs)           
    
    def loop_lnglat_getpoi2(self, poly_file):
        f = open(poly_file)
        lines = f.readlines()
        for line in lines:
            logging.info(line)
            arr = line.strip().split(' ')
            lng_lat = arr[1].split(',')
            lats = [float(lng_lat[0]),float(lng_lat[2])]
            lngs = [float(lng_lat[1]),float(lng_lat[3])]
            self.get_bounds_poi(arr[0], lats, lngs)    
    

if __name__=="__main__":
    keyword_type = sys.argv[1]
    print keyword_type
    time_stamp = int(time.time())
    poi_tag_file = "/home/test/baidu_poi/polygon/keyword"
    data_file = "/home/test/baidu_poi/polygon/data/%s.%s" % (keyword_type, time_stamp)
    log_file = "/home/test/baidu_poi/polygon/logs/log.%s.%s" % (keyword_type, time_stamp)
    if keyword_type == "k1111":
        lng_lat_interval = 0.02
        poly_file = sys.argv[2]
        baidu = BaiduPoi(data_file, log_file, poi_tag_file)
        baidu.loop_lnglat_getpoi(poly_file)
        baidu.file_obj.close()
    if keyword_type == "k2":
        k24_lat = [20.7,50.2]
        k24_lng = [73.6,105.2]
        baidu = BaiduPoi(data_file, log_file, poi_tag_file)
        baidu.get_poi_loop_tag(k24_lat, k24_lng)
        baidu.file_obj.close()  
    if keyword_type == "k3":
        k24_lat = [17.8,53.7]
        k24_lng = [105,135.4]
        baidu = BaiduPoi(data_file, log_file, poi_tag_file)
        baidu.get_poi_loop_tag(k24_lat, k24_lng)
        baidu.file_obj.close()  
    if keyword_type == "k4":
        lng_lat_interval = 0.1
        poly_file = sys.argv[2]
        baidu = BaiduPoi(data_file, log_file, poi_tag_file)
        baidu.loop_lnglat_getpoi2(poly_file)
        baidu.file_obj.close()
    if keyword_type == "geo":
        cood_file = sys.argv[2]
        baidu = BaiduPoi(data_file, log_file,poi_tag_file)
        baidu.get_baidu_poi(cood_file)
        baidu.file_obj.close()
    if keyword_type == "wgs":
        cood_file = sys.argv[2]
        baidu = BaiduPoi(data_file, log_file,poi_tag_file)
        baidu.get_baidu_poi_wgs(cood_file)
        baidu.file_obj.close()
    else:
        print "other location"
