# coding=utf-8

import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from matplotlib import pyplot as plt
this_root = u'D:\\PycharmProjects\\wenquanpei\\给小李20210225\\'
def pause():
    input('\33[7m'+"PRESS ENTER TO CONTINUE."+'\33[0m')
def mk_dir(dir, force=False):

    if not os.path.isdir(dir):
        if force == True:
            os.makedirs(dir)
        else:
            os.mkdir(dir)


def show_df_all_columns():
    pd.set_option('display.max_columns', None)
    pass

def print_head_n(df,n=10,pause_flag=0):
    show_df_all_columns()
    print(df.head(n))
    if pause_flag == 1:
        pause()

def variables():

    v = 'rdays	maxnrdays	SUM	PCD	PCP	N	R90	R95	R99	Rx1d	' \
        'Rx3d	Rx5d	Rx7d	Rx10d	Rx15d	Rx30d	特旱_spei	' \
        '重旱_spei	中旱_spei	轻旱_spei	无旱_spei	特旱	重旱	' \
        '中旱	轻旱	无旱	t	HDD0	HDD10	hdays0	hdays10	' \
        'tmax	tmaxdays35	tmaxdays37'

    v_split = v.split()
    return v_split


def get_shang_you():
    f = this_root + 'result\\sta_info\\shangyou.csv'

    df = pd.read_csv(f)
    sta = {}
    for i,row in tqdm(df.iterrows(),total=len(df)):
        lon = row.lon
        lat = row.lat
        key = (lon,lat)
        sta[key] = ''
    return sta

def get_xia_you():
    f = this_root + 'result\\sta_info\\xiayou.csv'
    df = pd.read_csv(f)
    sta = {}
    for i, row in tqdm(df.iterrows(), total=len(df)):
        lon = row.lon
        lat = row.lat
        key = (lon, lat)
        sta[key] = ''
    return sta


