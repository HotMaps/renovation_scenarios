'''
Created on Jul 28, 2017

@author: simulant
'''

import gdal
import ogr, osr
import os
import numpy as np




def create_reference_raster_layer_origin_extent_of_vctr_feat(InputRasterFile
                    , InputVectorFile, Vct_feat_id_LIST
                    , Vctr_key_field):
    """
    Clips raster file rectangular shape, 
    to the extent of a set given features of vector shape file
    Input
    InputRasterFile: Filename of Input raster
    InputVectorFile: Filename of vector input layer file
    Vct_feat_id_LIST: List of features of InputVectorFile to consider 
    Vctr_key_field: Key field of features
    
    returns:
    
    SaveLayerLIST: [geotransform_obj, extent]
    
    """
    SaveLayerLIST = []

        
    #Get extent of selected features of shape file
    # Vector Layer with selected specific feature
    inDriver = ogr.GetDriverByName("ESRI Shapefile")
    #Assert file exists
    print(InputVectorFile)
    assert(os.path.exists(InputVectorFile))
    
    inDataSource = inDriver.Open(InputVectorFile, 0)
    inLayer = inDataSource.GetLayer()
    
    num_feat_of_layer = inLayer.GetFeatureCount()
    feat_name = []
    j = 0
    if len(Vct_feat_id_LIST) > 0:
        for i, FeatName in enumerate(Vct_feat_id_LIST):
            if type(Vct_feat_id_LIST[0]) is str:
                feat_name.append(FeatName)
                j += 1
            else:
                break
        Vct_feat_id_LIST = Vct_feat_id_LIST[j:]       
    if Vct_feat_id_LIST == []:
        num_feat = inLayer.GetFeatureCount()
        Vct_feat_id_LIST = list(range(num_feat))    
    fminx = fminy = 10**10
    fmaxx = fmaxy = 0
    feat_name_dict = {}
    j = 0
    num_feat = len(Vct_feat_id_LIST)
    if num_feat >= num_feat_of_layer:
        Layer_uncut = True
    else:
        Layer_uncut = False
    for feat_id in Vct_feat_id_LIST:
        try:
            #print(feat_id)
            j += 1
            if feat_id < num_feat_of_layer:
                inFeature = inLayer.GetFeature(feat_id)
                FeatName = (inFeature.GetField(Vctr_key_field))
                continue_feat_id = True
                if len(feat_name) > 0:
                    for FeatName_ in feat_name:
                        if FeatName_ in FeatName:
                            continue_feat_id = False
                            break
                else:
                    continue_feat_id = False
                if continue_feat_id == True:
                    continue
                if len(Vct_feat_id_LIST) < 100:
                    print ("%i of (%i - %2.1f %%): %s" %(j, num_feat + 1, j * 100 / num_feat, FeatName))
                elif j % int(num_feat / 5) == 0:
                    print ("%i of (%i - %2.1f %%): %s" %(j, num_feat + 1, j * 100 / num_feat, FeatName))
                    
                if type(FeatName) is str:
                    key_n = FeatName[:2]  
                else:
                    key_n = FeatName
                if key_n in feat_name_dict.keys():
                    feat_name_dict[key_n].append(FeatName)
                else:
                    feat_name_dict[key_n] = [FeatName]
                geom = inFeature.GetGeometryRef()
                #Get boundaries
                fminx_, fmaxx_, fminy_, fmaxy_ = geom.GetEnvelope()
                fminx = min(fminx_, fminx)
                fminy = min(fminy_, fminy)
                fmaxx = max(fmaxx_, fmaxx)
                fmaxy = max(fmaxy_, fmaxy) 
                #inFeature = None
        except Exception as e:
            print(e)
            #break
    
    inLayer = None
    
    cutRastDatasource = gdal.Open(InputRasterFile)
    transform = cutRastDatasource.GetGeoTransform()
    minx = transform[0]
    maxy = transform[3]
    resX = transform[1]
    resY = -transform[5]
    
    # define exact index that encompasses the feature.
    lowIndexLG=int(max(0, int((fminx-minx)/resX)))
    lowIndexBG=int(max(0, int((maxy-fmaxy)/resY)))
    
    upIndexLG = lowIndexLG + int(np.ceil((fmaxx - fminx )/ resX)) + 1
    upIndexBG = lowIndexBG + int(np.ceil((fmaxy - fminy) / resY)) + 1

    
    # considering the resolution of strd raster, the raster origin should be a factor of resX/resY. this will be done in the following code.
    rasterOrigin2 = (minx + lowIndexLG * resX, maxy - lowIndexBG * resY)
    geotransform_obj = (rasterOrigin2[0], resX, 0, rasterOrigin2[1], 0, -resY)
    
    #Calculate the Extent in Pixel 
    RasterXSize = np.maximum(1, upIndexLG - lowIndexLG)
    RasterYSize = np.maximum(1, upIndexBG - lowIndexBG)
    RasterSize = [RasterYSize, RasterXSize]
    RESOLUTION = [resX, resY]
    
    
    minx = rasterOrigin2[0]
    maxy = rasterOrigin2[1]
    maxx = minx + transform[1] * RasterXSize
    miny = maxy + transform[5] * RasterYSize
    extent = (minx, maxx, miny, maxy) # i
    
    return [geotransform_obj, RasterSize, RESOLUTION, extent], Layer_uncut

    

