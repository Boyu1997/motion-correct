from parameter import *
from test import find_rate
from data import get_data, get_face_count
from build import build_automaton
from match import find_match
from convert import convert_to_vector
from network import conv_net
from predict import make_prediction

global results

# get face count of the group
face_count = get_face_count(group_similarity_src)

# select from database
print ("\n\n\n############ Training Session ############")

datas = []
for cnn_build_time_range in cnn_build_time_range_set:
    start_time = cnn_build_time_range[0]
    end_time = cnn_build_time_range[1]
    this_datas = get_data(start_time, end_time)
    datas = datas + this_datas
results.clear()

# print import data result for banchmark
print ("\n\n\n------ Original Result ------")
find_rate(datas, 'person_first_id')

# build automaton
root_c = build_automaton(datas)

# apply decision model
matched_face_table, unmatched_face_table, unmatched_validate_table, unmatched_face_objects = find_match(root_c.next, face_count)

# convert data to vector for neuron network
unmatched_face_table, unmatched_validate_table, unmatched_face_objects = convert_to_vector(matched_face_table, unmatched_face_table, unmatched_validate_table, unmatched_face_objects)

# separate training and test data
division = int(unmatched_face_table.shape[0] * 0.7)
X = unmatched_face_table[:division]
y = unmatched_validate_table[:division]
X_test = unmatched_face_table[division:]
y_test = unmatched_validate_table[division:]

# build cnn, and save the model
model = conv_net(X, y, X_test, y_test)

# use the model to make prediction on the construct session
print ("\n\n\n------ Unmatched Face (Corrected by CNN) ------")
cnn_result = make_prediction(model, unmatched_face_table, unmatched_face_objects)

print ("\n\n\n------ Overall Result (Corrected by CNN) ------")
all_result = list(results) + list(cnn_result)
find_rate(all_result, 'result_id')


print (predict_time_range_set)
for predict_time_range in predict_time_range_set:
    print (predict_time_range)

    # get data from different session for testing
    print ("\n\n\n############ Indipendent Testing Session ############")
    start_time = predict_time_range[0]
    end_time = predict_time_range[1]
    datas = get_data(start_time, end_time)
    results.clear()

    # print import data result for banchmark
    print ("\n\n\n------ Original Result ------")
    find_rate(datas, 'person_first_id')

    # build automaton
    root_c = build_automaton(datas)

    # apply decision model
    matched_face_table, unmatched_face_table, unmatched_validate_table, unmatched_face_objects = find_match(root_c.next, face_count)

    # convert data to vector for neuron network
    unmatched_face_table, unmatched_validate_table, unmatched_face_objects = convert_to_vector(matched_face_table, unmatched_face_table, unmatched_validate_table, unmatched_face_objects)

    # evaluate the model using data of the indipendent test session
    score = model.evaluate(unmatched_face_table, unmatched_validate_table)
    print("\nCross Session Accuracy: ", score[-1])

    # use the model to make prediction on the indipendent test session
    print ("\n\n\n------ Unmatched Face ------")
    find_rate(unmatched_face_objects, 'person_first_id')

    print ("\n\n\n------ Unmatched Face (Corrected by CNN) ------")
    cnn_result = make_prediction(model, unmatched_face_table, unmatched_face_objects)

    print ("\n\n\n------ Overall Result (Corrected by CNN) ------")
    all_result = list(results) + list(cnn_result)
    find_rate(all_result, 'result_id')
