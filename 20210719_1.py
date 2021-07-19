# coding=utf-8
import sys

import matplotlib.pyplot as plt
from LY_Tools import *
version = sys.version_info.major
assert version == 3, 'Python Version Error'
import os
import shpbuffer as sb
from tqdm import tqdm
import pandas as pd
import codecs
this_root = '/Volumes/SSD/wenq/cmip5hubei20210716/'

def check_points_in_shp(shp,x,y):
    poly = sb.get_poly(shp)
    in_shp = sb.check_xys_in_poly(x,y,poly)
    return in_shp


def ascii_to_tif(father_folder='r85'):
    fdir = this_root + '/{}/'.format(father_folder)
    outdir = this_root + 'result/tif/{}/'.format(father_folder)
    T.mk_dir(outdir)
    for folder in T.list_dir(fdir):
        outdir_i = outdir + folder
        T.mk_dir(outdir_i)
        for f in T.list_dir(os.path.join(fdir,folder)):
            if not f.endswith('.txt'):
                continue
            if '-' in f:
                continue
            ascii_str = open(os.path.join(fdir,folder,f),'r').readlines()
            matrix = []
            for line in ascii_str:
                line_split = line.split('\n')[0]
                vals_str = line_split.split()
                vals = np.array(vals_str,dtype=float)
                matrix.append(vals)
            matrix = np.array(matrix)
            fname = f.split('.')[0] + '.tif'
            outf = os.path.join(outdir,outdir_i,fname)
            longitude_start, latitude_start, pixelWidth, pixelHeight, array = 108,24+0.25*len(matrix),0.25,-0.25,matrix
            to_raster.array2raster(outf,longitude_start, latitude_start, pixelWidth, pixelHeight, array)
    pass


def gen_mask_arr():
    shp = '/Volumes/SSD/wenq/给小李0716/湖北边界/hb_polygon.shp'
    outf = this_root + 'result/template/hb_matrix'
    tif = this_root + 'result/template/tif_template.tif'
    D = DIC_and_TIF(tif)
    lon_lat_dic = D.spatial_tif_to_lon_lat_dic()
    inshp_points = {}
    for pix in lon_lat_dic:
        lon,lat = lon_lat_dic[pix]
        is_in_shp = check_points_in_shp(shp,lon,lat)
        if is_in_shp:
            inshp_points[pix] = True
        else:
            inshp_points[pix] = False
    matrix = D.pix_dic_to_spatial_arr_ascii(inshp_points)
    matrix = np.array(matrix)
    np.save(outf,matrix)


def clip_tif(father_folder='r45'):
    fdir = this_root + 'result/tif/{}/'.format(father_folder)
    outdir = this_root + 'result/tif_clip/{}/'.format(father_folder)
    hb_matrix_f = this_root + 'result/template/hb_matrix.npy'
    hb_matrix = np.load(hb_matrix_f)
    T.mk_dir(outdir,force=True)
    for folder in T.list_dir(fdir):
        outdir_i = outdir + folder
        T.mk_dir(outdir_i)
        for f in T.list_dir(os.path.join(fdir, folder)):
            if not f.endswith('.tif'):
                continue
            tif_name = os.path.join(fdir, folder, f)
            arr = to_raster.raster2array(tif_name)[0]
            arr[np.logical_not(hb_matrix)] = -9999
            fname = f.split('.')[0] + '.tif'
            outf = os.path.join(outdir, outdir_i, fname)
            longitude_start, latitude_start, pixelWidth, pixelHeight, array = 108, 24 + 0.25 * len(
                arr), 0.25, -0.25, arr
            to_raster.array2raster(outf, longitude_start, latitude_start, pixelWidth, pixelHeight, array,ndv=-9999)

def tif_to_arr_text(father_folder='r85'):
    fdir = this_root + 'result/tif_clip/{}/'.format(father_folder)
    outdir = this_root + 'result/arr_clip/{}/'.format(father_folder)
    T.mk_dir(outdir, force=True)
    for folder in T.list_dir(fdir):
        outdir_i = outdir + folder
        T.mk_dir(outdir_i)
        for f in T.list_dir(os.path.join(fdir, folder)):
            if not f.endswith('.tif'):
                continue
            tif_name = os.path.join(fdir, folder, f)
            arr = to_raster.raster2array(tif_name)[0]
            arr_text = ''
            for i in arr:
                temp = ''
                for j in i:
                    temp += str(j) + '\t'
                arr_text += temp + '\n'
            fname = f.split('.')[0] + '.txt'
            outf = os.path.join(outdir, outdir_i, fname)
            fw = open(outf,'w')
            fw.write(arr_text)
            fw.close()
            # print(arr_text)
            # exit()
    pass

def cal_mean(father_folder='r45'):
    fdir = this_root + 'result/tif_clip/{}/'.format(father_folder)
    outdir = this_root + 'result/mean/{}/'.format(father_folder)
    T.mk_dir(outdir, force=True)
    for folder in T.list_dir(fdir):
        outdir_i = outdir + folder
        T.mk_dir(outdir_i)
        mean_list = []
        for f in T.list_dir(os.path.join(fdir, folder)):
            if not f.endswith('.tif'):
                continue
            tif_name = os.path.join(fdir, folder, f)
            arr = to_raster.raster2array(tif_name)[0]
            arr[arr<-999] = np.nan
            mean = np.nanmean(arr)
            mean_list.append(str(mean))
        mean_list_str = '\n'.join(mean_list)
        fname = folder + '.txt'
        outf = os.path.join(outdir, outdir_i, fname)
        fw = open(outf,'w')
        fw.write(mean_list_str)
        fw.close()

    pass

def period_mean(father_folder='r45',period=(2021,2050)):
    fdir = this_root + 'result/tif_clip/{}/'.format(father_folder)
    outdir = this_root + 'result/period_mean/{}/'.format(father_folder)
    T.mk_dir(outdir, force=True)
    start,end = period
    year_list = [str(i) for i in range(start,end + 1)]
    for folder in T.list_dir(fdir):
        outdir_i = outdir + folder
        T.mk_dir(outdir_i)
        arr_sum = 0.
        flag = 0.
        for f in T.list_dir(os.path.join(fdir, folder)):
            if not f.endswith('.tif'):
                continue
            year = f.split('.')[0].split('_')[1]
            if not year in year_list:
                continue
            tif_name = os.path.join(fdir, folder, f)
            arr = to_raster.raster2array(tif_name)[0]
            # arr[arr < -999] = np.nan
            arr_sum += arr
            flag += 1.
        mean_arr = arr_sum / flag
        mean_arr = np.array(mean_arr)
        arr_text = ''
        for i in mean_arr:
            temp = ''
            for j in i:
                temp += str(j) + '\t'
            arr_text += temp + '\n'
        fname = folder + '_{}_{}.txt'.format(start,end)
        outf = os.path.join(outdir, outdir_i, fname)
        fw = open(outf, 'w')
        fw.write(arr_text)
        fw.close()
        # exit()
    pass

def main():
    # ascii_to_tif()
    # gen_mask_arr()
    # clip_tif()
    # tif_to_arr_text()
    # cal_mean()
    period_mean()
    pass

if __name__ == '__main__':

    main()