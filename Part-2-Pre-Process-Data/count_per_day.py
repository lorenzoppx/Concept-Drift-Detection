import pandas as pd
import glob
import h5py
import numpy as np

for file_path_origin in glob.glob("*.hdf5"):

    # Abrir arquivo e carregar os timestamps do dataset 'E'
    with h5py.File(file_path_origin, 'r') as f:
        raw_timestamps = f['Data'][:]  # Lê todos os valores do dataset 'E'
        
    timestamps = [
        ts[0].decode('utf-8')
        for ts in raw_timestamps
        if ts and ts != b''
    ]
    r = [ts for ts in raw_timestamps if ts == b'']
    print("Colunas invalidas:",len(r))
    print("Colunas validas:",len(timestamps))

    #print(timestamps[1])

    datetimes = pd.to_datetime(timestamps,format="%Y-%m-%d %H:%M:%S")

    # Contar quantos por dia
    counts_per_day = pd.Series(datetimes.date).value_counts().sort_index()

    #print(pd.Series(datetimes.date).value_counts())

    counts_ = pd.Series(datetimes.date).value_counts().sort_values()

    print("Min value:",counts_.iloc[0])
    print("Max value:",counts_.iloc[-1])

    # Exibir o resultado
    #print(file_path_origin,':',counts_per_day)

    # Convert to datetime index
    df = pd.DataFrame({'datetime': datetimes})
    df.set_index('datetime', inplace=True)

    # Group in 2-day intervals (resample by 2 days)
    counts_per_2days = df.resample('2D').size()

    print(counts_per_2days)

    print(file_path_origin)
    print(10*'-')
