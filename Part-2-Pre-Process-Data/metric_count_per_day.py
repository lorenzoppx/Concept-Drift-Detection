import pandas as pd
import glob
import h5py
import numpy as np

print(glob.glob("../Part-1-Extract-Data/Data-Extracted/LABIC-Vacinal/*.hdf5"))


# Janela de 2 dias sem sobreposição
for file_path_origin in [glob.glob("../Part-1-Extract-Data/Data-Extracted/LABIC-Vacinal/*.hdf5")[0]]:

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
        print(file_path_origin,':',counts_per_day)

        # Convert to datetime index
        df = pd.DataFrame({
            'datetime': datetimes,
            'E': list(f["E"][:]),  # caso E seja array 2D, use list para manter as linhas
            'Y_predicted': f["Y_predicted"][:].reshape(-1),
            'Y_original': f["Y_original"][:].reshape(-1),
            'Y_original_names': f["Y_original_names"][:].reshape(-1),
            'Y_predicted_names': f["Y_predicted_names"][:].reshape(-1)
        })
        df.set_index('datetime', inplace=True)

        # Group in 2-day intervals (resample by 2 days)
        counts_per_2days = df.resample('2D').size()

        #print(counts_per_2days)
        break

        print(file_path_origin)

        # 2. Agrupar em blocos de 2 dias e acessar os samples diretamente
        grouped = df.groupby(pd.Grouper(freq='2D'))

        # 3. Exemplo: imprimir os índices de cada grupo (ou os dados originais)
        for start_time, group in grouped:
            print(f"\nIntervalo: {start_time} → {start_time + pd.Timedelta(days=2)}")
            #print(group.values[0][0][0:10])  # ou group.index para ver os datetimes
            print(len(group.values))

        print(10*'-')

# Janela de 2 dias com sobreposição
from datetime import timedelta

for file_path_origin in [glob.glob("../Part-1-Extract-Data/Data-Extracted/LABIC-Vacinal/*.hdf5")[0]]:

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

        # Convert to datetime index
        df = pd.DataFrame({
            'datetime': datetimes,
            'E': list(f["E"][:]),  # caso E seja array 2D, use list para manter as linhas
            'Y_predicted': f["Y_predicted"][:].reshape(-1),
            'Y_original': f["Y_original"][:].reshape(-1),
            'Y_original_names': f["Y_original_names"][:].reshape(-1),
            'Y_predicted_names': f["Y_predicted_names"][:].reshape(-1)
        })
        df.set_index('datetime', inplace=True)


        window_size = timedelta(days=2)
        step_size = timedelta(days=1)  # ou menos, se quiser janela mais "deslizante"

        start_time = df.index.min().normalize()
        end_time = df.index.max()

        while start_time + window_size <= end_time:
            end_window = start_time + window_size
            window_df = df[(df.index >= start_time) & (df.index < end_window)]

            print(window_df.values[0][0][:10])
            print(f"\n🔷 Janela: {start_time} → {end_window}")
            print("Total samples:", len(window_df))
            # Aqui você pode processar ou salvar `window_df`
            # ex: window_df.to_csv(f"window_{start_time.date()}_{end_window.date()}.csv")

            # Avança a janela
            start_time += step_size
