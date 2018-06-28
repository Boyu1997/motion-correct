from automaton import Auto
from collection import Collection, collection_builder

def build_model(datas):

    # data pre-processing
    last_time = datas[0]['monitor_time']
    this_time_data = []
    counter = 0
    root_c = collection_builder(dict())
    c = root_c

    # build data, automaton, and collection
    for data in datas:
        if data['monitor_time'] == last_time:
            this_time_data.append(data)
        else:
            face_dict = dict()
            for face in this_time_data:
                face_dict.setdefault(face['person_first_id'], []).append(face)
            c = collection_builder(face_dict, c)
            last_time = data['monitor_time']
            this_time_data = [data]
    face_dict = dict()
    for face in this_time_data:
        face_dict.setdefault(face['person_first_id'], []).append(face)
    c = collection_builder(face_dict, c)

    return root_c
