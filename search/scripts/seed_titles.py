
import pandas as pd
from search.models import Document
import nltk
from nltk.tokenize import word_tokenize
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import os
from search.utils import cosine, listToString


def run():
    nltk.download('punkt')
    #sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
    data = pd.read_csv('./search/scripts/Fake.csv')
    half = 23482 / 2
    stop = 1000
    is_model = os.path.isfile('./model-d2v.bin')

    if is_model is True:
        model = Doc2Vec.load('./model-d2v.bin')
        print("Model loaded from file!")
    else:
        tokenized_sent = []
        for index, row in data.iterrows():
            tokenized_sent.append(word_tokenize(row['title']))
            tokenized_sent.append(word_tokenize(row['text']))
            if index == stop:
                break
        tagged_data = [TaggedDocument(d, [i])
                       for i, d in enumerate(tokenized_sent)]
        model = Doc2Vec(tagged_data, vector_size=40,
                        window=2, min_count=1, epochs=100)
        model.save("model-d2v.bin")
        print("Model created!")

    sent = []
    for index, row in data.iterrows():
        sent.append(row['title'])
        sent.append(row['text'])
        if index == stop:
            break

    title_vectors = []
    text_vectors = []

    for i in range(0, len(sent), 2):
        title_vectors.append(model.docvecs[i])
        text_vectors.append(model.docvecs[i+1])
    for index, row in data.iterrows():
        listToString(title_vectors[index])
        if index == stop:
            break
    print('...Inserting data')
    for index, row in data.iterrows():
        Document.objects.create(
            title=row['title'], text=row['text'], subject=row['subject'], title_vector=listToString(title_vectors[index]), text_vector=listToString(text_vectors[index]))
        if index == half:
            print("Half of database seeded")
        if index == stop:
            break
