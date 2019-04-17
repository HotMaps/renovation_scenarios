import os
import time
import sys
import numpy as np
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.
                                                       abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)
from N3scenario_to_raster import CalcEffectsAtRasterLevel
from CM_intern.common_modules.readCsvData import READ_CSV_DATA
import CM_intern.CEDM.modules.Subfunctions as SF
import CM_intern.common_modules.cliprasterlayer as CRL
from CM_intern.common_modules.exportLayerDict import export_layer as expLyr

print(sys.version_info)

def main():
    
    st = time.time()
    #end_year = 2030
    #start_year = 2012
    data_type = "f4"
    data_type_int = "uint32"
    
    
    
    
    subdir = "cut/"
    reshaped = False
    #subdir = ""
    #reshaped = True
    
    Reference, geotransform_obj = SF.rrl("input/cut/REFERENCE.tif", data_type=data_type_int)
    #NUTS_id, geotransform_obj = SF.rrl("input/NUTS3_cut_id_number.tif", data_type=data_type_int)
    NUTS_id, geotransform_obj = CRL.clip_raster_layer("input/%sNUTS3_cut_id_number.tif" % subdir
                                                            , geotransform_obj
                                                            , Reference.shape
                                                            , data_type=data_type_int)
    print( - st + time.time())
    
    SaveLayerDict = {}
    
        
    GFA_res, geotransform_obj = CRL.clip_raster_layer("input/%sgfa_res_curr_density.tif" % subdir
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type) 
    
    SaveLayerDict["f"] = ("input/cut/sgfa_res_curr_density.tif"
                            , geotransform_obj
                            , data_type
                            , GFA_res, 0)
    ENERGY_RES, geotransform_obj = CRL.clip_raster_layer("input/%sheat_res_curr_density.tif" % subdir
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type)
    SaveLayerDict["e"] = ("input/cut/heat_res_curr_density.tif"
                            , geotransform_obj
                            , data_type
                            , ENERGY_RES, 0)
    
    SaveLayerDict = expLyr(SaveLayerDict)
        
     
    LAU2_id, geotransform_obj = CRL.clip_raster_layer("input/%sLAU2_id_number.tif" % subdir
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type_int)  
    
    #LAU2_id, _  =  SF.rrl("input/LAU2_id_number.tif", data_type=data_type_int)
    print(LAU2_id.shape)
    cp_share_1975, geotransform_obj = CRL.clip_raster_layer("input/%sGHS_BUILT_1975_100_share.tif" % subdir
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type)
    print(cp_share_1975.shape)
    print( - st + time.time())
    cp_share_1990, geotransform_obj = CRL.clip_raster_layer("input/%sGHS_BUILT_1990_100_share.tif" % subdir
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type)
    print( - st + time.time())
    cp_share_2000, geotransform_obj = CRL.clip_raster_layer("input/%sGHS_BUILT_2000_100_share.tif" % subdir
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type)
    print( - st + time.time())
    cp_share_2014, geotransform_obj = CRL.clip_raster_layer("input/%sGHS_BUILT_2014_100_share.tif" % subdir
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type)
    print( - st + time.time())
    ENERGY_RES, geotransform_obj = CRL.clip_raster_layer("input/%sheat_res_curr_density.tif" % subdir
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type)
    print( - st + time.time())
    """ENERGY_NRES, geotransform_obj = CRL.clip_raster_layer("input/%sheat_nonres_curr_density.tif" % subdir
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type)    
    
    
    print( - st + time.time())
    """
    #cp_share_1990 = cp_share_1975
    #cp_share_2000 = cp_share_1975
    #cp_share_2014 = cp_share_1975
    SaveLayerDict["a"] = ("input/%sNUTS3_cut_id_number.tif" % subdir
                            , geotransform_obj
                            , data_type_int
                            , NUTS_id, 0)
    SaveLayerDict["c"] = ("input/cut/LAU2_id_number.tif"
                            , geotransform_obj
                            , data_type_int
                            , LAU2_id, 0)
    SaveLayerDict["b"] = ("input/cut/GHS_BUILT_1975_100_share.tif"
                            , geotransform_obj
                            , data_type
                            , cp_share_1975, 0)
    SaveLayerDict["d"] = ("input/cut/GHS_BUILT_1990_100_share.tif"
                            , geotransform_obj
                            , data_type
                            , cp_share_1990, 0)
    SaveLayerDict["e"] = ("input/cut/GHS_BUILT_2000_100_share.tif"
                            , geotransform_obj
                            , data_type
                            , cp_share_2000, 0)
    SaveLayerDict["f"] = ("input/cut/GHS_BUILT_2014_100_share.tif"
                            , geotransform_obj
                            , data_type
                            , cp_share_2014, 0)
    SaveLayerDict["g"] = ("input/cut/RESULTS_ENERGY_HEATING_RES_2012.tif"
                            , geotransform_obj
                            , data_type
                            , ENERGY_RES, 0)

    
      
    if reshaped == True:    
        SaveLayerDict = expLyr(SaveLayerDict)
    else:
        del SaveLayerDict
    NUTS_RESULTS_ENERGY_BASE = READ_CSV_DATA("input/RESULTS_SHARES_2012.csv", skip_header=3)[0]
    NUTS_RESULTS_ENERGY_FUTURE = READ_CSV_DATA("input/RESULTS_SHARES_2030.csv", skip_header=3)[0]
    NUTS_RESULTS_ENERGY_FUTURE_abs = READ_CSV_DATA("input/RESULTS_ENERGY_2030.csv", skip_header=3)[0]
    NUTS_RESULTS_GFA_BASE =   READ_CSV_DATA("input/RESULTS_GFA_2012.csv", skip_header=3)[0]
    NUTS_RESULTS_GFA_FUTURE = READ_CSV_DATA("input/RESULTS_GFA_2030.csv", skip_header=3)[0]

    csv_data_table = READ_CSV_DATA("input/Communal2_data.csv", skip_header=6)
    
    
    fn_res_bgf_initial = "input/%sRESULTS_GFA_RES_BUILD.tif" % subdir
    #fn_nres_bgf_initial = "input/%sRESULTS_GFA_NRES_BUILD.tif" % subdir
    SaveLayerDict = {}
    """
    A, geotransform_obj = CRL.clip_raster_layer("input/RESULTS_GFA_RES_BUILD.tif"
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type)
    V, geotransform_obj = CRL.clip_raster_layer("input/RESULTS_GFA_NRES_BUILD.tif"
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type)
    SaveLayerDict["12"] = ("input/cut/RESULTS_GFA_RES_BUILD.tif"
                            , geotransform_obj
                            , data_type
                            , A, 0)
    SaveLayerDict["13"] = ("input/cut/RESULTS_GFA_NRES_BUILD.tif"
                            , geotransform_obj
                            , data_type
                            , V, 0)
    SaveLayerDict = expLyr(SaveLayerDict)
    
    
    ENERGY_RES = CRL.clip_raster_layer(fn_res_bgf_initial
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type)[0] * 100
    
    GFA_RES, geotransform_obj = CRL.clip_raster_layer("input/%sgfa_res_curr_densisty.tif" % subdir
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type) 
    
    s = np.minimum(10, ENERGY_RES/ (0.000001 + GFA_RES)) *1000
    SaveLayerDict["xx"] = ("input/cut/spec_heat_demand_2012.tif"
                            , geotransform_obj
                            , data_type
                            , s, 0)
    
    SaveLayerDict = expLyr(SaveLayerDict)
    """
    _, _ = CalcEffectsAtRasterLevel(NUTS_RESULTS_GFA_BASE
                            , NUTS_RESULTS_GFA_FUTURE
                            , NUTS_RESULTS_ENERGY_BASE
                            , NUTS_RESULTS_ENERGY_FUTURE
                            , NUTS_RESULTS_ENERGY_FUTURE_abs
                            , NUTS_id
                            , LAU2_id
                            , cp_share_1975
                            , cp_share_1990
                            , cp_share_2000 + cp_share_2014
                            , ENERGY_RES
                            , GFA_res
                            , geotransform_obj, NUTS_id.shape
                            , csv_data_table
                            , fn_res_bgf_initial)
    
    
    
    
    
    
    

if __name__ == "__main__":
    print('calculation started')
    main()

#import sys;sys.path.append(r'/home/simulant/.eclipse/org.eclipse.platform_3.8_155965261/plugins/org.python.pydev_4.5.5.201603221110/pysrc')
#import pydevd;pydevd.settrace()