import pandas as pd
import spacy,sys


if __name__ == "__main__":
    argv = ['','output_mma_jan_fev_train.csv', 'output_mma_jan_fev_train_filtred.csv']

    #if len(argv)>=3:
    print("Start processing..")
    # Carrega o modelo SpaCy com vetores (pt_core_news_md é melhor para português)
    nlp = spacy.load("pt_core_news_md")  # Instale com: python -m spacy download pt_core_news_md

    # Lê o CSV
    df = pd.read_csv(argv[1],sep=',',encoding='utf-8')

    print(df.head)

    import re
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # símbolos e pictogramas
        u"\U0001F680-\U0001F6FF"  # transporte e mapas
        u"\U0001F1E0-\U0001F1FF"  # bandeiras (iOS)
        u"\U00002702-\U000027B0"  # outros símbolos
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)

    df["message"] = df["message"].apply(lambda x: emoji_pattern.sub(" ", str(x)))
    df["message"] = df["message"].astype(str).fillna("")

    # Processa os textos
    docs = []
    for i, texto in enumerate(df["message"]):
        try:
            texto = re.sub(r"http\S+", "URL", texto)
            texto = re.sub("à", "a", texto)
            texto = emoji_pattern.sub("", texto)
            texto = re.sub(r'\b\d+[\.\d]*[a-zA-Z]*\b', '', texto)
            print(f"Texto:{texto}")
            doc = nlp(texto)
            docs.append(doc)
            print(f"Line processed: {str(i)}")
        except Exception as e:
            print(f"❌ Erro no índice {i} para o texto: {texto}")
            print(f"Motivo: {e}")
            #docs.append(None)  # ou ignore se quiser pular esse texto


    print(docs)
    # Define limiar de similaridade (ajuste conforme necessário)
    threshold = 0.9

    # Lista de índices únicos
    unique_indices = []

    for i, doc in enumerate(docs):
        is_similar = False
        for j in unique_indices:
            if doc.similarity(docs[j]) >= threshold:
                is_similar = True
                break
        if not is_similar:
            unique_indices.append(i)

    # Filtra o DataFrame com os textos únicos
    df_filtrado = df.iloc[unique_indices]

    # Salva para um novo CSV
    df_filtrado.to_csv(argv[2], index=False,encoding='utf-8')

    print(f"CSV filtrado salvo como {argv[2]}")
