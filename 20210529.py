# coding=utf-8
import sys
version = sys.version_info.major
assert version == 3, 'Python Version Error'
import os
from tqdm import tqdm
import pandas as pd
import codecs
this_root = '/Volumes/SSD/wenq/给小李0526/'


def mk_dir(dir, force=False):
    if not os.path.isdir(dir):
        if force == True:
            os.makedirs(dir)
        else:
            os.mkdir(dir)

def variables():
    f = '/Volumes/SSD/wenq/给小李0526/要素.txt'
    fr = open(f,'r')
    line = fr.readline()
    v_split = line.split()

    # print(v_split)
    # v = 'rdays	maxnrdays	SUM	PCD	PCP	N	R90	R95	R99	Rx1d	' \
    #     'Rx3d	Rx5d	Rx7d	Rx10d	Rx15d	Rx30d	特旱_spei	' \
    #     '重旱_spei	中旱_spei	轻旱_spei	无旱_spei	特旱	重旱	' \
    #     '中旱	轻旱	无旱	t	HDD0	HDD10	hdays0	hdays10	' \
    #     'tmax	tmaxdays35	tmaxdays37'
    #
    # v_split = v.split()
    # print(v_split)
    # exit()

    return v_split


def get_shang_you():
    f = this_root + 'result/sta_info/shangyou.csv'

    df = pd.read_csv(f)
    sta = {}
    for i,row in tqdm(df.iterrows(),total=len(df)):
        lon = row.lon
        lat = row.lat
        key = (lon,lat)
        sta[key] = ''
    return sta

def get_xia_you():
    f = this_root + 'result/sta_info/xiayou.csv'
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
        self.read_historical()
        self.read_SSP245()
        self.read_SSP585()
        pass


    def read_historical(self):
        # region_pixs = get_shang_you()
        # outdir = this_root + 'result/historical/各模式逐年区域平均序列/上游/'
        #
        region_pixs = get_xia_you()
        outdir = this_root + 'result/historical/各模式逐年区域平均序列/中下游/'


        fdir = this_root + 'cmip6数据/historical/'
        mk_dir(outdir,force=True)
        for f in os.listdir(fdir):
            if f.startswith('.'):
                continue
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
            # print(head)
            # exit()
            # head = head.encode('gbk')
            fw = codecs.open(outf,'w',encoding='gbk')
            # fw = open(outf,'w')
            fw.write(head)
            fw.write(text)
            fw.close()
            # exit()
        pass

    def read_SSP245(self):
        # region_pixs = get_shang_you()
        # outdir = this_root + 'result/SSP245/各模式逐年区域平均序列/上游/'
        #
        region_pixs = get_xia_you()
        outdir = this_root + 'result/SSP245/各模式逐年区域平均序列/中下游/'


        fdir = this_root + u'cmip6数据/SSP245/'
        mk_dir(outdir,force=True)
        for f in os.listdir(fdir):
            if f.startswith('.'):
                continue
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
            # fw = open(outf,'w')
            fw = codecs.open(outf, 'w', encoding='gbk')
            fw.write(head)
            fw.write(text)
            fw.close()
            # exit()
        pass

    def read_SSP585(self):
        # region_pixs = get_shang_you()
        # outdir = this_root + 'result/SSP585/各模式逐年区域平均序列/上游/'
        #
        region_pixs = get_xia_you()
        outdir = this_root + 'result/SSP585/各模式逐年区域平均序列/中下游/'


        fdir = this_root + u'cmip6数据/SSP585/'
        mk_dir(outdir,force=True)
        for f in os.listdir(fdir):
            if f.startswith('.'):
                continue
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
            # fw = open(outf,'w')
            fw = codecs.open(outf, 'w', encoding='gbk')
            fw.write(head)
            fw.write(text)
            fw.close()
            # exit()
        pass

