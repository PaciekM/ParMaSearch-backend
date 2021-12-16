import operator
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


class Search(Enum):
    TITLE = "TITLE"
    TEXT = "TEXT"
    MIX = "MIX"


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
    print(word_tokenize(value))
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
        print(element.val)
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
        if type is Search.TITLE:
            return filter_data_title(value, Document.objects.all())
        if type is Search.TEXT:
            return filter_data_title(value, Document.objects.all())
        if type is Search.MIX:
            return filter_data_title(value, Document.objects.all())
