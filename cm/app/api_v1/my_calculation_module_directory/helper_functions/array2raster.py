import gdal, osr
import time
import sys, os

'''
To create the raster consider following data types:

GDT_Unknown     Unknown or unspecified type
GDT_Byte        Eight bit unsigned integer
GDT_UInt16      Sixteen bit unsigned integer
GDT_Int16       Sixteen bit signed integer
GDT_UInt32      Thirty two bit unsigned integer
GDT_Int32       Thirty two bit signed integer
GDT_Float32     Thirty two bit floating point
GDT_Float64     Sixty four bit floating point
GDT_CInt16      Complex Int16
GDT_CInt32      Complex Int32
GDT_CFloat32    Complex Float32
GDT_CFloat64    Complex Float64
'''

def array2raster(outRasterPath, GeoTransformObject
                , dataType, array, noDataValue
                , ZLEVEL=9
                , OutPutProjection=3035
                , ds_pr = None):
    """ 
    Exports array to raster file
    """
    
    
    
    st = time.time()
    try:
        ZLEVEL = int(ZLEVEL)
    except:
        ZLEVEL = 6
    # conversion of data types from numpy to gdal
    dict_varTyp ={"int8" : gdal.GDT_Byte, "int16" : gdal.GDT_Int16, "int32" : gdal.GDT_Int32
                  , "uint16" : gdal.GDT_UInt16, "uint32" : gdal.GDT_UInt32
                  , "float32" : gdal.GDT_Float32, "float64" : gdal.GDT_Float64
                  , "f4" : gdal.GDT_Float32}
    cols = array.shape[1]
    rows = array.shape[0]

    driver = gdal.GetDriverByName('GTiff')
    print ("  Exporting Raster Layer: %s" % outRasterPath)
    


    outRaster = driver.Create(outRasterPath.replace("//", "/"), cols, rows, 1, dict_varTyp[dataType], ['compress=DEFLATE',
                                                      'TILED=YES',
                                                      'TFW=YES',
                                                      'ZLEVEL=%i'%ZLEVEL,
                                                      'PREDICTOR=1'])
    
    
    #outRaster = driver.Create(outRasterPath, cols, rows, 1, dict_varTyp[dataType])    

    
    if ds_pr != None:
        
        ds_in = gdal.Open(ds_pr)
        GeoTransformObject = ds_in.GetGeoTransform()
        #Projection = osr.SpatialReference()
        #Projection.ImportFromWkt(ds_in.GetProjectionRef)
    
    """                         
    src_ds = gdal.Open(ds_pr)
    projection_ = osr.SpatialReference()
    GeoTransformObject = src_ds.GetGepTransform()
    outRaster.SetGeoTransform(GeoTransformObject)
    projection_.ImportFromWkt(src_ds.GetProjectionRef())
    outRaster.SetProjection(projection_.ExportToWkt())  
    """
    if 1==1:
        outRaster.SetGeoTransform(GeoTransformObject)
        outRasterSRS = osr.SpatialReference()
        outRasterSRS.ImportFromEPSG(OutPutProjection)
        outRaster.SetProjection(outRasterSRS.ExportToWkt())
        
    outRaster.GetRasterBand(1).SetNoDataValue(noDataValue)
    outRaster.GetRasterBand(1).WriteArray(array)
    outRaster.FlushCache()
    print("  Exporting took: %4.1f sec" % (time.time() - st))
    return



def array2rasterfileList(InputDataList):
    if len(InputDataList) < 5 or len(InputDataList) > 8:
        print("Error: List with at least 5 datasets required: ")
        print("outRasterPath, GeoTransformObject," 
               +" dataType, array, noDataValue")
        print("End script -> Done")
        sys.exit()
    if len(InputDataList) == 5:
        array2raster(InputDataList[0], InputDataList[1]
                     , InputDataList[2], InputDataList[3]
                     , InputDataList[4])
    elif len(InputDataList) == 6:
        array2raster(InputDataList[0], InputDataList[1]
                     , InputDataList[2], InputDataList[3]
                     , InputDataList[4], InputDataList[5])
    elif len(InputDataList) == 7:
        array2raster(InputDataList[0], InputDataList[1]
                     , InputDataList[2], InputDataList[3]
                     , InputDataList[4], InputDataList[5]
                     , InputDataList[6])
    else:
        array2raster(InputDataList[0], InputDataList[1]
                     , InputDataList[2], InputDataList[3]
                     , InputDataList[4], InputDataList[5]
                     , InputDataList[6], InputDataList[7])
                
    
def gdal_warp(inRasterPath,
              outRasterPath,
              OutPutProjection=3035
              , delete_orig = False):
    print("Warp: %s" % inRasterPath)
    # Open source dataset
    src_ds = gdal.Open(inRasterPath)
    # Define target SRS
    dst_srs = osr.SpatialReference()
    dst_srs.ImportFromEPSG(OutPutProjection)
    dst_wkt = dst_srs.ExportToWkt()
    
    error_threshold = 0.125  # error threshold --> use same value as in gdalwarp
    resampling = gdal.GRA_Bilinear
    
    # Call AutoCreateWarpedVRT() to fetch default values for target raster dimensions and geotransform
    tmp_ds = gdal.AutoCreateWarpedVRT( src_ds,
                                       None, # src_wkt : left to default value --> will use the one from source
                                       dst_wkt,
                                       resampling,
                                       error_threshold )
    
    # Create the final warped raster
    dst_ds = gdal.GetDriverByName('GTiff').CreateCopy(outRasterPath, tmp_ds)
    dst_ds = None
    print("  Done: %s" % outRasterPath)
    
    try:
        pass #os.remove(inRasterPath)
    except Exception as e:
        print(e)
        print("cannot remove: %s" % inRasterPath)
                    
                    
    return