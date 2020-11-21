# coding=gbk

import shpbuffer as sb
import time
import numpy as np
import pandas as pd
from tqdm import tqdm
import os
from matplotlib import pyplot as plt
import to_raster


this_root = r'D:\PycharmProjects\wenquanpei\20201119\\'
result_root = this_root + 'result\\'


def sleep(t=1):
    time.sleep(t)
def pause():
    raw_input('\33[7m'+"PRESS ENTER TO CONTINUE."+'\33[0m')


class Shp_Tools:
    def __init__(self):

        pass

    def mk_dir(self, dir, force=False):

        if not os.path.isdir(dir):
            if force == True:
                os.makedirs(dir)
            else:
                os.mkdir(dir)

    def check_points_in_shp(self,shp,x,y):
        poly = sb.get_poly(shp)
        in_shp = sb.check_xys_in_poly(x,y,poly)
        return in_shp

    def save_dict_to_txt(self,results_dic,outf):
        fw = outf + '.txt'
        fw = open(fw, 'w')
        fw.write(str(results_dic))
        pass

    def load_dict_txt(self,f):
        nan = np.nan
        dic = eval(open(f,'r').read())
        return dic


class TMP:

    def __init__(self):

        self.tmp_dir = this_root + ur'\ver2\气温要素\\'
        self.shp = this_root + ur'下游\\dissolve.shp'
        self.template_text = this_root + ur'\ver2\气温要素\\tmax历史及未来逐年值\\maxtmax_126_2436_20152100.txt'
        self.this_root_arr = result_root + 'arr\\TMP\\'
        Shp_Tools().mk_dir(self.this_root_arr,force=True)


    def run(self):
        # 0 prepare is_pix_in_shp_to_dic
        # self.is_pix_in_shp_to_dic()
        # 1 load is_pix_in_shp_to_dic
        self.pix_in_shp_dic = self.load_is_pix_in_shp()
        # self.cal_dir_mean()
        # self.text_dir_to_tif()
        self.mask_txt()

        pass


    def mask_txt(self):
        pix_in_shp_dic = self.pix_in_shp_dic
        out_dir = self.this_root_arr + 'mask_txt\\' + self.tmp_dir.split('\\')[-3] + '\\'
        # print out_dir
        Shp_Tools().mk_dir(out_dir, force=True)
        for folder in os.listdir(self.tmp_dir):
            print folder
            dir_i = os.path.join(self.tmp_dir, folder) + '\\'
            outdir_i = out_dir + folder + '\\'
            Shp_Tools().mk_dir(outdir_i, force=False)
            for f in os.listdir(dir_i):

                txt_f = dir_i + f
                outf = outdir_i + f
                print outf
                fw = open(outf,'w')
                fr = open(txt_f, 'r')
                lines = fr.readlines()
                flag = 0
                for line in lines:
                    flag += 1
                    line_split = line.split()
                    lon = float(line_split[0])
                    lat = float(line_split[1])
                    pix = (lon, lat)
                    if self.pix_in_shp_dic[pix]:
                        fw.write(line)
                fw.close()
                # exit()

    def text_dir_to_tif(self):

        work_dir = self.tmp_dir
        out_dir = self.this_root_arr + 'text_dir_to_tif\\' + work_dir.split('\\')[-3] + '\\'
        print out_dir
        Shp_Tools().mk_dir(out_dir, force=True)
        for folder in os.listdir(self.tmp_dir):
            print folder
            dir_i = os.path.join(self.tmp_dir, folder) + '\\'
            outdir_i = out_dir + folder + '\\'
            Shp_Tools().mk_dir(outdir_i, force=False)
            for f in os.listdir(dir_i):
                outf = outdir_i + f + '\\'
                print f
                self.text_to_tif(dir_i + f, outf)
        pass

    def text_to_tif(self,txt_f,outtifdir):
        Shp_Tools().mk_dir(outtifdir,force=True)
        fr = open(txt_f, 'r')
        lines = fr.readlines()
        fr.close()

        len_vals = np.nan
        for line in lines:
            line = line.split()
            vals = line[2:]
            len_vals = len(vals)
            break

        for i in range(len_vals):
            outf_i = outtifdir + '{:02d}.tif'.format(i+1)
            spatial_dic = {}
            for line in lines:
                line = line.split()
                lon = float(line[0])
                lat = float(line[1])
                vals = line[2:]
                vals = np.array(vals, dtype=float)
                val = vals[i]
                pix = (lon, lat)
                if self.pix_in_shp_dic[pix]:
                    spatial_dic[pix] = val
            Lon_Lat_to_tif(self.template_text).spatial_dic_to_tif(spatial_dic,outf_i)

        pass

    def is_pix_in_shp_to_dic(self):
        txt_f = self.tmp_dir + ur'tmax年代值\\tmax35d_index_126_period20412060_2436.txt'
        df = pd.DataFrame()
        fr = open(txt_f,'r')
        lines = fr.readlines()

        lon_list = []
        lat_list = []
        vals_list = []
        for line in lines:
            line = line.split()
            lon = float(line[0])
            lat = float(line[1])
            vals = line[2:]
            vals = np.array(vals,dtype=float)

            lon_list.append(lon)
            lat_list.append(lat)
            vals_list.append(vals)
        df['lon'] = lon_list
        df['lat'] = lat_list
        df['val'] = vals_list

        is_in_poly_dic = {}
        for i,row in tqdm(df.iterrows(),total=len(df)):
            lon = row['lon']
            lat = row['lat']
            is_in_poly = Shp_Tools().check_points_in_shp(self.shp,lon,lat)
            pix = (lon,lat)
            is_in_poly_dic[pix] = is_in_poly

        Shp_Tools().save_dict_to_txt(is_in_poly_dic,self.this_root_arr + 'is_in_poly_dic')

    def load_is_pix_in_shp(self):
        dic = Shp_Tools().load_dict_txt(self.this_root_arr + 'is_in_poly_dic.txt')
        return dic


    def cal_mean(self,txt_f,outf):
        fr = open(txt_f, 'r')
        lines = fr.readlines()
        selected_vals_list = []
        flag = 0
        for line in lines:
            flag += 1
            line = line.split()
            lon = float(line[0])
            lat = float(line[1])
            vals = line[2:]
            # print vals
            try:
                vals = np.array(vals, dtype=float)
            except Exception as e:
                print vals
                print txt_f
                print flag
                print e
                exit()
            pix = (lon,lat)
            if self.pix_in_shp_dic[pix]:
                selected_vals_list.append(vals)
        selected_vals_arr = np.array(selected_vals_list)
        selected_vals_arr = selected_vals_arr.T
        mean_vals = []
        for arr in selected_vals_arr:
            mean = np.mean(arr)
            mean_vals.append('{:0.2f}'.format(mean))

        str_ = '\t'.join(mean_vals)

        fw = open(outf,'w')
        fw.write(str_)
        fw.close()

    def cal_dir_mean(self):
        # print self.pre_dir1.split('\\')[-3]
        # exit()
        out_dir = self.this_root_arr + 'cal_dir_mean\\' + self.tmp_dir.split('\\')[-3] + '\\'
        # print out_dir
        Shp_Tools().mk_dir(out_dir,force=True)
        for folder in os.listdir(self.tmp_dir):
            print folder
            dir_i = os.path.join(self.tmp_dir,folder) + '\\'
            outdir_i = out_dir + folder + '\\'
            Shp_Tools().mk_dir(outdir_i, force=False)
            for f in os.listdir(dir_i):
                outf = outdir_i + f
                print f
                self.cal_mean(dir_i + f,outf)
        pass



