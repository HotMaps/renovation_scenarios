import gdal, ogr, osr
import os
import sys
'''
Created on Apr 23, 2017

@author: simulant
'''

#@profile
def rrl(file_name, data_type="f4", raster_band=1, return_srs=False):
    #read raster layer and return array
    return read_raster_layer(file_name, data_type, raster_band
                             ,return_srs)
    
    
#@profile
def read_raster_layer(file_name, data_type="f4", raster_band=1
                      , return_srs=False):
    #read raster layer and return array
    print("Reading: %s" % file_name)
    ds = gdal.Open(file_name)
    band = ds.GetRasterBand(raster_band)
    print ("   Got RasterBand")
    arr = band.ReadAsArray().astype(data_type)
    
    geotransform_obj = ds.GetGeoTransform()
    epsg = None
    try:
        srs = osr.SpatialReference(wkt=ds.GetProjection())
        if srs.IsProjected:
            geogcs = srs.GetAttrValue("GEOGCS") 
            epsg = int(srs.GetAttrValue("GEOGCS|AUTHORITY",1))
    except Exception as e:
        print(e)
            
    print ("   Done!")
    
    if return_srs == True:
        return  (arr, geotransform_obj, epsg)
    else:   
        return  (arr, geotransform_obj)
    
