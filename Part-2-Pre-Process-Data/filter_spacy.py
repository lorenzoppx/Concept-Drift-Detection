import pandas as pd
import spacy,sys
from pathlib import Path

# if __name__ == "__main__":
#     argv = ['','output_mma_jan_fev_train.csv', 'output_mma_jan_fev_train_filtred.csv']

#     #if len(argv)>=3:
#     print("Start processing..")
#     # Carrega o modelo SpaCy com vetores (pt_core_news_md é melhor para português)
#     nlp = spacy.load("pt_core_news_md")  # Instale com: python -m spacy download pt_core_news_md

#     # Lê o CSV
#     df = pd.read_csv(argv[1],sep=',',encoding='utf-8')

#     print(df.head)

#     import re
#     emoji_pattern = re.compile("["
#         u"\U0001F600-\U0001F64F"  # emoticons
#         u"\U0001F300-\U0001F5FF"  # símbolos e pictogramas
#         u"\U0001F680-\U0001F6FF"  # transporte e mapas
#         u"\U0001F1E0-\U0001F1FF"  # bandeiras (iOS)
#         u"\U00002702-\U000027B0"  # outros símbolos
#         u"\U000024C2-\U0001F251"
#         "]+", flags=re.UNICODE)

#     df["message"] = df["message"].apply(lambda x: emoji_pattern.sub(" ", str(x)))
#     df["message"] = df["message"].astype(str).fillna("")

#     # Processa os textos
#     docs = []
#     for i, texto in enumerate(df["message"]):
#         try:
#             texto = re.sub(r"http\S+", "URL", texto)
#             texto = re.sub(r"@\w+:", "", texto)
#             texto = re.sub("à", "a", texto)
#             texto = emoji_pattern.sub("", texto)
#             texto = re.sub(r'\b\d+[\.\d]*[a-zA-Z]*\b', '', texto)
#             print(f"Texto:{texto}")
#             doc = nlp(texto)
#             docs.append(doc)
#             print(f"Line processed: {str(i)}")
#         except Exception as e:
#             print(f"❌ Erro no índice {i} para o texto: {texto}")
#             print(f"Motivo: {e}")
#             #docs.append(None)  # ou ignore se quiser pular esse texto


#     print(docs)
#     # Define limiar de similaridade (ajuste conforme necessário)
#     threshold = 0.92

#     # Lista de índices únicos
#     unique_indices = []

#     for i, doc in enumerate(docs):
#         is_similar = False
#         for j in unique_indices:
#             if doc.similarity(docs[j]) >= threshold:
#                 is_similar = True
#                 break
#         if not is_similar:
#             unique_indices.append(i)

#     # Filtra o DataFrame com os textos únicos
#     df_filtrado = df.iloc[unique_indices]

#     # Salva para um novo CSV
#     df_filtrado.to_csv(argv[2], index=False,encoding='utf-8')

#     print(f"CSV filtrado salvo como {argv[2]}")

import pandas as pd
import spacy
import re
import glob

if __name__ == "__main__":
    fl = glob.glob("../Part-1-Extract-Data/Data-Extracted/LABIC-MMA/*.csv")
    for file_path_origin in fl:
        if 1:

            print("Start processing..")
            print(file_path_origin)
            # Carrega o modelo SpaCy com vetores
            nlp = spacy.load("pt_core_news_md")

            # Lê o CSV e faz a conversão da coluna 'date' para o formato datetime
            df = pd.read_csv(file_path_origin, sep=',', encoding='utf-8')

            df['id'] = df['id'].astype(str)

            df = df.drop_duplicates(subset='id', keep='first')

            # Assumindo que a sua coluna de data se chama 'date' ou algo parecido.
            # Se o nome for diferente, mude aqui: df['your_date_column_name']
            df['time'] = pd.to_datetime(df['time']) 
            print(df.head())

            emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"
                u"\U0001F300-\U0001F5FF"
                u"\U0001F680-\U0001F6FF"
                u"\U0001F1E0-\U0001F1FF"
                u"\U00002702-\U000027B0"
                u"\U000024C2-\U0001F251"
                "]+", flags=re.UNICODE)

            df["message"] = df["message"].apply(lambda x: emoji_pattern.sub(" ", str(x)))
            df["message"] = df["message"].astype(str).fillna("")
            df["message"] = df["message"].str.replace(r"@\S+", "", regex=True)
            df["message"] = df["message"].str.replace(r"http\S+", "", regex=True)

            # Define o limiar de similaridade
            threshold = 0.92
            
            # DataFrame para armazenar os resultados filtrados de cada dia
            df_filtrado_final = pd.DataFrame()

            # Agrupa o DataFrame por dia
            # Acessa a parte da data e ignora a hora
            for date, group in df.groupby(df['time'].dt.date):
                print(f"\nProcessando o dia: {date} com {len(group)} textos...")

                # Pré-processa os textos do grupo (dia) atual
                docs = []
                for i, texto in enumerate(group["message"]):
                    try:
                        texto = emoji_pattern.sub("", texto)
                        doc = nlp(texto)
                        docs.append(doc)
                    except Exception as e:
                        print(f"❌ Erro no índice {group.index[i]} para o texto: {texto}")
                        print(f"Motivo: {e}")
                        docs.append(None)

                # Filtra os documentos redundantes para o dia atual
                unique_indices_in_group = []
                if docs:
                    # Lista de índices dos documentos válidos (não None)
                    valid_indices = [i for i, doc in enumerate(docs) if doc is not None]
                    
                    # Mapeia os índices do grupo de volta para o DataFrame original
                    unique_original_indices = []

                    for i in valid_indices:
                        doc = docs[i]
                        is_similar = False
                        for j in unique_indices_in_group:
                            # Verifica se o documento atual é redundante em relação aos únicos já encontrados
                            if doc.similarity(docs[j]) >= threshold:
                                is_similar = True
                                break
                        if not is_similar:
                            unique_indices_in_group.append(i)
                            # Adiciona o índice original do DataFrame principal
                            unique_original_indices.append(group.index[i])
                
                # Concatena o grupo filtrado com o DataFrame final
                df_filtrado_final = pd.concat([df_filtrado_final, df.loc[unique_original_indices]])

            print(f"\nProcessamento concluído. Textos originais: {len(df)}. Textos filtrados: {len(df_filtrado_final)}.")
            
            name = Path(file_path_origin).name.replace('.csv','') 
            name = name + '_filtered_per_day.csv'

            # Salva para um novo CSV
            df_filtrado_final.to_csv( Path(file_path_origin).with_name(name), index=False, encoding='utf-8')

            print(f"CSV filtrado salvo como {name}")