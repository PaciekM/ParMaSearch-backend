from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from search.pagination import CustomPaginator
from search.models import Document
from search.serializers import DocumentSerializer
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import os
from search.utils import cosine
from sklearn.metrics.pairwise import cosine_similarity
from enum import Enum

# Create your views here.


class Search(str, Enum):
    TITLE = "TITLE"
    TEXT = "TEXT"
    MIX = "MIX"
    TITLE_TEXT = "TITLE_TEXT"
    TEXT_TITLE = "TEXT_TITLE"


class IndexWithVal:
    def __init__(self, index, val):
        self.val = val
        self.index = index


def filter_data_title(value, data):
    vectors_array = []
    for element in data:
        title_vector = element.title_vector.split(',')[:40]
        title_vector = [float(numeric_string)
                        for numeric_string in title_vector]
        vectors_array.append(np.array(title_vector))
    model = Doc2Vec.load('./model-d2v.bin')
    value_vector = model.infer_vector(word_tokenize(value))
    embedding_matrix = np.zeros((1, 40))
    embedding_matrix[0] = value_vector
    result_cosine = cosine_similarity(
        vectors_array, np.array(np.array(embedding_matrix)))
    result_cosine_with_index = []
    for index, element in enumerate(result_cosine):
        result_cosine_with_index.append(IndexWithVal(index, element[0]))
    sorted_array = []
    result_cosine_with_index.sort(
        key=lambda x: x.val, reverse=True)
    for element in result_cosine_with_index:
        # print(element.val)
        sorted_array.append(data[element.index])
    return sorted_array

def filter_data_text(value, data):
    vectors_array = []
    for element in data:
        text_vector = element.text_vector.split(',')[:40]
        text_vector = [float(numeric_string)
                        for numeric_string in text_vector]
        vectors_array.append(np.array(text_vector))
    model = Doc2Vec.load('./model-d2v.bin')
    value_vector = model.infer_vector(word_tokenize(value))
    embedding_matrix = np.zeros((1, 40))
    embedding_matrix[0] = value_vector
    result_cosine = cosine_similarity(
        vectors_array, np.array(np.array(embedding_matrix)))
    result_cosine_with_index = []
    for index, element in enumerate(result_cosine):
        result_cosine_with_index.append(IndexWithVal(index, element[0]))
    sorted_array = []
    result_cosine_with_index.sort(
        key=lambda x: x.val, reverse=True)
    for element in result_cosine_with_index:
        # print(element.val)
        sorted_array.append(data[element.index])
    return sorted_array

def filter_data_mix(value, data):
    vectors_array = dict()
    vectors_array['title'] = []
    vectors_array['text'] = []
    for element in data:
        title_vector = element.title_vector.split(',')[:40]
        title_vector = [float(numeric_string)
                        for numeric_string in title_vector]
        vectors_array['title'].append(np.array(title_vector))

        text_vector = element.text_vector.split(',')[:40]
        text_vector = [float(numeric_string)
                        for numeric_string in text_vector]
        vectors_array['text'].append(np.array(text_vector))
    
    model = Doc2Vec.load('./model-d2v.bin')
    value_vector = model.infer_vector(word_tokenize(value))
    embedding_matrix = np.zeros((1, 40))
    embedding_matrix[0] = value_vector

    result_cosine = dict()
    result_cosine['title'] = cosine_similarity(
        vectors_array['title'], np.array(np.array(embedding_matrix)))

    result_cosine['text'] = cosine_similarity(
        vectors_array['text'], np.array(np.array(embedding_matrix)))

    result_cosine_with_index = []
    for index, element in enumerate(result_cosine['title']):
        final_prob = element[0] * result_cosine['text'][index][0]
        result_cosine_with_index.append(IndexWithVal(index, final_prob))

    sorted_array = []
    result_cosine_with_index.sort(
        key=lambda x: x.val, reverse=True)
    for element in result_cosine_with_index:
        # print(element.val)
        sorted_array.append(data[element.index])
    return sorted_array

