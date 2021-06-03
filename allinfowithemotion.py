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
def get_polarity(e_value):
    pol_value=''
    if e_value>=0.05:
        pol_value='Positive'
    elif e_value<0.05 and e_value>-0.05:
        pol_value = 'Neutral'
    else:
        pol_value = 'Negative'
    return pol_value


if __name__ == "__main__":
    dir = ['.']
    for data_dir in dir:
        for path in Path(data_dir).iterdir():
            if path.name.endswith('network.csv'):
                path_str = os.path.splitext(path)[0][0:-7]
                filename = path_str + 'tweetInfo.csv'
                to_file = path_str + 'mergeInfo.csv'

                df1 = pd.read_csv(path, header=0, usecols=['FromNodeId', 'ToNodeId', 'Weight', 'Level'],
                                  dtype={"FromNodeId": str, "ToNodeId": str})
                df2 = pd.read_csv(filename, header=0, dtype={"id_str": str, 'u_id': str})
                df2['emo_polarity']=df2["emotion_value"].map(get_polarity)

                outfile = pd.merge(df1, df2, left_on='ToNodeId',
                                   right_on='id_str')  # 文件合并 left_on是第一个DataFrame中的列或索引级别用作键。right_on 是第二个DataFrame中的列

                outfile.to_csv(to_file, index=False,
                               columns=['FromNodeId', 'ToNodeId', 'Weight', 'Level', 'created_at', 'emotion_value','emo_polarity',
                                        'u_id', 'origin'])  # 输出文件
