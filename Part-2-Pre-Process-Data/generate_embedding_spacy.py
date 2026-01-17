import pandas as pd
import spacy
from tqdm import tqdm
import numpy as np
import glob
from pathlib import Path

# Ensure the pandas progress bar is registered
tqdm.pandas()

def generate_embeddings_from_csv(input_csv, output_csv, text_column):
    """
    Generates embeddings for an input CSV without any text preprocessing.

    Args:
        input_csv (str): The path to the input CSV file.
        output_csv (str): The path for the output CSV file.
        text_column (str): The name of the column containing the text.
    """
    try:
        # Load the Portuguese medium model with vectors
        nlp = spacy.load("pt_core_news_lg")
        print("SpaCy model 'pt_core_news_lg' loaded successfully.")
    except OSError:
        print("Error: The 'pt_core_news_lg' model was not found.")
        print("Please run the command 'python -m spacy download pt_core_news_lg' to install it.")
        return

    # 1. Read the CSV file
    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        print(f"Error: The file {input_csv} was not found.")
        return

    if text_column not in df.columns:
        print(f"Error: The column '{text_column}' was not found in the CSV file.")
        return

    print(f"Generating embeddings for text in the '{text_column}' column...")

    # 2. Generate embeddings efficiently using nlp.pipe
    embeddings_list = []
    
    # nlp.pipe is faster for large datasets
    # tqdm is used to display a progress bar
    for doc in tqdm(nlp.pipe(df[text_column].astype(str)), total=len(df), desc="Generating embeddings"):
        if doc.has_vector:
            embeddings_list.append(doc.vector)
        else:
            # If the document has no vector (e.g., empty string), append a zero vector
            embeddings_list.append(np.zeros(nlp.vocab.vectors.shape[1]))

    # 3. Add the embeddings as a new column
    #df['embedding'] = embeddings_list
    df['embedding'] = ['[' + ','.join(map(str, vec)) + ']' for vec in embeddings_list]

    # 4. Save the DataFrame to a new CSV file
    df.to_csv(output_csv, index=False)
    
    print(f"\nEmbeddings generated and saved to {output_csv}")
    print(f"Number of vectors generated: {len(df)}")


if __name__ == "__main__":
    # --- Parameters you need to adjust ---
    text_column_name = "message"

    fl = glob.glob("../Part-1-Extract-Data/Data-Extracted/LABIC-MMA/s/*.csv")
    for input_file in fl:
        if 1:
            name = Path(input_file).name.replace('.csv','')
            name = 'spacy_' + name + '.csv'
            
            generate_embeddings_from_csv(input_file,Path(input_file).with_name(name), text_column_name)