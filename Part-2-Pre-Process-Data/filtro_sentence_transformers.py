import pandas as pd
import re
from sentence_transformers import SentenceTransformer, util
import os
os.environ["USE_TF"] = "0"  # Impede que transformers tente importar TensorFlow

if __name__ == "__main__":
    argv = ['', 'output_mma_jan_fev_train.csv', 'output_mma_jan_fev_train_filtred.csv']

    print("Start processing...")

    # Lê o CSV
    df = pd.read_csv(argv[1], sep=',', encoding='utf-8')
    print(df.head())

    # Compila regex para emojis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # símbolos e pictogramas
        u"\U0001F680-\U0001F6FF"  # transporte e mapas
        u"\U0001F1E0-\U0001F1FF"  # bandeiras (iOS)
        u"\U00002702-\U000027B0"  # outros símbolos
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)

    # Pré-processamento
    def preprocess(texto):
        texto = str(texto).strip()
        texto = emoji_pattern.sub("", texto)
        texto = re.sub(r"http\S+", "URL", texto)
        texto = re.sub("à", "a", texto)
        texto = re.sub(r'\b\d+[\.\d]*[a-zA-Z]*\b', '', texto)  # remove 5, 6x, 6.5k etc.
        texto = re.sub(r'\s+', ' ', texto)
        return texto

    df["message"] = df["message"].astype(str).fillna("").apply(preprocess)

    # Carrega modelo BERT para embeddings semânticos
    model = SentenceTransformer("paraphrase-MiniLM-L6-v2")  # leve e eficiente

    # Gera embeddings
    print("Gerando embeddings...")
    sentences = df["message"].tolist()
    embeddings = model.encode(sentences, convert_to_tensor=True)

    # Define limiar de similaridade
    threshold = 0.9
    print(f"Filtrando frases com similaridade >= {threshold}")

    # Encontra mensagens únicas
    unique_indices = []
    for i in range(len(sentences)):
        is_similar = False
        for j in unique_indices:
            sim = util.cos_sim(embeddings[i], embeddings[j]).item()
            if sim >= threshold:
                is_similar = True
                break
        if not is_similar:
            unique_indices.append(i)
            print(f"Linha {i} mantida")
        else:
            print(f"Linha {i} removida (similar a {j})")

    # Filtra o DataFrame
    df_filtrado = df.iloc[unique_indices].reset_index(drop=True)

    # Salva novo CSV
    df_filtrado.to_csv(argv[2], index=False, encoding='utf-8')
    print(f"✅ CSV filtrado salvo como {argv[2]}")
