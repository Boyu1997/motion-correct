import json, ast
import copy
import numpy as np

from parameter import *
from test import find_rate
from similarity import get_similarity_table

def find_match(c, face_count):

    global results
    global face_to_list_dict
    global list_to_face_dict

    counter = 0
    start_with = 0
    left_by_a = 0
    left_by_b = 0
    left_by_c = 0
    remain_auto_count = 0
    all_face_list = copy.deepcopy(face_count)

    for key, value in enumerate(all_face_list):
        face_to_list_dict[value] = key
        list_to_face_dict[key] = value
    print ("list_to_face_dict", list_to_face_dict)
    face_count = len(face_count)
    matched_face_table = []
    unmatched_face_table = []
    unmatched_face_final_id = []
    unmatched_correct = 0
    unmatched_validate_table = []
    unmatched_face_objects = []

    similarity_table = get_similarity_table()


    while True:
        # void data initialize
        this_results = []

        # model report processing
        for face_key, face_objects in c.raw.items():
            start_with += len(face_objects)

        # decision pre-processing
        for face_id, face_autos in c.autos.items():
            for face_auto in face_autos:
                face_auto.occupy = False


        # find all exact match
        # self precision rate = 0.9765 (6340/6492)
        # depend on seeting
        for face_id, face_autos in c.autos.items():
            if len(face_autos) is 1:
                face_auto = face_autos[0]
                selected_face = 'NA'
                selected_auto = 'NA'
                if c.raw.get(face_id) is not None:
                    for face in c.raw[face_id]:
                        if face_auto.dist_check(face, validate_dist_threshold) is True:
                            if selected_face is 'NA':
                                selected_face = face
                                selected_auto = face_auto
                            else:
                                # see multiple faces in this regin, automaton donot pass
                                selected_face = 'Duplicate'
                    if selected_face is not 'NA' and selected_face is not 'Duplicate':
                        c.raw[face_id].remove(selected_face)
                        if len(c.raw[face_id]) is 0:
                            del c.raw[face_id]
                        selected_face['result_id'] = selected_face['person_first_id']
                        selected_face['update_code'] = 'match-1'
                        this_results.append(selected_face)
                        results.append(selected_face)
                        selected_auto.occupy = True


        # if already accounted for, ignore
        # self rate 0.0202 (8/396) => 0.3409 (135/396)
        # not deep copy, the original data is altered
        '''
        for face_id, face_autos in c.autos.items():
            for face_auto in face_autos:
                if face_auto.occupy is True:
                    if c.raw.get(face_id) is not None:
                        for face in c.raw[face_id]:
                            face['update_code'] = 'b-1'
                            face['person_first_id'] = face['person_second_id']
                            face['person_first_similarity'] = face['person_second_similarity']
        '''


        # data processing
        # construct array for neural network

        matched_face_table.append([[0,0,0] for n in range(face_count)])
        for result in this_results:
            r = ast.literal_eval(result['face_rectangle'])
            matched_face_table[counter][face_to_list_dict[result['result_id']]] = [result['id'], r['top'], r['left']]

        for face_id, face_objects in c.raw.items():
            for face_object in face_objects:
                r = ast.literal_eval(face_object['face_rectangle'])
                face_object_top = r['top']
                face_object_left = r['left']

                first_similarity_array = []
                for face_id in all_face_list:
                    if face_id == face_object['person_first_id']:
                        first_similarity_array.append(face_object['person_first_similarity'])
                        person_first_id = face_object['person_first_id']
                        person_first_similarity = face_object['person_first_similarity']
                    else:
                        first_similarity_array.append(0)
                for i in range(1, len(first_similarity_array)):
                    first_similarity_array[i] = person_first_similarity * similarity_table[person_first_id][list_to_face_dict[i]]

                second_similarity_array = []
                for face_id in all_face_list:
                    if face_id == face_object['person_second_id']:
                        second_similarity_array.append(face_object['person_second_similarity'])
                        person_second_id = face_object['person_second_id']
                        person_second_similarity = face_object['person_second_similarity']
                    else:
                        second_similarity_array.append(0)
                for i in range(1, len(second_similarity_array)):
                    second_similarity_array[i] = person_second_similarity * similarity_table[person_second_id][list_to_face_dict[i]]

                face_dist_dict = dict()
                matched_id = []
                for result in this_results:
                    r = ast.literal_eval(result['face_rectangle'])
                    d = 1 - ((face_object_top-r['top'])**2 + (face_object_left-r['left'])**2)**0.5 / (2560**2 + 1440**2)**0.5
                    face_dist_dict[result['result_id']] = d
                    matched_id.append(result['result_id'])

                distence_array = []
                for face_id in all_face_list:
                    if face_id in face_dist_dict:
                        distence_array.append(face_dist_dict[face_id])
                    else:
                        distence_array.append(0)

                claimed_array = []
                for face_id in all_face_list:
                    if face_id in matched_id:
                        claimed_array.append(1)
                    else:
                        claimed_array.append(0)

                info_array = []
                for first_similarity, second_similarity, distence, claimed in zip(first_similarity_array, second_similarity_array, distence_array, claimed_array):
                    info_array.append([[first_similarity], [second_similarity], [distence], [claimed]])

                validate_array = []
                for face_id in all_face_list:
                    if face_id == face_object['final_id']:
                        validate_array.append(1)
                    else:
                        validate_array.append(0)

                # how to avoid out of indix situation??
                # more though needed here
                if face_object['final_id'] in all_face_list:
                    unmatched_face_table.append(info_array)
                    unmatched_face_final_id.append(face_to_list_dict[face_object['final_id']])
                    if face_object['person_first_id'] == face_object['final_id']:
                        unmatched_correct += 1

                    unmatched_validate_table.append(validate_array)

                    unmatched_face_objects.append(face_object)


        if c.next is 'NA':
            break
        else:
            c = c.next
            counter += 1


    matched_correct = 0
    for result in results:
        if result['result_id'] == result['final_id']:
            matched_correct += 1
    print ("Out of", len(results), "matched,", matched_correct, "are correct, correct rate is", matched_correct/len(results))
    print ("Out of", len(unmatched_face_final_id), "unmatched,", unmatched_correct, "are correct, correct rate is", unmatched_correct/len(unmatched_face_final_id))

    return matched_face_table, unmatched_face_table, unmatched_validate_table, unmatched_face_objects
