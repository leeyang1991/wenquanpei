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

def reverse_colourmap(cmap, name = 'my_cmap_r'):
    """
    In:
    cmap, name
    Out:
    my_cmap_r

    Explanation:
    t[0] goes from 0 to 1
    row i:   x  y0  y1 -> t[0] t[1] t[2]
                   /
                  /
    row i+1: x  y0  y1 -> t[n] t[1] t[2]

    so the inverse should do the same:
    row i+1: x  y1  y0 -> 1-t[0] t[2] t[1]
                   /
                  /
    row i:   x  y1  y0 -> 1-t[n] t[2] t[1]
    """
    reverse = []
    k = []

    for key in cmap._segmentdata:
        k.append(key)
        channel = cmap._segmentdata[key]
        data = []

        for t in channel:
            data.append((1-t[0],t[2],t[1]))
        reverse.append(sorted(data))

    LinearL = dict(zip(k,reverse))
    my_cmap_r = mpl.colors.LinearSegmentedColormap(name, LinearL)
    return my_cmap_r


def makeColours(vals,cmap,reverse=0):
    norm = []
    for i in vals:
        norm.append((i-np.min(vals))/(np.max(vals)-np.min(vals)))
    colors = []
    cmap = plt.get_cmap(cmap)
    if reverse:
        cmap = reverse_colourmap(cmap)
    else:
        cmap = cmap

    for i in norm:
        colors.append(cmap(i))
    return colors




def plot_scatter(val1,val2,title='',cmap='Spectral',reverse=1,s=15.):

    kde_val = np.array([val1,val2])
    print('doing kernel density estimation... ')
    densObj = kde(kde_val)
    # print(densObj)
    dens_vals = densObj.evaluate(kde_val)

    colors = makeColours(dens_vals,cmap,reverse=reverse)
    # print(colors)
    print('ploting...')
    # fig = plt.figure(figsize=(5,2))

    # set background color
    # ax = plt.gca()
    # ax.set_facecolor('black')

    if reverse:
        plt.title(title)
    else:
        plt.title(title)

    plt.scatter(val1,val2,c=colors,s=s)
    # x y lim

    min_v = min([min(val1),min(val2)])
    max_v = max([max(val1),max(val2)])
    if min_v == 0:
        plt.xlim((-3, max_v*1.1))
        plt.ylim((-3, max_v*1.1))
    else:
        plt.xlim((min_v-(max_v-min_v)*0.05, max_v+(max_v-min_v)*0.05))
        plt.ylim((min_v-(max_v-min_v)*0.05, max_v+(max_v-min_v)*0.05))
    # plt.ylim((min(val2), max(val2)))
    print('showing...')
    # plt.show()



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
        if i >= 7:
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
    # grid1 =
    flatten_arr = []
    for i in arr:
        for j in i:
            if not np.isnan(j):
                flatten_arr.append(j)
    return flatten_arr


def tif_to_arr(f):
    huazhong_tif = this_root + 'huazhong.tif'
    huazhong_arr, originX, originY, pixelWidth, pixelHeight = to_raster.raster2array(huazhong_tif)
    huazhong_arr = huazhong_arr[::-1]
    huazhong_arr = np.array(huazhong_arr)
    arr, originX, originY, pixelWidth, pixelHeight = to_raster.raster2array(f)
    arr = np.array(arr)
    grid = huazhong_arr > 100
    arr[np.logical_not(grid)] = np.nan
    flatten_arr = []
    for i in arr:
        for j in i:
            if not np.isnan(j):
                flatten_arr.append(j)
    return flatten_arr




def main():

    # tif1 = this_root+'corr\\r5d_krig1.tif'
    # tif2 = this_root+'corr\\rcp45_19812010_r5d1.tif'
    # array1,originX,originY,pixelWidth,pixelHeight = to_raster.raster2array(tif1)
    # array2,originX,originY,pixelWidth,pixelHeight = to_raster.raster2array(tif2)
    #
    # number1 = []
    # number2 = []
    # for i in array1:
    #     for j in i:
    #         number1.append(j)
    #
    # for i in array2:
    #     for j in i:
    #         number2.append(j)

    # f1 = this_root+u'源数据\\高温\\rcp45_19812010_SU35.asc'
    # f11 = this_root + u'源数据\\高温\\su35.tif'
    # print(f11)
    # number1 = acs_to_arr(f1)
    # number2 = tif_to_arr(f11)
    #
    # f2 = this_root+u'源数据\\高温\\rcp45_19812010_Txx.asc'
    # f22 = this_root+u'源数据\\高温\\txx.tif'
    # number1 = acs_to_arr(f2)
    # number2 = tif_to_arr(f22)
    # print(f22)

    f3 = this_root+u'源数据\\降水\\rcp45_19812010_r5d.asc'
    f33 = this_root+u'源数据\\降水\\r5.tif'
    number1 = acs_to_arr(f3)
    number2 = tif_to_arr(f33)
    # print(f33)

    # f4 = this_root+u'代码+源数据0902\\代码+源数据\\源数据\\高温\\rcp45_19812010_SU35.asc'
    # f44 = this_root + u'代码+源数据0902\\代码+源数据\\源数据\\高温new\\su35.tif'
    # title = 'su35'

    # f4 = this_root+u'代码+源数据0902\\代码+源数据\\源数据\\高温\\rcp45_19812010_Txx.asc'
    # f44 = this_root+u'代码+源数据0902\\代码+源数据\\源数据\\高温new\\txx.tif'
    title = 'txx'
    # number1 =
    # number1 = tif_to_arr(f44)
    # number2 = acs_to_arr(f4)
    # print(f44)



    number1 = np.array(number1)
    number2 = np.array(number2)

    # new = []
    # for i in number2:
    #     val = i+(np.random.random()*60)
    #     new.append(val)
    #     print(i)
    #     print(val)
    #     print()
    # exit()
    # number2 = new
    plt.figure(figsize=(6,6))
    # plot_scatter(number1,number2,title)
    plot_scatter(number1,number2,title)
    # plt.scatter(number1,number2)
    # plot_scatter(number1_new,number2_new,'pre')

    r = scipy.stats.pearsonr(number1,number2)
    print(r)
    plt.show()


if __name__ == '__main__':
    # shp = this_root+u'源数据\\华中三省边界\\huazhongsanshengxintouying.shp'
    # output = this_root+'test.tif'
    # x_min, y_min, x_res, y_res, pixel_width = 108,24,37,53,0.25
    # to_raster.rasterize_shp(shp,output,x_min,y_min,x_res,y_res,pixel_width)
    main()