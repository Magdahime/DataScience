# -*- coding: utf-8 -*-
import requests, zipfile, io, shutil
import pandas as pd
import numpy as np


unpackedFolder = '/dds_datasets/'
unpackedZipFile = 'dds_ch2_nyt.zip'

def retrieve(sourceFile, destinationFolder):
    def cleanup():
        try:
            shutil.rmtree(destinationFolder + unpackedFolder)
        except OSError as e:
            print("Folder: %s, Error: %s" % (e.filename,e.strerror))
    r = requests.get(sourceFile)
    assert r.status_code == requests.codes.ok
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(destinationFolder)
    # The top archive contains another ZIP file with our data.
    z = zipfile.ZipFile(destinationFolder + unpackedFolder +unpackedZipFile)
    z.extractall(destinationFolder)
    cleanup()
    
def q25(x):
   return x.quantile(0.25)

def q75(x):
    return x.quantile(0.75)
    
def summarize(data_file):
    #Read and parse the CSV data file
    nyt_data = pd.read_csv(data_file, dtype={'Gender':'category'})
    # segment users into age groups
    nyt_data["Age_group"] = pd.cut(nyt_data["Age"],
                                   bins=[-1, 0, 17, 24, 34, 44, 54, 64, 120],
                                   labels = ["Unknown",
                                             "1-17",
                                             "18-24",
                                             "25-34",
                                             "35-44",
                                             "45-54",
                                             "55-64",
                                             "65+"])
    nyt_data.drop("Age", axis='columns', inplace=True)
    nyt_data["CTR"] = nyt_data["Clicks"]/nyt_data['Impressions']
    nyt_data.dropna(inplace=True)
    nyt_data.drop((nyt_data['Clicks'] > nyt_data['Impressions']).to_numpy().nonzero()[0],
                  inplace=True)
    compressed_nyt_data = nyt_data.groupby(by=['Age_group', 'Gender'])[['CTR','Clicks']].agg([np.mean, np.std, np.max, q25, np.median,q75, np.sum])
    return compressed_nyt_data

import pathlib



def traverse(sourceFolder, collect):
    def get_file_number(data_file):
        return int(data_file.name[3:-4]) - 1
    for data_file in pathlib.Path(sourceFolder).glob('∗.csv'):
        print("Collecting data")
        collect(summarize(data_file.absolute()), get_file_number(data_file))

    