# coding=gbk

import os
import numpy as np
from matplotlib import pyplot as plt
this_root = os.getcwd()+'\\..\\'
from scipy.stats import gaussian_kde as kde
import matplotlib as mpl
import seaborn as sns
import pandas as pd
import random
import to_raster
import scipy


def acs_to_arr(f):
    # f = this_root+u'源数据\\高温\\rcp45_19812010_SU35.asc'
    huazhong_tif = this_root+'huazhong.tif'
    huazhong_arr,originX,originY,pixelWidth,pixelHeight = to_raster.raster2array(huazhong_tif)
    huazhong_arr = huazhong_arr[::-1]
    huazhong_arr = np.array(huazhong_arr)
    fr = open(f,'r')
    lines = fr.readlines()

    i = 0
    arr = []
    for line in lines:
        i+=1
        line = line.split('\n')[0]
        line = line.split()
        # print(len(line))
        # exit()
        temp = []
        for val in line:
            temp.append(float(val))
        arr.append(temp)
    arr = np.array(arr)
    grid = huazhong_arr>100
    arr[np.logical_not(grid)] = np.nan
    # plt.imshow(arr)
    # plt.show()
    # grid1 =
    return arr


def main():
    fdir = r'F:\OneDrive - mail.bnu.edu.cn\临时存放\温泉沛\r50\\'
    # f = r'F:\OneDrive - mail.bnu.edu.cn\临时存放\温泉沛\r50\r50_1982.txt'
    mean_list = []
    std_list = []
    yearlist = []
    for f in os.listdir(fdir):
        # print f
        if f == r'r50-1980-2098.txt':
            continue
        year = f.split('.')[0].split('_')[1]
        yearlist.append(year)
        arr = acs_to_arr(fdir + f)
        mean = np.nanmean(arr)
        print '{}\t{}'.format(year,mean)
        std = np.nanstd(arr)
        mean_list.append(mean)
        std_list.append(std)
    mean_list = np.array(mean_list)
    std_list = np.array(std_list)
    plt.plot(mean_list,zorder=99,c='r')
    plt.fill_between(range(len(mean_list)),mean_list-std_list,mean_list+std_list,alpha=0.3,color='gray',interpolate=True,edgecolors='b')
    plt.xticks(range(len(mean_list))[::5],yearlist[::5],rotation=90)
    plt.tight_layout()
    plt.show()
    pass


if __name__ == '__main__':
    main()