class Pre:

    def __init__(self):

        self.pre_dir1 = this_root + ur'\ver2\降水历史及未来逐年值1\\'
        self.pre_dir2 = this_root + ur'\ver2\降水年代值1\\'
        self.shp = this_root + ur'长江上游边界\\dissolve_new.shp'

        self.this_root_arr = result_root + 'arr\\Pre\\'
        Shp_Tools().mk_dir(self.this_root_arr,force=True)


    def run(self):
        # 0 prepare is_pix_in_shp_to_dic
        # self.is_pix_in_shp_to_dic()
        self.pix_in_shp_dic = self.load_is_pix_in_shp()
        # 1 cal_dir_mean
        # self.cal_dir_mean()
        # 2 text_dir_to_tif
        # self.text_dir_to_tif()
        # 3 mask txt
        self.mask_txt()

    def mask_txt(self):
        work_dir = self.pre_dir2
        out_dir = self.this_root_arr + 'mask_txt\\' + work_dir.split('\\')[-3] + '\\'
        print out_dir
        Shp_Tools().mk_dir(out_dir, force=True)
        for f in os.listdir(work_dir):
            txt_f = work_dir + f
            outf = out_dir + f
            print outf
            fw = open(outf, 'w')
            fr = open(txt_f, 'r')
            lines = fr.readlines()
            flag = 0
            for line in lines:
                flag += 1
                line_split = line.split()
                lon = float(line_split[0])
                lat = float(line_split[1])
                pix = (lon, lat)
                if self.pix_in_shp_dic[pix]:
                    fw.write(line)
            fw.close()


        pass


    def text_dir_to_tif(self):

        work_dir = self.pre_dir2
        out_dir = self.this_root_arr + 'text_dir_to_tif\\' + work_dir.split('\\')[-3] + '\\'
        print out_dir
        Shp_Tools().mk_dir(out_dir, force=True)
        for f in os.listdir(work_dir):
            print f
            self.text_to_tif(work_dir + f, out_dir + f + '\\')
        pass


    def text_to_tif(self,txt_f,outtifdir):
        Shp_Tools().mk_dir(outtifdir,force=True)
        fr = open(txt_f, 'r')
        lines = fr.readlines()
        fr.close()

        len_vals = np.nan
        for line in lines:
            line = line.split()
            vals = line[2:]
            len_vals = len(vals)
            break

        for i in range(len_vals):
            outf_i = outtifdir + '{:02d}.tif'.format(i+1)
            spatial_dic = {}
            for line in lines:
                line = line.split()
                lon = float(line[0])
                lat = float(line[1])
                vals = line[2:]
                vals = np.array(vals, dtype=float)
                val = vals[i]
                pix = (lon, lat)
                if self.pix_in_shp_dic[pix]:
                    spatial_dic[pix] = val
            Lon_Lat_to_tif().spatial_dic_to_tif(spatial_dic,outf_i)

        pass


    def is_pix_in_shp_to_dic(self):
        txt_f = self.pre_dir1 + 'pre0days_126_2436_20152100.txt'
        df = pd.DataFrame()
        fr = open(txt_f,'r')
        lines = fr.readlines()

        lon_list = []
        lat_list = []
        vals_list = []
        for line in lines:
            line = line.split()
            lon = float(line[0])
            lat = float(line[1])
            vals = line[2:]
            vals = np.array(vals,dtype=float)

            lon_list.append(lon)
            lat_list.append(lat)
            vals_list.append(vals)
        df['lon'] = lon_list
        df['lat'] = lat_list
        df['val'] = vals_list

        is_in_poly_dic = {}
        for i,row in tqdm(df.iterrows(),total=len(df)):
            lon = row['lon']
            lat = row['lat']
            is_in_poly = Shp_Tools().check_points_in_shp(self.shp,lon,lat)
            pix = (lon,lat)
            is_in_poly_dic[pix] = is_in_poly

        Shp_Tools().save_dict_to_txt(is_in_poly_dic,self.this_root_arr + 'is_in_poly_dic')

    def load_is_pix_in_shp(self):
        dic = Shp_Tools().load_dict_txt(self.this_root_arr + 'is_in_poly_dic.txt')
        return dic


    def cal_mean(self,txt_f,outf):
        fr = open(txt_f, 'r')
        lines = fr.readlines()
        selected_vals_list = []
        for line in lines:
            line = line.split()
            lon = float(line[0])
            lat = float(line[1])
            vals = line[2:]
            vals = np.array(vals, dtype=float)
            pix = (lon,lat)
            if self.pix_in_shp_dic[pix]:
                selected_vals_list.append(vals)
        selected_vals_arr = np.array(selected_vals_list)
        selected_vals_arr = selected_vals_arr.T
        mean_vals = []
        for arr in selected_vals_arr:
            mean = np.mean(arr)
            mean_vals.append('{:0.2f}'.format(mean))

        str_ = '\t'.join(mean_vals)

        fw = open(outf,'w')
        fw.write(str_)
        fw.close()

    def cal_dir_mean(self):
        # print self.pre_dir1.split('\\')[-3]
        # exit()
        # out_dir = self.this_root_arr + 'cal_dir_mean\\' + self.pre_dir1.split('\\')[-3] + '\\'
        out_dir = self.this_root_arr + 'cal_dir_mean\\' + self.pre_dir2.split('\\')[-3] + '\\'
        print out_dir
        Shp_Tools().mk_dir(out_dir,force=True)
        for f in os.listdir(self.pre_dir2):
            print f
            self.cal_mean(self.pre_dir2 + f,out_dir + f)
        pass


