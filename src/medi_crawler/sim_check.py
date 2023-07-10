import gensim.downloader as api
import numpy as np
import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
import sys
import os
sys.path[0] = 'c:/Users/Robert/Documents/Projekte/dev/medi_crawler/'
os.chdir('c:/Users/Robert/Documents/Projekte/dev/medi_crawler/')
import config as CONFIG

def cosine_similarity(v1, v2):
    """Calculates the cosine similarity between two vectors."""
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return dot_product / (norm_v1 * norm_v2)

# Create a function to compute the similarity between two abstracts
def compute_similarity(abstract1, abstract2,model):
    # Tokenize the abstracts and remove stop words
    tokens1 = [t for t in abstract1.lower().split() if t in model.wv.vocab]
    tokens2 = [t for t in abstract2.lower().split() if t in model.wv.vocab]

    # Compute the word embeddings for each token in the abstracts
    embeddings1 = [model.wv[t] for t in tokens1 if t in model.wv.vocab]
    embeddings2 = [model.wv[t] for t in tokens2 if t in model.wv.vocab]

    # Compute the similarity between the embeddings using the cosine similarity metric
    if len(embeddings1) > 0 and len(embeddings2) > 0:
        
        sim_matrix = np.dot(embeddings1, np.transpose(embeddings2))
        sim = np.sum(sim_matrix) / (np.linalg.norm(embeddings1) * np.linalg.norm(embeddings2))
        return sim
    else:
        return 0
