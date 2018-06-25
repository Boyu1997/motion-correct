import random
import numpy as np

def convert_to_vector(matched_face_table, unmatched_face_table, unmatched_validate_table, unmatched_face_objects):

    # data processing
    unmatched_face_dict = dict()
    for key, _ in enumerate(unmatched_validate_table[0]):
        unmatched_face_dict[key] = []

    for face, validate, face_object in zip(unmatched_face_table, unmatched_validate_table, unmatched_face_objects):
        have_key = False
        for key, entry in enumerate(validate):
            if entry is 1:
                unmatched_face_dict[key].append([face, face_object])
                have_key = True
                break
        if have_key is False:
            unmatched_face_dict.setdefault(999, []).append([face, face_object])

    '''
    total_count = 0
    for key, value in sorted(unmatched_face_dict.items(), key=lambda x: x[0]):
        total_count += len(value)
        print (key, len(value))
    print ("face total count", total_count)
    '''

    unmatched_face_table = []
    unmatched_validate_table = []
    unmatched_face_objects = []

    for key, values in sorted(unmatched_face_dict.items(), key=lambda x: x[0]):
        if key is not 999:

            for value in values:
                unmatched_face_table.append(value[0])
                unmatched_face_objects.append(value[1])
            validate_set = [0 for _ in range(len(unmatched_face_dict))]
            validate_set[key] = 1
            for _ in range(len(values)):
                unmatched_validate_table.append(validate_set)

    # random shuffle
    list_set = list(zip(unmatched_face_table, unmatched_validate_table, unmatched_face_objects))
    random.shuffle(list_set)
    unmatched_face_table, unmatched_validate_table, unmatched_face_objects = zip(*list_set)


    matched_face_table = np.array(matched_face_table)
    unmatched_face_table = np.array(unmatched_face_table).astype('float32')
    unmatched_validate_table = np.array(unmatched_validate_table).astype('float32')

    return unmatched_face_table, unmatched_validate_table, unmatched_face_objects
