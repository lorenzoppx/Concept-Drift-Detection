from datetime import datetime

def create_structure(file_path):
    file_w = h5py.File(file_path,'w')
    
    dt = h5py.string_dtype(encoding='utf-8')
    
    float_data = np.array([[0.0,1.0,2.0]])
    
    file_w.create_dataset('E', #data=float_data,
                        shape=(1,768),
                        maxshape=(None, None),
                        chunks=True)
    
    file_w.create_dataset('X', #data=float_data,
                        shape=(1,1),
                        dtype=dt,
                        maxshape=(None, None),
                        chunks=True)
    
    file_w.create_dataset('Data', #data=float_data,
                        shape=(1,1),
                        dtype=dt,
                        maxshape=(None, None),
                        chunks=True)

    file_w.create_dataset('Y_original', #data=float_data,
                        shape=(1,1),
                        maxshape=(None, None),
                        chunks=True)
    
    file_w.create_dataset('Y_original_names', #data=float_data,
                        shape=(1,1),
                        dtype=dt,
                        maxshape=(None, None),
                        chunks=True)
    
    file_w.create_dataset('Y_predicted', #data=float_data,
                        shape=(1,1),
                        maxshape=(None, None),
                        chunks=True)
    
    file_w.create_dataset('Y_predicted_names', #data=float_data,
                        shape=(1,1),
                        dtype=dt,
                        maxshape=(None, None),
                        chunks=True)
    file_w.close()
    
def convert_to_timestamp(time_str):
    try:
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.f")
    return dt.timestamp()


# Convert .csv to .hdf5

import h5py
import numpy as np
import ast
import pandas as pd
import glob
import os
from pathlib import Path


for file_path_origin in glob.glob("*.csv"):
    print(f"Init conversion csv to hdf5 of {file_path_origin}..")

    dir = 'hdf5_converted'
    os.makedirs(dir,exist_ok=True)

    name_file = file_path_origin.replace('.csv','')
    if 'mma' in file_path_origin:
        name_ = 'mma'
    else: 
        name_ = 'vacinal'
    path_file_name = Path(dir,f'embedding_{name_file}.hdf5')

    create_structure(path_file_name)

    file_r = h5py.File(path_file_name,'a')
    print("HDF5 file loaded successfully!")
    print("keys:",file_r.keys())

    #file_path = 'output_vacinal_12_04.csv'
    #file_path = 'output_vacinal_mar_val.csv'
    df = pd.read_csv(file_path_origin, sep=',')

    df['id'] = df['id'].astype(str)

    df = df.drop_duplicates(subset='id', keep='first')

    print("CSV file loaded successfully!")
    print(df.head())

    class_dict = {
        'vacinal':0,
        'mma':1
    }

    count = 0
    file_idx = 0
    for x in range(0,len(df)):
        print("-"*10)
        print(f"iteration:{x}")

        row = df.iloc[[x]]

        row_dict = {
        'E' : ast.literal_eval(row['embedding_openclip_text'].values[0]),
        'Data' : row['time'].values[0],
        'X' : row['message'].values[0],
        'Y_original' : class_dict[name_],
        'Y_original_names' : name_,
        'Y_predicted' : class_dict[name_],
        'Y_predicted_names' : name_
        }
        print(type(row_dict['X']))

        if pd.notna(row_dict['X']):
            for i in ['E', 'X', 'Data', 'Y_original', 'Y_original_names', 'Y_predicted', 'Y_predicted_names']:
        
                if x!=0:
                    new_len = file_r[i].shape[0] + 1
                    file_r[i].resize((new_len, file_r[i].shape[1]))
        
                #print(i)
                if i == 'E':
                    print(i+'-sample:',row_dict[i][0:10])
                else:
                    print(i+'-sample:',row_dict[i])
        
                #print("original:",file[i][x])
        
                file_r[i][file_idx] = row_dict[i]
        
                #for x in range(0,25):
                #    if(file["Y_original_names"][x]!=file["Y_predicted_names"][x]):
                #        print("Not equal",x)
            
            count+=1
            file_idx += 1
            #if count>=200000:
            #    break
    file_r.close()
    print('HDF5 writed successfully')