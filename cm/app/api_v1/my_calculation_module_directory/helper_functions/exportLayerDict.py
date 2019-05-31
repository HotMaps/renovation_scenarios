'''
Created on Feb 3, 2018

@author: simulant
'''
#import time

import helper_functions.array2raster as a2r
DONTEXPORT_temp = False
DONTEXPORT_existing = False
import os

def export_layer(SaveLayerDict):
    
    
    print ("Export Layers:")
    #st = time.time()
    for k in list(SaveLayerDict.keys()):
        #st1 = time.time()
        LL = SaveLayerDict[k]
        #print (LL[0])
        if DONTEXPORT_temp == True and  "/Temp/" in LL[0]:
            pass
        else:
            if type(LL[3]) is str:
                pass
                print ("already exported")
            else:
                try:
                    pass
                    if DONTEXPORT_existing == False or not os.path.exists(LL[0]):
                        a2r.array2rasterfileList(LL)
                    else:
                        print("Not exporting {}".format(LL[0]))
                except Exception as e:
                    print (e)
        del SaveLayerDict[k]
        
    #print("   Process Export Layers took: %4.1f seconds" %(time.time() - st)) 
    
    return(SaveLayerDict)