import csv
import numpy as np

from parameter import *

def get_similarity_table():
    with open(group_similarity_src, 'r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        input_list = list(csv.reader(csvfile))

    index_array = input_list.pop(0)
    index_array.pop(0)   # pop the 0th empty field
    column_to_face_dict = dict()
    for key, face_id in enumerate(index_array):
        column_to_face_dict[key] = int(face_id)

    conversion_dict = dict()
    for conversion_array in input_list:
        this_face_id = conversion_array.pop(0)
        this_face_dict = dict()
        for key, rate in enumerate(conversion_array):
            this_face_dict[int(column_to_face_dict[key])] = float(rate)
        conversion_dict[int(this_face_id)] = this_face_dict

    return conversion_dict