def filter_data_title_text(value, data):
    vectors_array = dict()
    vectors_array['title'] = []
    vectors_array['text'] = []
    for element in data:
        title_vector = element.title_vector.split(',')[:40]
        title_vector = [float(numeric_string)
                        for numeric_string in title_vector]
        vectors_array['title'].append(np.array(title_vector))

        text_vector = element.text_vector.split(',')[:40]
        text_vector = [float(numeric_string)
                        for numeric_string in text_vector]
        vectors_array['text'].append(np.array(text_vector))
    
    model = Doc2Vec.load('./model-d2v.bin')
    value_vector = model.infer_vector(word_tokenize(value))
    embedding_matrix = np.zeros((1, 40))
    embedding_matrix[0] = value_vector

    result_cosine = dict()
    result_cosine['title'] = cosine_similarity(
        vectors_array['title'], np.array(np.array(embedding_matrix)))

    result_cosine['text'] = cosine_similarity(
        vectors_array['text'], np.array(np.array(embedding_matrix)))

    result_cosine_with_index = []
    for index, element in enumerate(result_cosine['title']):
        final_prob = (element[0] * 0.7) + (result_cosine['text'][index][0] * 0.3)
        result_cosine_with_index.append(IndexWithVal(index, final_prob))

    sorted_array = []
    result_cosine_with_index.sort(
        key=lambda x: x.val, reverse=True)
    for element in result_cosine_with_index:
        # print(element.val)
        sorted_array.append(data[element.index])
    return sorted_array

def filter_data_text_title(value, data):
    vectors_array = dict()
    vectors_array['title'] = []
    vectors_array['text'] = []
    for element in data:
        title_vector = element.title_vector.split(',')[:40]
        title_vector = [float(numeric_string)
                        for numeric_string in title_vector]
        vectors_array['title'].append(np.array(title_vector))

        text_vector = element.text_vector.split(',')[:40]
        text_vector = [float(numeric_string)
                        for numeric_string in text_vector]
        vectors_array['text'].append(np.array(text_vector))
    
    model = Doc2Vec.load('./model-d2v.bin')
    value_vector = model.infer_vector(word_tokenize(value))
    embedding_matrix = np.zeros((1, 40))
    embedding_matrix[0] = value_vector

    result_cosine = dict()
    result_cosine['title'] = cosine_similarity(
        vectors_array['title'], np.array(np.array(embedding_matrix)))

    result_cosine['text'] = cosine_similarity(
        vectors_array['text'], np.array(np.array(embedding_matrix)))

    result_cosine_with_index = []
    for index, element in enumerate(result_cosine['text']):
        final_prob = (element[0] * 0.7) + (result_cosine['title'][index][0] * 0.3)
        result_cosine_with_index.append(IndexWithVal(index, final_prob))

    sorted_array = []
    result_cosine_with_index.sort(
        key=lambda x: x.val, reverse=True)
    for element in result_cosine_with_index:
        # print(element.val)
        sorted_array.append(data[element.index])
    return sorted_array


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]


class SearchResults(generics.ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    pagination_class = CustomPaginator

    def get_queryset(self):
        value = self.request.query_params.get('value')
        type = self.request.query_params.get('type')
        if value is None:
            return self.queryset
        if type == Search.TITLE:
            print('tajtul')
            return filter_data_title(value, Document.objects.all())
        if type == Search.TEXT:
            print('degzd')
            return filter_data_text(value, Document.objects.all())
        if type == Search.TITLE_TEXT:
            print('tajtul degzd')
            return filter_data_title_text(value, Document.objects.all())
        if type == Search.MIX:
            print('migz')
            return filter_data_mix(value, Document.objects.all())
        if type == Search.TEXT_TITLE:
            print('degzd tajtul')
            return filter_data_text_title(value, Document.objects.all())
        else:
            print('ELZE')
            return self.queryset
