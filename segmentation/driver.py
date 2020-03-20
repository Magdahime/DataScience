#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os 

sys.path.append(os.path.abspath('scripts'))
from nyt_data import retrieve

repoUrl = 'https://github.com/oreillymedia/doing_data_science/'
fileUrl = 'raw/master/dds_datasets.zip'

retrieve(repoUrl+fileUrl, 'raw_data')
print('Raw data files are successfully retrieved.')