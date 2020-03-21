#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os 

sys.path.append(os.path.abspath('scripts'))
from nyt_data import retrieve

repoUrl = 'https://github.com/oreillymedia/doing_data_science/'
fileUrl = 'raw/master/dds_datasets.zip'

#retrieve(repoUrl+fileUrl, 'raw_data')
print('Raw data files are successfully retrieved.')

import numpy as np
import pandas as pd
from nyt_data import traverse

summary_data = dict()
summary_data.setdefault("CTR", np.empty(31))
summary_data.setdefault("Clicks", np.empty(31))

def select_stats_unregistered(df, file_num):
    summary_data['CTR'][file_num] = df['CTR']['mean'][('Unknown', '0')]
    summary_data["Clicks"][file_num] = df["Clicks"]["sum"][('Unknown', '0')]
    

traverse('./raw_data', select_stats_unregistered)

print('Raw data files are successfully processed.')
df = pd.DataFrame.from_dict(summary_data)
import matplotlib.pyplot as plt

fig, axes = plt.subplots(nrows=2, ncols=1)
df['CTR'].plot(
        title='Click Through Rate Over 1 Month',
        ax=axes[0],
        figsize=(8, 9),
        xticks=[]
);

df['Clicks'].plot(
        xticks=range(0, 31, 2),
        title='Total Clicks Over 1 Month',
        ax=axes[1],
        figsize=(8, 9)
);