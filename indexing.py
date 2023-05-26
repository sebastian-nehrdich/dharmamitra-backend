import faiss
import fasttext
import pandas as pd 
import pyewts
import numpy as np
from pandarallel import pandarallel
import os 
import chinese_converter as cc

pandarallel.initialize()
pyewts = pyewts.pyewts()


class Index:
    SENTENCE_PATH: str
    FASTTEXT_PATH: str 

    def __init__(self):        
        self.fasttext = fasttext.load_model(self.FASTTEXT_PATH)
        self.sentences = pd.read_csv(self.SENTENCE_PATH, sep='\t', encoding='utf-8', names=['input_text', 'target_text'], on_bad_lines='skip')
        # remove duplicate input_text
        self.sentences = self.sentences.drop_duplicates(subset=['input_text'])        
        self.sentences = self.sentences[self.sentences['input_text'].str.len() < 200]
        self.sentences = self.sentences[self.sentences['target_text'].str.len() < 200]

        # create hnsw index
        dim = self.fasttext.get_dimension()
        if not os.path.exists(self.SENTENCE_PATH + ".idx"):
            self.index = faiss.IndexHNSWFlat(dim, 32)
            print("GOT HERE")
            self.index.hnsw.efSearch = 128
            #self.index = faiss.IndexFlatIP(dim)
            self.index.verbose = True
            # add sentences to index
            tib_vectors = []

            self.sentences['vectors'] = self.sentences['input_text'].apply(lambda x: self.fasttext.get_sentence_vector(x))
            # convert vectors to numpy array
            tib_vectors = np.array(self.sentences['vectors'].tolist())
            faiss.normalize_L2(tib_vectors)
            self.index.add(tib_vectors)
            faiss.write_index(self.index, self.SENTENCE_PATH + ".idx")
        else:
            self.index = faiss.read_index(self.SENTENCE_PATH + ".idx")
            

    def search(self, query, k):
        input_sentences = query.split("\n")
        print("INPUT SENTENCES", input_sentences)
        query_vectors = []
        for sentence in input_sentences:
            query_vectors.append(self.fasttext.get_sentence_vector(sentence))
        if len(query_vectors) >= k:
            k = 1
        else:
            k = int(k / len(query_vectors))        
        D, I = self.index.search(np.asarray(query_vectors), k)
        result = []
        for i in range(len(I)):
            for i in range(len(I[i])):
                result.append([self.sentences.iloc[I[0][i]]['input_text'], self.sentences.iloc[I[0][i]]['target_text']])

        return result


class TibIndex(Index):
    SENTENCE_PATH = 'data/tibetan_sentences_wylie.tsv'
    FASTTEXT_PATH = 'fasttext_models/tib.bin'

class ChnIndex(Index):
    SENTENCE_PATH = 'data/chinese_sentences.tsv'
    FASTTEXT_PATH = 'fasttext_models/chn.bin'

class SktIndex(Index):
    SENTENCE_PATH = 'data/sanskrit_sentences.tsv'
    FASTTEXT_PATH = 'fasttext_models/skt.bin'
