# coding=utf-8

import osr, ogr
import gdal
import numpy as np
import os
from osgeo import gdalconst

this_root = os.path.dirname(__file__)

def raster2array(rasterfn):
    '''
    create array from raster
    Agrs:
        rasterfn: tiff file path
    Returns:
        array: tiff data, an 2D array
    '''
    raster = gdal.Open(rasterfn)
    geotransform = raster.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    band = raster.GetRasterBand(1)
    array = band.ReadAsArray()
    array = np.asarray(array)
    del raster
    return array,originX,originY,pixelWidth,pixelHeight



def array2raster(newRasterfn,longitude_start,latitude_start,pixelWidth,pixelHeight,array):
    cols = array.shape[1]
    rows = array.shape[0]
    originX = longitude_start
    originY = latitude_start
    # open geotiff
    driver = gdal.GetDriverByName('GTiff')
    if os.path.exists(newRasterfn):
        os.remove(newRasterfn)
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Float32)
    # Add Color Table
    # outRaster.GetRasterBand(1).SetRasterColorTable(ct)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    # Write Date to geotiff
    outband = outRaster.GetRasterBand(1)
    ndv = -999999
    outband.SetNoDataValue(ndv)
    outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(4326)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    # Close Geotiff
    outband.FlushCache()
    del outRaster


def rasterize_shp(shp,output,x_min,y_min,x_res,y_res,pixel_width):
    # tif = 'D:\\MODIS\\data_tif\\MOD11A2.006\\2003.01.09.LST_Day_1km.tif'
    # shp = 'D:\\MODIS\\shp\\china_dissolve.shp'
    # output = 'D:\\MODIS\\my.tif'

    # data = gdal.Open(tif, gdalconst.GA_ReadOnly)
    # geo_transform = data.GetGeoTransform()
    #source_layer = data.GetLayer()
    # x_min = 108
    # x_max = x_min + geo_transform[1] * 0.25
    # y_min = 24
    # y_max = y_max + geo_transform[5] * 0.25
    # x_res = 37
    # y_res = 53
    mb_v = ogr.Open(shp)
    mb_l = mb_v.GetLayer()
    # pixel_width = 0.25

    target_ds = gdal.GetDriverByName('GTiff').Create(output, x_res, y_res, 1, gdal.GDT_Byte)
    target_ds.SetGeoTransform((x_min, pixel_width, 0, y_min, 0, pixel_width))
    band = target_ds.GetRasterBand(1)
    NoData_value = -999999
    band.SetNoDataValue(NoData_value)
    band.FlushCache()
    gdal.RasterizeLayer(target_ds, [1], mb_l)
    # gdal.RasterizeLayer(target_ds, [1], mb_l, options=["ATTRIBUTE=hedgerow"])

    target_ds = None


if __name__ == '__main__':
    arr = np.load(this_root+'/ERA/era_1_layer_mean.npy')[720-587:720-493,897:1079]
    from matplotlib import pyplot as plt
    # plt.imshow(arr)
    # plt.show()
    # exit()
    new_arr = []
    for i in arr:
        temp = []
        for j in i:
            if not np.isnan(j) and j > 0:
                temp.append(j)
            else:
                temp.append(-999999)
        new_arr.append(temp)
    new_arr = np.array(new_arr)
    array2raster('era_1_layer_mean.tif',44.25,56.75,0.25,-0.25,new_arr)