class Every_Model_mean:

    def __init__(self):

        pass

    def run(self):
        self.read_historical()
        self.read_SSP245()
        self.read_SSP585()
        pass

    def read_historical(self):
        fdir = this_root + 'result/historical/各模式逐年区域平均序列/'
        for region in os.listdir(fdir):
            outdir = this_root + 'result/historical/模式集合后逐年区域平均序列/'+region+'/'
            mk_dir(outdir,force=True)
            outf = outdir + '模式集合.csv'
            year_list = []
            df_list = []
            for f in os.listdir((fdir + region)):
                # print()
                # exit()
                if f.startswith('.'):
                    continue
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
            # fw = open(outf, 'w')
            fw = codecs.open(outf, 'w', encoding='gbk')
            fw.write(head)
            fw.write(text)
            fw.close()

    def read_SSP245(self):
        fdir = this_root + 'result/SSP245/各模式逐年区域平均序列/'
        for region in os.listdir(fdir):
            outdir = this_root + 'result/SSP245/模式集合后逐年区域平均序列/'+region+'/'
            mk_dir(outdir,force=True)
            outf = outdir + '模式集合.csv'
            year_list = []
            df_list = []
            for f in os.listdir((fdir + region)):
                # print()
                # exit()
                if f.startswith('.'):
                    continue
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
            # fw = open(outf, 'w')
            fw = codecs.open(outf, 'w', encoding='gbk')
            fw.write(head)
            fw.write(text)
            fw.close()


    def read_SSP585(self):
        fdir = this_root + 'result/SSP585/各模式逐年区域平均序列/'
        for region in os.listdir(fdir):
            outdir = this_root + 'result/SSP585/模式集合后逐年区域平均序列/'+region+'/'
            mk_dir(outdir,force=True)
            outf = outdir + '模式集合.csv'
            year_list = []
            df_list = []
            for f in os.listdir((fdir + region)):
                # print()
                # exit()
                if f.startswith('.'):
                    continue
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
            # fw = open(outf, 'w')
            fw = codecs.open(outf, 'w', encoding='gbk')
            fw.write(head)
            fw.write(text)
            fw.close()


class Every_Model_time:

    def __init__(self):
        self.variable = variables()
        pass

    def run(self):

        # self.historical()

        date_range_list = range(3)
        for product in ['SSP245','SSP585']:
            for region in ['shang','xia']:
                for date_range in date_range_list:
                    print(product,region,date_range)
                    self.predict(product,date_range,region)
        #
        pass
    def historical(self):
        # region_pixs = get_shang_you()
        # outdir = this_root + 'result/historical/年代值/上游/'

        region_pixs = get_xia_you()
        outdir = this_root + 'result/historical/年代值/中下游/'

        fdir = this_root + 'cmip6数据/historical/'
        mk_dir(outdir, force=True)
        for f in os.listdir(fdir):
            if f.startswith('.'):
                continue
            outf = outdir + f
            fname = (fdir + f)
            print(fname)
            df = pd.read_csv(fdir + f, encoding='gbk')

            df = df[df['year']>=1995]
            df = df[df['year']<=2014]

            # print_head_n(df,n=30)
            # exit()
            lon_list = df.lon
            lat_list = df.lat
            lon_list = list(set(lon_list))
            lat_list = list(set(lat_list))
            lon_list.sort()
            lat_list.sort()
            indx = []
            for i,row in tqdm(df.iterrows(),total=len(df),desc='picking region pixs'):
                lon = row.lon
                lat = row.lat
                pix = (lon, lat)
                if pix in region_pixs:
                    indx.append(i)
            df_region = df.drop(index=indx)

            df_list = []
            for lon in tqdm(lon_list):
                df_lon = df_region[df_region['lon']==lon]
                for lat in lat_list:
                    df_lat = df_lon[df_lon['lat']==lat]
                    if len(df_lat) == 0:
                        continue
                    df_mean = df_lat.mean(axis=0)
                    df_mean = pd.DataFrame(df_mean)
                    df_mean = df_mean.T
                    df_list.append(df_mean)
            df_mean_all_pix = pd.concat(df_list,axis=0)
            df_mean_all_pix.to_csv(outf,encoding='gbk')

        pass

    def predict(self,product,date_range,region):
        date_range_list = [(2021,2040),(2041,2060),(2081,2100),]
        if date_range == 0:
            date_str = '近期20212040'
        elif date_range == 1:
            date_str = '中期20412060'
        elif date_range == 2:
            date_str = '远期20812100'
        else:
            raise UserWarning('date range error')
        if region == 'shang':
            region_pixs = get_shang_you()
            outdir = this_root + 'result/{}/年代值/上游/{}/各模式/'.format(product,date_str)
        elif region == 'xia':
            region_pixs = get_xia_you()
            outdir = this_root + 'result/{}/年代值/中下游/{}/各模式/'.format(product,date_str)
        else:
            raise UserWarning('region error')
        start,end = date_range_list[date_range]

        fdir = this_root + 'cmip6数据/{}/'.format(product)
        mk_dir(outdir, force=True)
        for f in os.listdir(fdir):
            if f.startswith('.'):
                continue
            outf = outdir + '{}-{}_'.format(start,end)+f
            fname = (fdir + f)
            print(fname)
            df = pd.read_csv(fdir + f, encoding='gbk')

            df = df[df['year']>=start]
            df = df[df['year']<=end]

            # print_head_n(df,n=30)
            # exit()
            lon_list = df.lon
            lat_list = df.lat
            lon_list = list(set(lon_list))
            lat_list = list(set(lat_list))
            lon_list.sort()
            lat_list.sort()
            indx = []
            for i,row in tqdm(df.iterrows(),total=len(df),desc='picking region pixs'):
                lon = row.lon
                lat = row.lat
                pix = (lon, lat)
                if pix in region_pixs:
                    indx.append(i)
            df_region = df.drop(index=indx)

            df_list = []
            for lon in tqdm(lon_list):
                df_lon = df_region[df_region['lon']==lon]
                for lat in lat_list:
                    df_lat = df_lon[df_lon['lat']==lat]
                    if len(df_lat) == 0:
                        continue
                    df_mean = df_lat.mean(axis=0)
                    df_mean = pd.DataFrame(df_mean)
                    df_mean = df_mean.T
                    df_list.append(df_mean)
            df_mean_all_pix = pd.concat(df_list,axis=0)
            df_mean_all_pix.to_csv(outf,encoding='gbk')

        pass