#@profile
def clip_raster_layer(InputRasterFile
                      , REFERENCE_geotransform_obj
                      , REFERENCE_extent
                      , BASE_MAP=[]
                      , return_offset_list = False
                      , final_res=0
                      , data_type=""):

    ########################################
    # Load Raster layer file
    # Cut with boundaries base_minx,..base_maxy
    # Return cutted Raster layer image
    ######################################
    
    if type(InputRasterFile) is list:
        (arr1, transform) = InputRasterFile
        epsg = 3035
    else:
        if os.path.exists(InputRasterFile) == False:
            print(" ERROR\nFiles doesn't exist: \n   %s" %InputRasterFile)
            print("Abort run")
            assert(os.path.exists(InputRasterFile) == True)
        print("Read (and clip) raster layer: %s" %InputRasterFile)
        cutRastDatasource = gdal.Open(InputRasterFile)
        transform = cutRastDatasource.GetGeoTransform()
        
        b11 = cutRastDatasource.GetRasterBand(1)
        arr1 = b11.ReadAsArray()
        if data_type != "":
            arr1 = arr1.astype(data_type)
        
        srs = osr.SpatialReference(wkt=cutRastDatasource.GetProjection())
        if srs.IsProjected:
            try:
                epsg = int(srs.GetAttrValue("GEOGCS|AUTHORITY",1))
            except:
                epsg = 3035
    
    arr1_shape = arr1.shape
    print("Clip raster layer: Shape: %s, Type: %s" %(str(arr1_shape), str(arr1.dtype)))
    cutIM_size_orig = arr1.size
    if epsg == 3035:
        cutIM_minx = np.round(transform[0])
        cutIM_maxy = np.round(transform[3])
        base_minx = np.round(REFERENCE_geotransform_obj[0])
        base_maxy = np.round(REFERENCE_geotransform_obj[3])
    
    else:
        cutIM_minx = np.round(transform[0]*1000) / 1000
        cutIM_maxy = np.round(transform[3]*1000) / 1000
        base_minx = np.round(REFERENCE_geotransform_obj[0]*1000) / 1000
        base_maxy = np.round(REFERENCE_geotransform_obj[3]*1000) / 1000
        
    cutIM_resX = transform[1]
    cutIM_resY = transform[5]
    cutIM_maxx = cutIM_minx + arr1_shape[1] * cutIM_resX
    cutIM_miny = cutIM_maxy + arr1_shape[0] * cutIM_resY
    #cutIM_deltax = cutIM_maxx - cutIM_minx
    #cutIM_deltay = cutIM_maxy - cutIM_miny
    cutIM_top_corner = np.maximum(cutIM_maxy, cutIM_miny)
    cutIM_bottom_corner = np.minimum(cutIM_maxy, cutIM_miny)
    cutIM_right_corner = np.maximum(cutIM_maxx, cutIM_minx)
    cutIM_left_corner = np.minimum(cutIM_minx, cutIM_maxx)
    
    
    base_maxx = base_minx + REFERENCE_extent[1] * REFERENCE_geotransform_obj[1] 
    base_miny = base_maxy + REFERENCE_extent[0] * REFERENCE_geotransform_obj[5]
    base_top_corner = np.maximum(base_maxy, base_miny)
    base_bottom_corner = np.minimum(base_maxy, base_miny)
    base_right_corner = np.maximum(base_maxx, base_minx)
    base_left_corner = np.minimum(base_minx, base_maxx)
    
    
    base_deltax = base_right_corner - base_left_corner
    base_deltay = base_top_corner - base_bottom_corner
    size_newX = int(abs(base_deltax / cutIM_resX))
    size_newY = int(abs(base_deltay / cutIM_resY))
    size_new = size_newX * size_newY
    
    
    
    top_corner = np.minimum(base_top_corner, cutIM_top_corner)
    bottom_corner = np.minimum(top_corner, np.maximum(base_bottom_corner, cutIM_bottom_corner))
    top_corner = np.maximum(bottom_corner, top_corner)
    
    right_corner = np.minimum(base_right_corner, cutIM_right_corner)
    left_corner = np.minimum(right_corner, np.maximum(base_left_corner, cutIM_left_corner))
    right_corner = np.maximum(left_corner, right_corner)
    
    
    
    
    cutIM_resX = abs(cutIM_resX)
    cutIM_resY = abs(cutIM_resY)
    
    cutIM_lowIndexY = int(np.maximum(0
                                , np.round((cutIM_top_corner - top_corner) / cutIM_resY )))
    cutIM_lowIndexX = int(np.maximum(0
                                , np.round((left_corner - cutIM_left_corner) / cutIM_resX )))
    cutIM_highIndexY = int(np.maximum(cutIM_lowIndexY
                                , np.round((cutIM_top_corner - bottom_corner) / cutIM_resY)))
    cutIM_highIndexX = int(np.maximum(cutIM_lowIndexX
                                , np.round((right_corner - cutIM_left_corner) / cutIM_resX)))
    cutIM_dimY = cutIM_highIndexY - cutIM_lowIndexY
    cutIM_dimX = cutIM_highIndexX - cutIM_lowIndexX   
    
    
    size_cutIM = cutIM_dimY * cutIM_dimX
    
    
    base_lowIndexY = int(np.maximum(0
                            , np.round((base_top_corner - top_corner) / cutIM_resY )))
    base_lowIndexX = int(np.maximum(0
                            , np.round((left_corner - base_left_corner) / cutIM_resX )))
    if final_res > cutIM_resX: 
        res_change = final_res / cutIM_resX
        base_lowIndexY_ = int(np.floor(base_lowIndexY / res_change) * res_change)
        base_lowIndexX_ = int(np.floor(base_lowIndexX / res_change) * res_change)
    
        base_highIndexY_ = int(np.ceil((base_lowIndexY + cutIM_dimY) / res_change) * res_change)
        base_highIndexX_ = int(np.ceil((base_lowIndexX + cutIM_dimX) / res_change) * res_change)
    
    else:
        base_lowIndexY_ = int(base_lowIndexY)
        base_lowIndexX_ = int(base_lowIndexX)
        base_highIndexY_ = int(base_lowIndexY + cutIM_dimY)
        base_highIndexX_ = int(base_lowIndexX + cutIM_dimX) 

    
    
     
    
    #base_dimY = base_highIndexY - base_lowIndexY
    #base_dimX = base_highIndexX - base_lowIndexX
    USE_BASE_AMP = False
    if (not type(BASE_MAP)  is list and
            BASE_MAP.shape[0] == size_newY and BASE_MAP.shape[1] == size_newX):
        USE_BASE_AMP = True

        
    if return_offset_list == True:
        if final_res > cutIM_resX:  
            cutIM_dimY_out = int((base_highIndexY_ - base_lowIndexY_))
            cutIM_dimX_out = int((base_highIndexX_ - base_lowIndexX_))
     
        arr_out = np.zeros((cutIM_dimY_out, cutIM_dimX_out), dtype=arr1.dtype)
        
        
    elif USE_BASE_AMP == False:
        arr_out = np.zeros((size_newY, size_newX), dtype=arr1.dtype)
    else:
        arr_out = BASE_MAP
    
    offset_x = base_lowIndexX - base_lowIndexX_
    offset_y = base_lowIndexY - base_lowIndexY_   
    
    base_lowIndexY = int(np.maximum(0
                            , np.round((base_top_corner - (top_corner + offset_y)) / cutIM_resY )))
    base_lowIndexX = int(np.maximum(0
                        , np.round((left_corner - (base_left_corner - offset_x)) / cutIM_resX )))

    base_highIndexY = base_lowIndexY + cutIM_dimY
    base_highIndexX = base_lowIndexX + cutIM_dimX    
    
    delta_y = np.maximum(0, cutIM_highIndexY - arr1_shape[0])
    delta_x = np.maximum(0, cutIM_highIndexX - arr1_shape[1])
    
    
    
    if size_cutIM == 0:
        print("Images do not intersect")    
    elif return_offset_list == True: 
        
        
    
        arr_out[offset_y:offset_y + cutIM_highIndexY - cutIM_lowIndexY
                , offset_x:offset_x + cutIM_highIndexX - cutIM_lowIndexX] += \
                arr1[cutIM_lowIndexY:cutIM_highIndexY, cutIM_lowIndexX:cutIM_highIndexX] 
        
        
    elif USE_BASE_AMP == True:
        
        
        arr_out[base_lowIndexY:base_highIndexY - delta_y
                    , base_lowIndexX:base_highIndexX - delta_x] += \
                arr1[cutIM_lowIndexY:cutIM_highIndexY
                    , cutIM_lowIndexX:cutIM_highIndexX] 
    else:
        dY1 = base_highIndexY - base_lowIndexY - delta_y
        dX1 = base_highIndexX - delta_x - base_lowIndexX
        
        dY2 = cutIM_highIndexY - cutIM_lowIndexY
        dX2 = cutIM_highIndexX - cutIM_lowIndexX
        delta_y2 = max(0, dY1 - arr_out.shape[0])
        delta_x2 = max(0, dX1 - arr_out.shape[1])
        arr_out[base_lowIndexY:base_highIndexY - delta_y
                    , base_lowIndexX:base_highIndexX - delta_x] = \
                arr1[cutIM_lowIndexY:cutIM_highIndexY - delta_y2
                    , cutIM_lowIndexX:cutIM_highIndexX - delta_x2]   
                              
    
    if return_offset_list == True:
        geotransform_obj = (REFERENCE_geotransform_obj[0] + base_lowIndexX_ * cutIM_resX, cutIM_resX, 0
                        , REFERENCE_geotransform_obj[3] - base_lowIndexY_ * cutIM_resY, 0, -cutIM_resY)       
    else:

        geotransform_obj = (REFERENCE_geotransform_obj[0], cutIM_resX, 0
                        , REFERENCE_geotransform_obj[3], 0, -cutIM_resY)
    
    del arr1
    b11 = None
    cutRastDatasource = None
    
    arr_out_shape = arr_out.shape
    print("Shape Array In : %s" % str(arr1_shape))
    
    print("Shape Array Out: %s -> %2.2f %% " % (str(arr_out_shape)
                                    , (100 * size_new / np.maximum(1, cutIM_size_orig))))
    
    if arr_out_shape != arr1_shape:
        reshaped = True
    else:
        reshaped = False
    if return_offset_list == True:
        return (arr_out
                , [base_lowIndexY_, base_highIndexY_
                   , base_lowIndexX_, base_highIndexX_]
                , geotransform_obj)
    else:
        return (arr_out, geotransform_obj)