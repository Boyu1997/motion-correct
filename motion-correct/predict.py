import numpy as np

from parameter import *
from test import find_rate

global list_to_face_dict

def make_prediction(model, unmatched_face_table, unmatched_face_objects):
    predictions = model.predict_proba(unmatched_face_table)

    predicted_face_objects = []
    for prediction, face_table, face_object in zip(predictions, unmatched_face_table, unmatched_face_objects):

        prediction = prediction.tolist()
        this_face_index = prediction.index(max(prediction))
        face_object['result_id'] = list_to_face_dict[this_face_index]
        face_object['update_code'] = 'cnn-1'
        predicted_face_objects.append(face_object)

    find_rate(unmatched_face_objects, 'result_id')

    return unmatched_face_objects
