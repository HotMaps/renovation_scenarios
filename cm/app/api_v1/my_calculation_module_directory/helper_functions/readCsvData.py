'''
Created on Sep 21, 2017

@author: simulant
'''

import os
import numpy as np
import csv

def READ_CSV_DATA(filename, delimiter=",", skip_header=6):
    """
    Reads data from csv-file into a numpy recarray
    First ROW: Variable Name
    Second ROW: Data Type
    Third ROW: EXPORT DATA To RasterLayer (1 if True)
    Four ROW: Scaling Factor: 
    Five: Unit
    """
    
    if os.path.exists(filename) and os.path.isfile(filename):
        filename = filename
    else:
        exstring = "File " + filename + " does not exist."
        raise IOError(exstring)
    
    mapping = np.ndarray(shape=(0,0))
    """
    try:
        print("Loading format from file {0}".format(filename))
        np_version = np.__version__.split(".")
        if int(np_version[0])*100 + int(np_version[1]) >=116:
            mapping = np.loadtxt(filename, dtype="U1024", delimiter=delimiter, max_rows=10)
        else:
            mapping = np.loadtxt(filename, dtype="U1024", delimiter=delimiter)
        
        print("Imported format specification from textfile: {0}".format(filename))
    except (ValueError, TypeError) as ex:
        args = list(ex.args)
        for i in range(len(args)):
            args[i] = str(args[i])
        error_msg = ("Error while importing the format specification from textfile {0}: {1}".format(filename, "".join(args)))
        
        raise IOError(error_msg)
    except Exception as ex:
        print (ex)
     """   
        
    
    mapping_list =[]
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            mapping_list.append(row)
            line_count += 1
            if line_count >= skip_header or line_count > 5:
                break 
    mapping = np.asarray(mapping_list, dtype="U1024")
    
    #get Type and Name
    dtype = []
    EXPORT_COLUMNS = []
    SCALING_FACTOR = []
    CUTOFF_Value =  []
    j = 0
    for r in range(min(6, mapping.shape[0])):
        for col in range(mapping.shape[1]):
            if mapping[r, col].startswith("b'") and  mapping[r, col].endswith("'"):
                mapping[r, col] = mapping[r, col][2:-1]

    
    for row in mapping.transpose():
        if row[0] == "":
            j = j + 1 
            dtype.append(("emptycol_%i"%j, "f4"))
        else:
            if row[1].startswith("S"):
                row[1] = "U" + row[1][1:]
            dtype.append((row[0], row[1]))
            if row[2].strip() == "1":
                EXPORT_COLUMNS.append(row[0])
                try:
                    SCALING_FACTOR.append(eval(row[3]))
                except:
                    SCALING_FACTOR = [0]
                try:
                    CUTOFF_Value.append(eval(row[5]))
                except:
                    CUTOFF_Value = [0]
                    
                
            
        
    
            
    DATA = np.genfromtxt(filename, dtype=dtype, skip_header=skip_header,
                             delimiter=delimiter, missing_values="0", filling_values = "0" )       
         
    return DATA, EXPORT_COLUMNS, SCALING_FACTOR, CUTOFF_Value