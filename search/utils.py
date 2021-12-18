import numpy as np


def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


# def most_similar(doc_id, similarity_matrix, matrix):
#     if matrix == 'Cosine Similarity':
#         similar_ix = np.argsort(similarity_matrix[doc_id])[::-1]
#     elif matrix == 'Euclidean Distance':
#         similar_ix = np.argsort(similarity_matrix[doc_id])
#     for ix in similar_ix:
#         if ix == doc_id:
#             continue


def listToString(s):
    # print(len(s))
    # initialize an empty string
    result = ''
    e = 0
    for element in s:
        # print()
        result += str(element)+','
        # print(element)
        e = e + 1
    # print("============================")
    # print(e)

    return result
