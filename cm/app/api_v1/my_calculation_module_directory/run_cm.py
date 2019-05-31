import os
import time
import sys
import numpy as np
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.
                                                       abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)
from N3scenario_to_raster import CalcEffectsAtRasterLevel
from helper_functions.readCsvData import READ_CSV_DATA
import helper_functions.Subfunctions as SF
import helper_functions.cliprasterlayer as CRL
from helper_functions.exportLayerDict import export_layer as expLyr

print(sys.version_info)




def main(fn_reference_tif
         , fn_NUTS3_id_number
         , fn_gfa_res_curr
         , fn_heat_res_curr
         , fn_LAU2_id_number
         , fn_GHS_BUILT_1975_100_share
         , fn_GHS_BUILT_1990_100_share
         , fn_GHS_BUILT_2000_100_share
         , fn_GHS_BUILT_2014_100_share):
    
    st = time.time()
    #end_year = 2030
    #start_year = 2012
    data_type = "f4"
    data_type_int = "uint32"
    
    
    
    dirname = os.path.dirname(fn_reference_tif).replace("\\", "/")
    
    
    dirname2 = "/".join(dirname.split("/")[:-1])
    
    
    reshaped = False
    #subdir = ""
    #reshaped = True
    
    Reference, geotransform_obj = SF.rrl(fn_reference_tif, data_type=data_type_int)
    #NUTS_id, geotransform_obj = SF.rrl("input/NUTS3_cut_id_number.tif", data_type=data_type_int)
    NUTS_id, geotransform_obj = CRL.clip_raster_layer(fn_NUTS3_id_number
                                                            , geotransform_obj
                                                            , Reference.shape
                                                            , data_type=data_type_int)
    print( - st + time.time())
    
    SaveLayerDict = {}
    
        
    GFA_res, geotransform_obj = CRL.clip_raster_layer(fn_gfa_res_curr
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type) 
    
    fn_sgfa_res_curr_density = "%s/sgfa_res_curr_density.tif" % dirname
    SaveLayerDict["f"] = (fn_sgfa_res_curr_density
                            , geotransform_obj
                            , data_type
                            , GFA_res, 0)
    
    ENERGY_RES, geotransform_obj = CRL.clip_raster_layer(fn_heat_res_curr
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type)
    fn_heat_res_curr_densit = "%s/heat_res_curr_densit.tif" % dirname
    SaveLayerDict["e"] = (fn_heat_res_curr_densit
                            , geotransform_obj
                            , data_type
                            , ENERGY_RES, 0)
    
    SaveLayerDict = expLyr(SaveLayerDict)
        
     
    LAU2_id, geotransform_obj = CRL.clip_raster_layer(fn_LAU2_id_number
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type_int)  
    
    #LAU2_id, _  =  SF.rrl("input/LAU2_id_number.tif", data_type=data_type_int)
    print(LAU2_id.shape)
    cp_share_1975, geotransform_obj = CRL.clip_raster_layer(fn_GHS_BUILT_1975_100_share
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type)
    print(cp_share_1975.shape)
    print( - st + time.time())
    cp_share_1990, geotransform_obj = CRL.clip_raster_layer(fn_GHS_BUILT_1990_100_share
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type)
    print( - st + time.time())
    cp_share_2000, geotransform_obj = CRL.clip_raster_layer(fn_GHS_BUILT_2000_100_share
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type)
    print( - st + time.time())
    cp_share_2014, geotransform_obj = CRL.clip_raster_layer(fn_GHS_BUILT_2014_100_share
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type)
    print( - st + time.time())
    ENERGY_RES, geotransform_obj = CRL.clip_raster_layer(fn_heat_res_curr
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type)
    print( - st + time.time())
    """
    ENERGY_NRES, geotransform_obj = CRL.clip_raster_layer("input/%sheat_nonres_curr_density.tif" % subdir
                                                            , geotransform_obj
                                                            , NUTS_id.shape
                                                            , data_type=data_type)    
    
    
    print( - st + time.time())
    """
    #cp_share_1990 = cp_share_1975
    #cp_share_2000 = cp_share_1975
    #cp_share_2014 = cp_share_1975
    fn_nuts3 = "%s/NUTS3_cut_id_number.tif" % dirname
    SaveLayerDict["a"] = (fn_nuts3
                            , geotransform_obj
                            , data_type_int
                            , NUTS_id, 0)
    fn_lau2 = "%s/LAU2_id_number.tif" % dirname
    SaveLayerDict["c"] = (fn_lau2
                            , geotransform_obj
                            , data_type_int
                            , LAU2_id, 0)
    fn_GHS_BUILT_1975_100_share = "%s/GHS_BUILT_1975_100_share.tif" % dirname
    SaveLayerDict["b"] = (fn_GHS_BUILT_1975_100_share
                            , geotransform_obj
                            , data_type
                            , cp_share_1975, 0)
    fn_GHS_BUILT_1990_100_share = "%s/GHS_BUILT_1990_100_share.tif" % dirname
    SaveLayerDict["d"] = (fn_GHS_BUILT_1990_100_share
                            , geotransform_obj
                            , data_type
                            , cp_share_1990, 0)
    fn_GHS_BUILT_2000_100_share = "%s/GHS_BUILT_2000_100_share.tif" % dirname
    SaveLayerDict["e"] = (fn_GHS_BUILT_2000_100_share
                            , geotransform_obj
                            , data_type
                            , cp_share_2000, 0)
    fn_GHS_BUILT_2014_100_share = "%s/GHS_BUILT_2014_100_share.tif" % dirname
    SaveLayerDict["f"] = (fn_GHS_BUILT_2014_100_share
                            , geotransform_obj
                            , data_type
                            , cp_share_2014, 0)
    fn_RESULTS_ENERGY_HEATING_RES_2012 = "%s/RESULTS_ENERGY_HEATING_RES_2012.tif" % dirname
    SaveLayerDict["g"] = (fn_RESULTS_ENERGY_HEATING_RES_2012
                            , geotransform_obj
                            , data_type
                            , ENERGY_RES, 0)

    
      
    if reshaped == True:    
        SaveLayerDict = expLyr(SaveLayerDict)
    else:
        del SaveLayerDict
    dirname2 = "/".join(dirname.split("/")[:-1])
    fn_RESULTS_SHARES_2012 = "%s/RESULTS_SHARES_2012.csv" % dirname2
    NUTS_RESULTS_ENERGY_BASE = READ_CSV_DATA(fn_RESULTS_SHARES_2012, skip_header=3)[0]
    fn_RESULTS_SHARES_2030 = "%s/RESULTS_SHARES_2030.csv" % dirname2
    NUTS_RESULTS_ENERGY_FUTURE = READ_CSV_DATA(fn_RESULTS_SHARES_2030, skip_header=3)[0]
    fn_RESULTS_ENERGY_2030 = "%s/RESULTS_ENERGY_2030.csv" % dirname2
    NUTS_RESULTS_ENERGY_FUTURE_abs = READ_CSV_DATA(fn_RESULTS_ENERGY_2030, skip_header=3)[0]
    fn_RESULTS_GFA_2012 = "%s/RESULTS_GFA_2012.csv" % dirname2
    NUTS_RESULTS_GFA_BASE =   READ_CSV_DATA(fn_RESULTS_GFA_2012, skip_header=3)[0]
    fn_RESULTS_GFA_2030 = "%s/RESULTS_GFA_2030.csv" % dirname2
    NUTS_RESULTS_GFA_FUTURE = READ_CSV_DATA(fn_RESULTS_GFA_2030, skip_header=3)[0]
    fn_Communal2_data = "%s/Communal2_data.csv" % dirname2
    csv_data_table = READ_CSV_DATA(fn_Communal2_data, skip_header=6)
    
    
    fn_res_bgf_initial = "%s/RESULTS_GFA_RES_BUILD.csv" % dirname
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
    
    
    
    print("Done")
    
    
    

