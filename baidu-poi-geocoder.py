# -*- coding:utf-8 -*-
# vim:fenc=utf-8

import os
import sys
#import rtree
import httplib
import json
import time
import copy
import logging
from osgeo import ogr
import time

# World Borders DataSet download from http://thematicmapping.org/downloads/world_borders.php
country_shape_file = "/home/root/baidu_poi/data/TM_WORLD_BORDERS-0.3.shp"
time_format = "%Y-%m-%d %X"
#lat_range = [18.1, 53.55]
#lng_range = [73.666667, 135.041667]
lng_lat_interval = 0.4
AK = "1111"
class BaiduPoi(object):

    def __init__(self, data_file, log_file, country_shape_file=country_shape_file):
        driver = ogr.GetDriverByName('ESRI Shapefile')
        self.country_file = driver.Open(country_shape_file)
        self.layer = self.country_file.GetLayer()
        self.china = self.layer.GetFeature(29)
        self.china_shape = self.china.GetGeometryRef()
        self.conn = httplib.HTTPConnection("api.map.baidu.com")
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

    def get_geocoder_poi(self, filename):
        with open(filename) as f:
            filelines = f.readlines()
            for line in filelines:      
                try:
                    arr = line.strip().split(',')
                    if self.is_in_china(round(float(arr[0]),0),round(float(arr[1]),0))==False:
                    	continue    
                    if len(arr)!=2:
                        continue
                    url = "/geocoder/v2/?ak=%s&location=%s,%s&output=json&pois=1&coordtype=wgs84ll" % (AK,arr[1],arr[0])
                    self.conn.request("GET", url)
                    if self.query_count%100==0:
                        logging.info('sleep 1s, %s',self.query_count)
                        time.sleep(2)
                    res = self.conn.getresponse()
                    if res.status == 200:
                        data = None
                        try:
                            data = res.read()
                            self.write_file(data)
                        except Exception,e:
                            logging.error('data error %s %s' % (data, e))
                    else :
                        self.conn = httplib.HTTPConnection("api.map.baidu.com")
                except Exception,e:
                    logging.error('get poi error %s' % e)
                    self.conn = httplib.HTTPConnection("api.map.baidu.com")
                self.query_count = self.query_count + 1


    def write_file(self, line):
        self.file_obj.write(line)
        self.file_obj.write('\n')

if __name__=="__main__":
    type = sys.argv[1]
    #print type
    hour = time.strftime("%Y%m%d%H", time.localtime(time.time()))
    if type == "geo":
        data_file = "/home/root/baidu_poi/baidu-map/base-lnglat-poi/%s.geo" %  hour
        log_file = "/home/root/baidu_poi/baidu-map/logs/log.%s.%s" % (type, hour)   
        baidu = BaiduPoi(data_file, log_file)
        baidu.get_geocoder_poi(sys.argv[2])
        baidu.file_obj.close()
    else:
        print "error type:%s" % type