class Every_Model_time_mean:

    def __init__(self):

        pass

    def run(self):
        # self.historical()
        date_range_list = range(3)
        for product in ['SSP245', 'SSP585']:
            for region in ['shang', 'xia']:
                for date_range in date_range_list:
                    print(product, region, date_range)
                    self.predict(product, date_range, region)
        pass

    def historical(self):

        # fdir = this_root + 'result/historical/年代值/上游/各模式/'
        # outdir = this_root + 'result/historical/年代值/上游/各模式平均/'

        fdir = this_root + 'result/historical/年代值/中下游/各模式/'
        outdir = this_root + 'result/historical/年代值/中下游/各模式平均/'

        mk_dir(outdir, force=True)
        outf = outdir + 'mean.csv'
        df_list = []
        for f in os.listdir(fdir):
            if f.startswith('.'):
                continue
            fname = (fdir + f)
            print(fname)
            df = pd.read_csv(fdir + f, encoding='gbk')
            df_list.append(df)
            # print(df.loc[0])
            # print_head_n(df)
            # exit()
        all_indx_mean_list = []
        for i in tqdm(range(len(df_list[0]))):
            selected = []
            for df_indx in range(len(df_list)):
                series = df_list[df_indx].loc[i]
                series = pd.DataFrame(series)
                series = series.T
                # print(series)
                selected.append(series)
                # print(series)
            all_df = pd.concat(selected)
            df_mean = all_df.mean(axis=0)
            df_mean = pd.DataFrame(df_mean)
            df_mean = df_mean.T
            all_indx_mean_list.append(df_mean)
            # print(df_mean)
            # exit()
        all_indx_mean_df = pd.concat(all_indx_mean_list)
        all_indx_mean_df.to_csv(outf,encoding='gbk')


    def predict(self,product,date_range,region):
        if date_range == 0:
            date_str = '近期20212040'
        elif date_range == 1:
            date_str = '中期20412060'
        elif date_range == 2:
            date_str = '远期20812100'
        else:
            raise UserWarning('date range error')

        if region == 'shang':
            fdir = this_root + 'result/{}/年代值/上游/{}/各模式/'.format(product,date_str)
            outdir = this_root + 'result/{}/年代值/上游/{}/各模式平均/'.format(product,date_str)
        elif region == 'xia':
            fdir = this_root + 'result/{}/年代值/中下游/{}/各模式/'.format(product,date_str)
            outdir = this_root + 'result/{}/年代值/中下游/{}/各模式平均/'.format(product,date_str)
        else:
            raise UserWarning('region error')
        # print(outdir)
        # exit()
        mk_dir(outdir)
        outf = outdir + 'mean.csv'
        df_list = []
        for f in os.listdir(fdir):
            if f.startswith('.'):
                continue
            fname = (fdir + f)
            print(fname)
            df = pd.read_csv(fdir + f, encoding='gbk')
            df_list.append(df)
            # print(df.loc[0])
            # print_head_n(df)
            # exit()
        all_indx_mean_list = []
        for i in tqdm(range(len(df_list[0]))):
            selected = []
            for df_indx in range(len(df_list)):
                series = df_list[df_indx].loc[i]
                series = pd.DataFrame(series)
                series = series.T
                # print(series)
                selected.append(series)
                # print(series)
            all_df = pd.concat(selected)
            df_mean = all_df.mean(axis=0)
            df_mean = pd.DataFrame(df_mean)
            df_mean = df_mean.T
            all_indx_mean_list.append(df_mean)
            # print(df_mean)
            # exit()
        all_indx_mean_df = pd.concat(all_indx_mean_list)
        all_indx_mean_df.to_csv(outf, encoding='gbk')


def main():
    Every_Model().run()
    Every_Model_mean().run()
    Every_Model_time().run()
    Every_Model_time_mean().run()
    pass


if __name__ == '__main__':
    main()