class Every_Model:

    def __init__(self):
        self.variable = variables()
        pass

    def run(self):
        # self.read_historical()
        # self.read_SSP245()
        self.read_SSP585()
        pass


    def read_historical(self):
        # region_pixs = get_shang_you()
        # outdir = this_root + 'result\\historical\\各模式逐年区域平均序列\\上游\\'

        region_pixs = get_xia_you()
        outdir = this_root + 'result\\historical\\各模式逐年区域平均序列\\中下游\\'


        fdir = this_root + u'长江流域要素\\historical\\'
        mk_dir(outdir,force=True)
        for f in os.listdir(fdir):
            outf = outdir + f
            fname = (fdir + f)
            print(fname)
            df = pd.read_csv(fdir + f,encoding='gbk')
            year_list = df.year

            year_list = list(set(year_list))
            year_list.sort()
            mean_dic = {}
            for y in tqdm(year_list):
                df_y = df[df['year']==y]
                indx = []
                for i,row in df_y.iterrows():
                    lon = row.lon
                    lat = row.lat
                    pix = (lon,lat)
                    if pix in region_pixs:
                        indx.append(i)
                df_y_region = df_y.drop(index=indx)

                result_list = []
                for v in self.variable:
                    try:
                        mean = df_y_region[v].mean()
                        result_list.append(mean)
                    except:
                        mean = ''
                        result_list.append(mean)
                mean_dic[y] = result_list
            text = ''
            for y in year_list:
                result = mean_dic[y]
                text_list = []
                for i in result:
                    text_list.append(str(i))
                text_i = str(y)+','+','.join(text_list) + '\n'
                text += text_i
            head = 'year,' +','.join(self.variable)+'\n'
            fw = open(outf,'w')
            fw.write(head)
            fw.write(text)
            fw.close()
            # exit()
        pass

    def read_SSP245(self):
        # region_pixs = get_shang_you()
        # outdir = this_root + 'result\\SSP245\\各模式逐年区域平均序列\\上游\\'

        region_pixs = get_xia_you()
        outdir = this_root + 'result\\SSP245\\各模式逐年区域平均序列\\中下游\\'


        fdir = this_root + u'长江流域要素\\SSP245\\'
        mk_dir(outdir,force=True)
        for f in os.listdir(fdir):
            outf = outdir + f
            fname = (fdir + f)
            print(fname)
            df = pd.read_csv(fdir + f,encoding='gbk')
            year_list = df.year

            year_list = list(set(year_list))
            year_list.sort()
            mean_dic = {}
            for y in tqdm(year_list):
                df_y = df[df['year']==y]
                indx = []
                for i,row in df_y.iterrows():
                    lon = row.lon
                    lat = row.lat
                    pix = (lon,lat)
                    if pix in region_pixs:
                        indx.append(i)
                df_y_region = df_y.drop(index=indx)

                result_list = []
                for v in self.variable:
                    try:
                        mean = df_y_region[v].mean()
                        result_list.append(mean)
                    except:
                        mean = ''
                        result_list.append(mean)
                mean_dic[y] = result_list
            text = ''
            for y in year_list:
                result = mean_dic[y]
                text_list = []
                for i in result:
                    text_list.append(str(i))
                text_i = str(y)+','+','.join(text_list) + '\n'
                text += text_i
            head = 'year,' +','.join(self.variable)+'\n'
            fw = open(outf,'w')
            fw.write(head)
            fw.write(text)
            fw.close()
            # exit()
        pass

    def read_SSP585(self):
        # region_pixs = get_shang_you()
        # outdir = this_root + 'result\\SSP585\\各模式逐年区域平均序列\\上游\\'

        region_pixs = get_xia_you()
        outdir = this_root + 'result\\SSP585\\各模式逐年区域平均序列\\中下游\\'


        fdir = this_root + u'长江流域要素\\SSP585\\'
        mk_dir(outdir,force=True)
        for f in os.listdir(fdir):
            outf = outdir + f
            fname = (fdir + f)
            print(fname)
            df = pd.read_csv(fdir + f,encoding='gbk')
            year_list = df.year

            year_list = list(set(year_list))
            year_list.sort()
            mean_dic = {}
            for y in tqdm(year_list):
                df_y = df[df['year']==y]
                indx = []
                for i,row in df_y.iterrows():
                    lon = row.lon
                    lat = row.lat
                    pix = (lon,lat)
                    if pix in region_pixs:
                        indx.append(i)
                df_y_region = df_y.drop(index=indx)

                result_list = []
                for v in self.variable:
                    try:
                        mean = df_y_region[v].mean()
                        result_list.append(mean)
                    except:
                        mean = ''
                        result_list.append(mean)
                mean_dic[y] = result_list
            text = ''
            for y in year_list:
                result = mean_dic[y]
                text_list = []
                for i in result:
                    text_list.append(str(i))
                text_i = str(y)+','+','.join(text_list) + '\n'
                text += text_i
            head = 'year,' +','.join(self.variable)+'\n'
            fw = open(outf,'w')
            fw.write(head)
            fw.write(text)
            fw.close()
            # exit()
        pass