class Lon_Lat_to_tif:

    def __init__(self,template_text_f):
        self.text_f = template_text_f
        pass

    def run(self):
        # self.text_to_spatial_dic()

        pass


    def text_to_spatial_dic(self):
        text_f = this_root + ur'ver2\降水年代值1\pre_index_245_period20212040_2436.txt'
        fr = open(text_f, 'r')
        lines = fr.readlines()
        spatial_dic = {}
        for line in lines:
            line = line.split()
            lon = float(line[0])
            lat = float(line[1])
            vals = line[2]
            vals = np.array(vals, dtype=float)
            spatial_dic[(lon,lat)] = vals
        spatial, originX, originY, pixelWidth, pixelHeight = self.spatial_dic_to_arr(spatial_dic)
        plt.imshow(spatial)
        plt.show()
        pass

    def spatial_dic_to_arr(self,in_dic):
        # text_f = this_root + ur'ver2\降水年代值1\pre_index_245_period20212040_2436.txt'
        text_f = self.text_f
        fr = open(text_f, 'r')
        lines = fr.readlines()
        lon_list = []
        lat_list = []
        vals_list = []
        for line in lines:
            line = line.split()
            lon = float(line[0])
            lat = float(line[1])
            vals = line[2]
            vals = np.array(vals, dtype=float)
            lon_list.append(lon)
            lat_list.append(lat)
            vals_list.append(vals)
        lon_list = set(lon_list)
        lon_list = list(lon_list)
        lat_list = set(lat_list)
        lat_list = list(lat_list)

        lon_list.sort()
        lat_list.sort()

        lon_max = max(lon_list)
        lon_min = min(lon_list)

        lat_max = max(lat_list)
        lat_min = min(lat_list)

        lon_cell_size = (lon_max - lon_min) / (len(lon_list)-1)
        lat_cell_size = (lat_max - lat_min) / (len(lat_list)-1)

        row = len(lat_list)
        col = len(lon_list)

        spatial_dic_lon_lat = {}
        for lon in lon_list:
            for lat in lat_list:
                pix_ = (int((lat - lat_min)/lat_cell_size),int((lon-lon_min)/lon_cell_size))
                lon_lat = (lon,lat)
                spatial_dic_lon_lat[lon_lat] = pix_

        spatial_dic_transform = {}
        for lon_lat in in_dic:
            pix = spatial_dic_lon_lat[lon_lat]
            val = in_dic[lon_lat]
            spatial_dic_transform[pix] = val

        spatial = []
        for r in range(row):
            temp = []
            for c in range(col):
                key = (r, c)
                if key in spatial_dic_transform:
                    val_pix = spatial_dic_transform[key]
                    temp.append(val_pix)
                else:
                    temp.append(np.nan)
            spatial.append(temp)

        spatial = np.array(spatial, dtype=float)
        spatial = spatial[::-1]
        originX, originY, pixelWidth, pixelHeight = lon_min,lat_max,lon_cell_size,lat_cell_size
        ndv = -999999
        spatial[np.isnan(spatial)] = ndv
        return spatial,originX, originY, pixelWidth, pixelHeight
        pass


    def spatial_dic_to_tif(self,spatial_dic,outf):
        spatial,originX, originY, pixelWidth, pixelHeight = Lon_Lat_to_tif(self.text_f).spatial_dic_to_arr(spatial_dic)
        to_raster.array2raster(outf,originX,originY,pixelWidth,-pixelHeight,spatial)



def plot_scatter():
    dic = TMP().load_is_pix_in_shp()
    for pix in tqdm(dic):
        lon,lat = pix
        val = dic[pix]
        if val:
            plt.scatter(lon,lat,s=4,c='black')
    plt.show()

    pass

def main():
    Pre().run()
    # TMP().run()
    # Lon_Lat_to_tif().run()
    # plot_scatter()
    pass


if __name__ == '__main__':

    main()
