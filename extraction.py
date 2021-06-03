#!/usr/bin/env python3
from pymongo import MongoClient
from functools import reduce
import os
import gzip
import json
import pandas as pd
import csv

from pathlib import Path
from collections import OrderedDict

class Json2Mongo(object):
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 27017
        # 创建mongodb客户端
        self.client = MongoClient(self.host, self.port)

        dblist = self.client.list_database_names()
        if "tweet" not in dblist:
            # 创建数据库
            self.db = self.client.tweet

        collist = self.client["tweet"].list_collection_names()
        if "record" not in collist:
            # 创建集合tweet202001
            self.collection = self.client["tweet"].record

    # 从数据库读取
    def read_datebase(self, tid, tlv):
        try:
            myquery = {"qt_id_str": tid}  # 查询条件
            scene_flow = self.client["tweet"].record.find(myquery)
            for x in scene_flow:
                print(x)
                new_p_id = x['id_str']
                csv_writer.writerow(
                    [str(tid) + '\t', str(new_p_id) + '\t', '3', str(tlv + 1)])

                find_relation(new_p_id, tlv + 1)

        except Exception as e:
            print(e)

        try:
            myquery = {"rp_id_str": tid}  # 查询条件
            scene_flow = self.client["tweet"].record.find(myquery)
            for x in scene_flow:
                print(x)
                new_p_id = x['id_str']
                csv_writer.writerow(
                    [str(tid) + '\t', str(new_p_id) + '\t', '2', str(tlv + 1)])
                find_relation(new_p_id, tlv + 1)

        except Exception as e:
            print(e)

        try:
            myquery = {"rt_id_str": tid}  # 查询条件
            scene_flow = self.client["tweet"].record.find(myquery)
            for x in scene_flow:
                print(x)
                new_p_id = x['id_str']
                csv_writer.writerow(
                    [str(tid) + '\t', str(new_p_id) + '\t', '1', str(tlv + 1)])
                find_relation(new_p_id, tlv + 1)

        except Exception as e:
            print(e)


def find_relation(p_id, lv):
    jm.read_datebase(p_id, lv)

if __name__ == "__main__":
    jm = Json2Mongo()
    # 在dataframe查找
    id_file = pd.ExcelFile("tweetTongji-final.xlsx")
    data = id_file.parse('tweetNetInfo')
    for i in range(len(data)):
        print(str(data.iloc[i, 0]) + "-->" + str(data.iloc[i, 1]))
        # 写入csv文件的头部信息
        f = open(str(data.iloc[i, 0]) + "_network.csv", 'w', encoding='utf-8', newline='')
        csv_writer = csv.writer(f)
        csv_writer.writerow(['FromNodeId', 'ToNodeId', 'Weight', 'Level'])
        #
        find_relation(str(data.iloc[i, 0]), 0)
        #
        f.close()