class Every_Model_mean:

    def __init__(self):

        pass

    def run(self):
        # self.read_historical()
        # self.read_SSP245()
        self.read_SSP585()
        pass

    def read_historical(self):
        fdir = this_root + 'result\\historical\\各模式逐年区域平均序列\\'
        for region in os.listdir(fdir):
            outdir = this_root + 'result\\historical\\模式集合后逐年区域平均序列\\'+region+'\\'
            mk_dir(outdir,force=True)
            outf = outdir + '模式集合.csv'
            year_list = []
            df_list = []
            for f in os.listdir((fdir + region)):
                # print()
                # exit()
                fpath = os.path.join(fdir,region,f)
                df = pd.read_csv(fpath,encoding='gbk')
                df_list.append(df)
                years = df.year
                for y in years:
                    year_list.append(y)
            year_list = list(set(year_list))
            year_list.sort()
            # df_all = pd.DataFrame()
            # for df in df_list:
            df_all = pd.concat(df_list)
            mean_dic = {}
            for y in tqdm(year_list):
                df_y = df_all[df_all['year']==y]
                # print(df_y)
                result_list = []
                for v in Every_Model().variable:
                    try:
                        mean = df_y[v].mean()
                        result_list.append(mean)
                    except:
                        mean = ''
                        result_list.append(mean)
                mean_dic[y] = result_list

            text = ''
            for y in year_list:
                result = mean_dic[y]
                text_list = []
                for i in result:
                    text_list.append(str(i))
                text_i = str(y) + ',' + ','.join(text_list) + '\n'
                text += text_i
            head = 'year,' + ','.join(Every_Model().variable) + '\n'
            fw = open(outf, 'w')
            fw.write(head)
            fw.write(text)
            fw.close()

    def read_SSP245(self):
        fdir = this_root + 'result\\SSP245\\各模式逐年区域平均序列\\'
        for region in os.listdir(fdir):
            outdir = this_root + 'result\\SSP245\\模式集合后逐年区域平均序列\\'+region+'\\'
            mk_dir(outdir,force=True)
            outf = outdir + '模式集合.csv'
            year_list = []
            df_list = []
            for f in os.listdir((fdir + region)):
                # print()
                # exit()
                fpath = os.path.join(fdir,region,f)
                df = pd.read_csv(fpath,encoding='gbk')
                df_list.append(df)
                years = df.year
                for y in years:
                    year_list.append(y)
            year_list = list(set(year_list))
            year_list.sort()
            # df_all = pd.DataFrame()
            # for df in df_list:
            df_all = pd.concat(df_list)
            mean_dic = {}
            for y in tqdm(year_list):
                df_y = df_all[df_all['year']==y]
                # print(df_y)
                result_list = []
                for v in Every_Model().variable:
                    try:
                        mean = df_y[v].mean()
                        result_list.append(mean)
                    except:
                        mean = ''
                        result_list.append(mean)
                mean_dic[y] = result_list

            text = ''
            for y in year_list:
                result = mean_dic[y]
                text_list = []
                for i in result:
                    text_list.append(str(i))
                text_i = str(y) + ',' + ','.join(text_list) + '\n'
                text += text_i
            head = 'year,' + ','.join(Every_Model().variable) + '\n'
            fw = open(outf, 'w')
            fw.write(head)
            fw.write(text)
            fw.close()


    def read_SSP585(self):
        fdir = this_root + 'result\\SSP585\\各模式逐年区域平均序列\\'
        for region in os.listdir(fdir):
            outdir = this_root + 'result\\SSP585\\模式集合后逐年区域平均序列\\'+region+'\\'
            mk_dir(outdir,force=True)
            outf = outdir + '模式集合.csv'
            year_list = []
            df_list = []
            for f in os.listdir((fdir + region)):
                # print()
                # exit()
                fpath = os.path.join(fdir,region,f)
                df = pd.read_csv(fpath,encoding='gbk')
                df_list.append(df)
                years = df.year
                for y in years:
                    year_list.append(y)
            year_list = list(set(year_list))
            year_list.sort()
            # df_all = pd.DataFrame()
            # for df in df_list:
            df_all = pd.concat(df_list)
            mean_dic = {}
            for y in tqdm(year_list):
                df_y = df_all[df_all['year']==y]
                # print(df_y)
                result_list = []
                for v in Every_Model().variable:
                    try:
                        mean = df_y[v].mean()
                        result_list.append(mean)
                    except:
                        mean = ''
                        result_list.append(mean)
                mean_dic[y] = result_list

            text = ''
            for y in year_list:
                result = mean_dic[y]
                text_list = []
                for i in result:
                    text_list.append(str(i))
                text_i = str(y) + ',' + ','.join(text_list) + '\n'
                text += text_i
            head = 'year,' + ','.join(Every_Model().variable) + '\n'
            fw = open(outf, 'w')
            fw.write(head)
            fw.write(text)
            fw.close()

def main():
    # Every_Model().run()
    Every_Model_mean().run()
    pass


if __name__ == '__main__':
    main()