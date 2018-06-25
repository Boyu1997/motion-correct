build_dist_threshold = 200
validate_dist_threshold = 250
correct_dist_threshold = 100

nan_max_rate = 0.7
nan_max_continue = 5
auto_min_continue = 5


results = []
face_to_list_dict = dict()
list_to_face_dict = dict()

group_similarity_src = 'data/group5.csv'

cnn_build_time_range_set = [['2018-01-03 15:30:00', '2018-01-03 16:59:59'], ['2018-01-18 15:30:00', '2018-01-18 15:59:59']]
predict_time_range_set = [['2018-01-09 15:30:00', '2018-01-09 15:59:59'], ['2018-01-11 15:30:00', '2018-01-11 15:59:59'],
                          ['2018-01-16 15:30:00', '2018-01-16 15:59:59'],
                          ['2018-01-25 15:30:00', '2018-01-25 15:59:59']]
