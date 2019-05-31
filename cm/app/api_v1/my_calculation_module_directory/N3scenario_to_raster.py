# -*- coding: utf-8 -*-
'''
This script has been created in the context of the Hotmaps EU project.

@author: Andreas Mueller
@Institute: TUW, Austria
@Contact: mueller@eeg.tuwien.ac.at
'''

import numpy as np
import time
import os



TARGET_RESOLUTION = 100

from helper_functions.exportLayerDict import export_layer as expLyr
import helper_functions.cyf.create_density_map as CDM
import helper_functions.cliprasterlayer as CRL


def getData(fn, geotransform_obj, size, data_type):
    
    
    ARR, geotransform_obj = CRL.clip_raster_layer(fn
                , geotransform_obj
                , size
                , data_type=data_type) 
        
    return ARR

                            
                            
def CalcEffectsAtRasterLevel(NUTS_RESULTS_GFA_BASE
                            , NUTS_RESULTS_GFA_FUTURE
                            , NUTS_RESULTS_ENERGY_BASE
                            , NUTS_RESULTS_ENERGY_FUTURE
                            , NUTS_RESULTS_ENERGY_FUTURE_abs
                            , NUTS_id
                            , LAU2_id
                            , cp_share_1975
                            , cp_share_1990
                            , cp_share_2014
                            , ENERGY_RES
                            , GFA_RES
                            , geotransform_obj, size
                            , csv_data_table
                            , fn_res_bgf_intial
                            , output_path="./output/"):
    
    """
    idx = NUTS_id < 1
    NUTS_id[idx] = 1
    del idx
    NUTS_id -= 1
    """

    if os.path.exists(output_path) == False:
        os.mkdir(output_path)
    
    csv_results = np.zeros((np.max(LAU2_id)+1, 100), dtype="f4")
    header = {}
    oNUTS = 40
    for i in range(1):
        energy_current = np.zeros_like(cp_share_1975)
        energy_future = np.zeros_like(cp_share_1975)
    
        area_future = np.zeros_like(cp_share_1975)
        area_current = np.zeros_like(cp_share_1975)
    
        Share_cp_area_initial = np.zeros((NUTS_RESULTS_GFA_BASE.shape[0]+1, 4), dtype="f4")
        Share_cp_area_future = np.zeros((NUTS_RESULTS_GFA_FUTURE.shape[0]+1, 4), dtype="f4")
        Share_cp_energy_initial = np.zeros((NUTS_RESULTS_ENERGY_BASE.shape[0]+1, 3), dtype="f4")
        Share_cp_energy_future = np.zeros((NUTS_RESULTS_ENERGY_FUTURE.shape[0]+1, 3), dtype="f4")
        
        if i == 0:
            o = 0
            bt_type = "Res"
            ENERGY = ENERGY_RES
            del ENERGY_RES
            BGF_intial = GFA_RES    # getData(fn_res_bgf_intial, geotransform_obj, size, "f4")
            
            Share_cp_area_initial[1:, 0] = (NUTS_RESULTS_GFA_BASE["gfa_sfh_1977"] + NUTS_RESULTS_GFA_BASE["gfa_mfh_1977"])
            Share_cp_area_initial[1:, 1] = (NUTS_RESULTS_GFA_BASE["gfa_sfh_77_90"] + NUTS_RESULTS_GFA_BASE["gfa_mfh_77_90"])
            Share_cp_area_initial[1:, 2] = (NUTS_RESULTS_GFA_BASE["gfa_sfh_90_17"] + NUTS_RESULTS_GFA_BASE["gfa_mfh_90_17"])
            Share_cp_area_initial[1:, 3] = (NUTS_RESULTS_GFA_BASE["gfa_sfh_2017__"] + NUTS_RESULTS_GFA_BASE["gfa_mfh_2017__"])
            
            Share_cp_area_future[1:, 0] = (NUTS_RESULTS_GFA_FUTURE["gfa_sfh_1977"] + NUTS_RESULTS_GFA_FUTURE["gfa_mfh_1977"])
            Share_cp_area_future[1:, 1] = (NUTS_RESULTS_GFA_FUTURE["gfa_sfh_77_90"] + NUTS_RESULTS_GFA_FUTURE["gfa_mfh_77_90"])
            Share_cp_area_future[1:, 2] = (NUTS_RESULTS_GFA_FUTURE["gfa_sfh_90_17"] + NUTS_RESULTS_GFA_FUTURE["gfa_mfh_90_17"])
            Share_cp_area_future[1:, 3] = (NUTS_RESULTS_GFA_FUTURE["gfa_sfh_2017__"] + NUTS_RESULTS_GFA_FUTURE["gfa_mfh_2017__"])
            
            Share_cp_energy_initial[1:, 0] = 0.5 * (NUTS_RESULTS_ENERGY_BASE["share_sfh_1977"] + NUTS_RESULTS_ENERGY_BASE["share_mfh_1977"])
            Share_cp_energy_initial[1:, 1] = 0.5 * (NUTS_RESULTS_ENERGY_BASE["share_sfh_77_90"] + NUTS_RESULTS_ENERGY_BASE["share_mfh_77_90"])
            Share_cp_energy_initial[1:, 2] = 0.5 * (NUTS_RESULTS_ENERGY_BASE["share_sfh_90_17"] + NUTS_RESULTS_ENERGY_BASE["share_mfh_90_17"])
            
            Share_cp_energy_future[1:, 0] = 0.5 * (NUTS_RESULTS_ENERGY_FUTURE["share_sfh_1977"] + NUTS_RESULTS_ENERGY_FUTURE["share_mfh_1977"])
            Share_cp_energy_future[1:, 1] = 0.5 * (NUTS_RESULTS_ENERGY_FUTURE["share_sfh_77_90"] + NUTS_RESULTS_ENERGY_FUTURE["share_mfh_77_90"])
            Share_cp_energy_future[1:, 2] = 0.5 * (NUTS_RESULTS_ENERGY_FUTURE["share_sfh_90_17"] + NUTS_RESULTS_ENERGY_FUTURE["share_mfh_90_17"])

        else:
            continue
            """
            o = 23
            bt_type = "NRes"
            BGF_intial = getData(fn_nres_bgf_intial, geotransform_obj, size, "f4")
            
            Share_cp_area_initial = np.zeros((NUTS_RESULTS_GFA_BASE.shape[0]+1, 4), dtype="f4")
            Share_cp_area_initial[1:, 0] = NUTS_RESULTS_GFA_BASE["gfa_nres_1977"]
            Share_cp_area_initial[1:, 1] = NUTS_RESULTS_GFA_BASE["gfa_nres_77_90"]
            Share_cp_area_initial[1:, 2] = NUTS_RESULTS_GFA_BASE["gfa_nres_90_17"]
            Share_cp_area_initial[1:, 3] = NUTS_RESULTS_GFA_BASE["gfa_nres_2017__"]
            

            
            Share_cp_area_future[1:, 0] = NUTS_RESULTS_GFA_FUTURE["gfa_nres_1977"]
            Share_cp_area_future[1:, 1] = NUTS_RESULTS_GFA_FUTURE["gfa_nres_77_90"]
            Share_cp_area_future[1:, 2] = NUTS_RESULTS_GFA_FUTURE["gfa_nres_90_17"]
            Share_cp_area_future[1:, 3] = NUTS_RESULTS_GFA_FUTURE["gfa_nres_2017__"]
            
            
            Share_cp_energy_initial[1:, 0] = NUTS_RESULTS_ENERGY_BASE["share_nres_1977"]
            Share_cp_energy_initial[1:, 1] = NUTS_RESULTS_ENERGY_BASE["share_nres_77_90"]
            Share_cp_energy_initial[1:, 2] = NUTS_RESULTS_ENERGY_BASE["share_nres_90_17"]
            
            
            Share_cp_energy_future[1:, 0] = NUTS_RESULTS_ENERGY_FUTURE["share_nres_1977"]
            Share_cp_energy_future[1:, 1] = NUTS_RESULTS_ENERGY_FUTURE["share_nres_77_90"]
            Share_cp_energy_future[1:, 2] = NUTS_RESULTS_ENERGY_FUTURE["share_nres_90_17"]
            """
        
        # Future shares based on current area
        Share_cp_area_future /= (np.ones((4,1),dtype="f4") 
                                 * np.maximum(0.1, np.sum(Share_cp_area_initial, axis=1))).T
                                 
        Share_cp_area_initial /= (np.ones((4,1),dtype="f4") 
                                 * np.maximum(0.1, np.sum(Share_cp_area_initial, axis=1))).T
                                    
        oL = o 
        oN = o + oNUTS
        TABLE_RESULTS_LAU = CDM.CreateResultsTableperIndicator(BGF_intial, LAU2_id) 
        TABLE_RESULTS_NUTS = CDM.CreateResultsTableperIndicator(BGF_intial, NUTS_id) 
        
        """ """                  
        # Get NUTS ID per LAU Region: 2 different versions
        # 1st From images
        NUTS_ID = np.rint(CDM.CreateResultsTableperIndicator(NUTS_id, LAU2_id, return_mean=1)).astype("uint32")[:,[0,3]]
        # 2nd via Table
        D = np.zeros((np.max(csv_data_table[0]["LAU_UNIQUEDATA_ID"])+1, 2), dtype="uint32")
        idx = csv_data_table[0]["LAU_UNIQUEDATA_ID"]
        D[idx, 1] = csv_data_table[0]["NUTS3_ID"]
        D[idx, 0] = idx
        # NUTS3_ID: 1st col = LAU ID, 2nd col = NUTS ID
        NUTS3_ID = D[np.rint(TABLE_RESULTS_LAU[:,0]).astype("uint32"), 1]
        NUTS3_ID[NUTS3_ID > TABLE_RESULTS_NUTS[-1,0]] = 0
        header[0] = "LAU UNIQUEData ID"
        header[1] = "NUTS ID"
        header[2] = "NUTS ID"
        csv_results[:,:2] = NUTS_ID
        csv_results[:,2] = NUTS3_ID
        del D, idx
        """ 
        Initial BGF
        """ 
        col = 3 
        header[col + oL] = "Initial BGF total %s" % bt_type
        csv_results[:,col + oL] = TABLE_RESULTS_LAU[:,1]
        header[col + oN] = "Initial BGF total %s" % bt_type
        csv_results[:,col + oN] = TABLE_RESULTS_NUTS[NUTS3_ID, 1]
        
        """ 
        Future BGF
        """ 
        
        col = 3 
        header[col + oL] = "Initial BGF total %s" % bt_type
        csv_results[:,col + oL] = TABLE_RESULTS_LAU[:,1]
        header[col + oN] = "Initial BGF total %s" % bt_type
        csv_results[:,col + oN] = TABLE_RESULTS_NUTS[NUTS3_ID, 1]
        
     
        # CLuster construction periods: Until 1977; 1978 - 1990; 1991 - 2011
        # Run through construction periods
        for i_cp_ in range(3):
            if i_cp_ == 0:
                cp_share = cp_share_1975
            elif i_cp_ == 1:
                cp_share = cp_share_1990
            else:
                cp_share = cp_share_2014
                
            AREA = cp_share * BGF_intial
            TABLE_RESULTS_LAU = CDM.CreateResultsTableperIndicator(AREA, LAU2_id) 
            TABLE_RESULTS_NUTS = CDM.CreateResultsTableperIndicator(AREA, NUTS_id) 
            area_current += AREA
            
            col = 4+i_cp_
            header[col+oL] = "Initial BGF LAU %s CP idx %i" % (bt_type, i_cp_ + 1)
            csv_results[:,col+oL] = TABLE_RESULTS_LAU[:,1]   
            header[col+oN] = "Initial BGF NUTS %s CP idx %i" % (bt_type, i_cp_ + 1)
            csv_results[:,col+oN] = TABLE_RESULTS_NUTS[NUTS3_ID, 1] 
            

            SHARE_NUTS3_area_intial = Share_cp_area_initial[:, i_cp_][NUTS_id]
            ratio_px_vs_NUTS = cp_share / (0.0001 + SHARE_NUTS3_area_intial)
            del SHARE_NUTS3_area_intial
            
            
            # RES FUTURE AREA
            AREA = AREA.copy()
            AREA *= (Share_cp_area_future[:, i_cp_] / np.maximum(0.00001, Share_cp_area_initial[:, i_cp_]))[NUTS_id]     
            
            # Now it is the future demand
            TABLE_RESULTS_LAU = CDM.CreateResultsTableperIndicator(AREA, LAU2_id) 
            TABLE_RESULTS_NUTS = CDM.CreateResultsTableperIndicator(AREA, NUTS_id) 
            area_future += AREA
            del AREA
            col = 8+i_cp_
            header[col+oL] = "Future BGF LAU %s CP idx %i" % (bt_type, i_cp_ + 1)
            csv_results[:,col+oL] = TABLE_RESULTS_LAU[:,1]   
            header[col+oN] = "Future BGF NUTS %s CP idx %i" % (bt_type, i_cp_ + 1)
            csv_results[:,col+oN] = TABLE_RESULTS_NUTS[NUTS3_ID, 1]
            
            
            
            # CURRENT DEMAND
            
            SHARE_NUTS3_energy = ENERGY.copy()
            SHARE_NUTS3_energy *= ratio_px_vs_NUTS
            SHARE_NUTS3_energy *= Share_cp_energy_initial[:, i_cp_][NUTS_id]
            # At this stage it is the current demand
            TABLE_RESULTS_LAU = CDM.CreateResultsTableperIndicator(SHARE_NUTS3_energy, LAU2_id) 
            TABLE_RESULTS_NUTS = CDM.CreateResultsTableperIndicator(SHARE_NUTS3_energy, NUTS_id) 
            energy_current += SHARE_NUTS3_energy
            del SHARE_NUTS3_energy
            
            
            col = 12+i_cp_
            header[col+oL] = "Current Demand LAU RESB CP idx %i" % (i_cp_ + 1)
            csv_results[:,col+oL] = TABLE_RESULTS_LAU[:,1]   
            header[col+oN] = "Current Demand NUTS RESB CP idx %i" % (i_cp_ + 1) 
            csv_results[:,col+oN] = TABLE_RESULTS_NUTS[NUTS3_ID, 1]
            
            # RES FUTURE DEMAND
            SHARE_NUTS3_energy = ENERGY.copy()
            SHARE_NUTS3_energy *= ratio_px_vs_NUTS
            SHARE_NUTS3_energy *= Share_cp_energy_future[:, i_cp_][NUTS_id]      
            # Now it is the future demand
            TABLE_RESULTS_LAU = CDM.CreateResultsTableperIndicator(SHARE_NUTS3_energy, LAU2_id) 
            TABLE_RESULTS_NUTS = CDM.CreateResultsTableperIndicator(SHARE_NUTS3_energy, NUTS_id) 
            energy_future += SHARE_NUTS3_energy
            del SHARE_NUTS3_energy
            col = 20+i_cp_
            header[col+oL] = "Future Demand LAU RESB CP idx %i" % (i_cp_ + 1)
            csv_results[:,col+oL] = TABLE_RESULTS_LAU[:,1]   
            header[col+oN] = "Future Demand NUTS RESB CP idx %i" % (i_cp_ + 1) 
            csv_results[:,col+oN] = TABLE_RESULTS_NUTS[NUTS3_ID, 1]
            
        TABLE_RESULTS_LAU = CDM.CreateResultsTableperIndicator(energy_future, LAU2_id)
        TABLE_RESULTS_NUTS = CDM.CreateResultsTableperIndicator(energy_future, NUTS_id)
        col = 24 
        header[col+oL] = "Future Demand LAU %s" % bt_type
        csv_results[:,col+oL] = TABLE_RESULTS_LAU[:,1]
        header[col+oN] = "Future Demand NUTS %s"% bt_type
        csv_results[:,col+oN] = TABLE_RESULTS_NUTS[NUTS3_ID,1]
        
        TABLE_RESULTS_LAU = CDM.CreateResultsTableperIndicator(energy_current, LAU2_id)
        TABLE_RESULTS_NUTS = CDM.CreateResultsTableperIndicator(energy_current, NUTS_id)
        col = 25 
        header[col+oL] = "CURRENT Demand LAU %s" % bt_type
        csv_results[:,col+oL] = TABLE_RESULTS_LAU[:,1]
        header[col+oN] = "CURRENT Demand NUTS %s"% bt_type
        csv_results[:,col+oN] = TABLE_RESULTS_NUTS[NUTS3_ID,1]
        
        
        
        TABLE_RESULTS_LAU = CDM.CreateResultsTableperIndicator(area_future, LAU2_id)
        TABLE_RESULTS_NUTS = CDM.CreateResultsTableperIndicator(area_future, NUTS_id)
        col = 26 
        header[col+oL] = "Future AREA LAU %s" % bt_type
        csv_results[:,col+oL] = TABLE_RESULTS_LAU[:,1]
        header[col+oN] = "Future AREA NUTS %s"% bt_type
        csv_results[:,col+oN] = TABLE_RESULTS_NUTS[NUTS3_ID,1]
        
        TABLE_RESULTS_LAU = CDM.CreateResultsTableperIndicator(area_current, LAU2_id)
        TABLE_RESULTS_NUTS = CDM.CreateResultsTableperIndicator(area_current, NUTS_id)
        col = 27 
        header[col+oL] = "CURRENT AREA LAU %s" % bt_type
        csv_results[:,col+oL] = TABLE_RESULTS_LAU[:,1]
        header[col+oN] = "CURRENT AREA NUTS %s"% bt_type
        csv_results[:,col+oN] = TABLE_RESULTS_NUTS[NUTS3_ID,1]
        
            
        #Export IMAGE
        SaveLayerDict = {}

        fn_out_fp = "%s/Energy_%s.tif" % (output_path, bt_type)
        SaveLayerDict["AA"] =   (fn_out_fp, geotransform_obj
                                            , "f4", energy_future , 0)
        SaveLayerDict = expLyr(SaveLayerDict)
    

    header_names = NUTS_RESULTS_ENERGY_FUTURE_abs.dtype.names[0] 
    
    
    demand_new_build = (NUTS_RESULTS_ENERGY_FUTURE_abs['gfa_sfh_2017__']
                           + NUTS_RESULTS_ENERGY_FUTURE_abs['gfa_mfh_2017__']
                           + NUTS_RESULTS_ENERGY_FUTURE_abs['gfa_nres_2017__'] + 0.001)
    
    area_new_buildings = (NUTS_RESULTS_GFA_FUTURE['gfa_sfh_2017__']
                           + NUTS_RESULTS_GFA_FUTURE['gfa_mfh_2017__']
                           + NUTS_RESULTS_GFA_FUTURE['gfa_nres_2017__'] + 0.00001)
    area_existing_buildings = (NUTS_RESULTS_GFA_BASE['gfa_total_2017'])
    
    
    

    
    
    """
        BGF New buildings
    """
    AREA_NEW_BUILD_per_existing_area = np.minimum(1, (area_new_buildings / (0.000001+area_existing_buildings)))
    BGF_intial *= AREA_NEW_BUILD_per_existing_area[NUTS_id]
    TABLE_RESULTS_LAU = CDM.CreateResultsTableperIndicator(BGF_intial, LAU2_id)
    TABLE_RESULTS_NUTS = CDM.CreateResultsTableperIndicator(BGF_intial, NUTS_id)
    col += 1 
    header[col+oL] = "BGF LAU NewBuild"
    csv_results[:,col+oL] = TABLE_RESULTS_LAU[:,1]
    col += 1
    header[col+oN] = "BGF NUTS NewBuild"
    csv_results[:,col+oN] = TABLE_RESULTS_NUTS[NUTS3_ID,1]
    
    """
        Energy New buildings
    """
    DEMAND_NEW_BUILD_per_existing_area = (demand_new_build / area_new_buildings)
    BGF_intial *= DEMAND_NEW_BUILD_per_existing_area[NUTS_id]
    TABLE_RESULTS_LAU = CDM.CreateResultsTableperIndicator(BGF_intial, LAU2_id)
    TABLE_RESULTS_NUTS = CDM.CreateResultsTableperIndicator(BGF_intial, NUTS_id)
    col += 1 
    header[col+oL] = "Future Demand LAU NEW_build"
    csv_results[:,col+oL] = TABLE_RESULTS_LAU[:,1]
    col += 1
    header[col+oN] = "Future Demand NUTS NEW_build"
    csv_results[:,col+oN] = TABLE_RESULTS_NUTS[NUTS3_ID,1]
    
    
    
    TABLE_RESULTS_LAU = CDM.CreateResultsTableperIndicator(BGF_intial, LAU2_id)
    TABLE_RESULTS_NUTS = CDM.CreateResultsTableperIndicator(BGF_intial, NUTS_id)
    col += 1 
    header[col+oL] = "Future Demand LAU NEW_build"
    csv_results[:,col+oL] = TABLE_RESULTS_LAU[:,1]
    col += 1
    header[col+oN] = "Future Demand NUTS NEW_build"
    csv_results[:,col+oN] = TABLE_RESULTS_NUTS[NUTS3_ID,1]
    
    
    #INITIAL DEMAND JUST TO CHECK DATA
    
    TABLE_RESULTS_LAU = CDM.CreateResultsTableperIndicator(ENERGY, LAU2_id)
    TABLE_RESULTS_NUTS = CDM.CreateResultsTableperIndicator(ENERGY, NUTS_id)
    col += 1 
    header[col+oL] = "INITIAL Demand LAU RES"
    csv_results[:,col+oL] = TABLE_RESULTS_LAU[:,1]
    col += 1
    header[col+oN] = "INITIAL Demand NUTS RES"
    csv_results[:,col+oN] = TABLE_RESULTS_NUTS[NUTS3_ID,1]
    """
    TABLE_RESULTS_LAU = CDM.CreateResultsTableperIndicator(ENERGY, LAU2_id)
    TABLE_RESULTS_NUTS = CDM.CreateResultsTableperIndicator(ENERGY, NUTS_id)
    col += 1 
    header[col] = "INITIAL Demand LAU nRES"
    csv_results[:,col] = TABLE_RESULTS_LAU[:,1]
    col += 1
    header[col] = "INITIAL Demand NUTS nRES"
    csv_results[:,col] = TABLE_RESULTS_NUTS[NUTS3_ID,1]
    
    """     
    
    
    
    fn_out_csv = "%s/Results_table.csv" % output_path
    notempty = csv_results[:, 1] > 0.1                   
    header_ = ""
    for k in range(csv_results.shape[1]):
        if k in header.keys():
            header_ += header[k] 
        header_ += ","
    np.savetxt(fn_out_csv, csv_results[notempty, :], delimiter = ",", header = header_, comments="")
    
    print("Done")
    return 1, 2
    #return(energy_res, energy_nres)
            
            
    