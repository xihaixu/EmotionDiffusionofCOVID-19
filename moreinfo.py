#!/usr/bin/env python3

import os
import pandas as pd
import numpy as np

from pathlib import Path
import gzip
import json
import csv

from datetime import datetime
from datetime import timedelta

data_dirs = ['2020-01', '2020-02', '2020-03', '2020-04', '2020-05']


def main():
    for data_dir in data_dirs:
        for path in Path(data_dir).iterdir():
            if path.name.endswith('.gz'):
                print('handling {}'.format(path))
                if not path.is_file():
                    print('the json file not exists: {}'.format(path))
                    return

                write_csv(path)  # 写入csv时，加\t避免数字以科学计数法输出


def write_csv(id_file):
    with gzip.open(id_file, 'r') as pf:
        # 转换为dict
        for line in pf:
            line_data = json.loads(line)
            if line_data["id_str"] + "\t" in df_dic:
                level = df_dic[line_data["id_str"] + "\t"]
                origin = ""
                e_value = calc_emotion(handleextra(line_data['full_text']))
                if line_data["in_reply_to_status_id_str"] is not None:
                    origin += " reply"
                if line_data.__contains__('retweeted_status'):
                    origin += " retweet"
                if line_data.__contains__('quoted_status'):
                    origin += " quoted"

                csv_writer.writerow(
                    [CTS2BJS(line_data['created_at']) + '\t', line_data['id_str'] + '\t',
                     line_data['full_text'] + '\t', str(e_value) + '\t', str(line_data["retweet_count"]) + '\t',
                     str(line_data["favorite_count"]) + '\t', line_data["user"]["id_str"] + '\t',
                     line_data["user"]["name"] + '\t', line_data["user"]["created_at"] + '\t',
                     str(line_data["user"]["followers_count"]) + '\t',
                     str(line_data["user"]["friends_count"]) + '\t',
                     str(line_data["user"]["favourites_count"]) + '\t',
                     str(line_data["user"]["statuses_count"]) + "\t",
                     origin + "\t", level])


import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# 去除特殊字符
def handleextra(txt):
    txt = re.sub('https?://[a-zA-Z0-9.?/&=:]*', "", txt)
    txt = re.sub('[,\.()":;!#$%^&*\d]|\'s|\'', '', txt)
    txt = re.sub('@[a|A-z|1-9]+', "", txt)
    return txt.replace('\n', ' ').replace("   ", " ").replace('RT ', '')


# 计算情感值
def calc_emotion(txt):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(txt)['compound']


def CTS2BJS(CTS):
    CTS_format = "%a %b %d %H:%M:%S +0000 %Y"
    BJS_format = "%Y-%m-%d %H:%M:%S"
    CTS = datetime.strptime(CTS, CTS_format)
    # 格林威治时间+8小时变为北京时间
    BJS = CTS + timedelta(hours=8)
    BJS = BJS.strftime(BJS_format)
    return BJS

if __name__ == "__main__":
    dir = ['.']
    for data_dir in dir:
        for path in Path(data_dir).iterdir():
            if path.name.endswith('network.csv'):
                df = pd.read_csv(path, header=0, usecols=["ToNodeId", "Level"],
                                 dtype={"ToNodeId": str})
                df_dic = df[["ToNodeId", "Level"]].set_index("ToNodeId").to_dict()["Level"]

                path_str = os.path.splitext(path)[0][0:-7]
                filename = path_str + 'tweetInfo.csv'

                f = open(filename, 'w', encoding='utf-8-sig', newline='')
                csv_writer = csv.writer(f)
                csv_writer.writerow(
                    ["created_at", "id_str", "full_text", "emotion_value", "retweet", "t_favorite_c", "u_id", "u_name",
                     "u_createtime", "follower", "friend", "favorite", "status", "origin", "level"])

                main()