if __name__ == "__main__":
    print('calculation started')
    
    subdir = "cut/"
    dir_ = "../../../tests/data"
    fn_reference_tif = "%s/%sREFERENCE.tif" % (dir_, subdir)
    fn_NUTS3_id_number = "%s/%sNUTS3_cut_id_number.tif" % (dir_, subdir)
    fn_gfa_res_curr = "%s/%sgfa_res_curr_density.tif" % (dir_, subdir)
    fn_heat_res_curr = "%s/%sheat_res_curr_density.tif" % (dir_, subdir)
    
    fn_LAU2_id_number = "%s/%sLAU2_id_number.tif" % (dir_, subdir)
    
    fn_GHS_BUILT_1975_100_share = "%s/%sGHS_BUILT_1975_100_share.tif" % (dir_, subdir)
    fn_GHS_BUILT_1990_100_share = "%s/%sGHS_BUILT_1990_100_share.tif" % (dir_, subdir)
    fn_GHS_BUILT_2000_100_share = "%s/%sGHS_BUILT_2000_100_share.tif" % (dir_, subdir)
    fn_GHS_BUILT_2014_100_share = "%s/%sGHS_BUILT_2014_100_share.tif" % (dir_, subdir)


    main(fn_reference_tif
         , fn_NUTS3_id_number
         , fn_gfa_res_curr
         , fn_heat_res_curr
         , fn_LAU2_id_number
         , fn_GHS_BUILT_1975_100_share
         , fn_GHS_BUILT_1990_100_share
         , fn_GHS_BUILT_2000_100_share
         , fn_GHS_BUILT_2014_100_share)

#import sys;sys.path.append(r'/home/simulant/.eclipse/org.eclipse.platform_3.8_155965261/plugins/org.python.pydev_4.5.5.201603221110/pysrc')
#import pydevd;pydevd.settrace()