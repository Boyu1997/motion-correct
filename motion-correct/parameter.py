### Parameters for building the trusted area model ###
#
# max distance for a recognition result to be added into a model
build_dist_threshold = 200
#
# max distance for a recognition to be matched to an existed model
## the larger number is used to account for the model mean being drifted away
## by the newly added faces
## in addition, we want to make the model harder to build but easier to match
## on, this should generate better result (unverified)
validate_dist_threshold = 250


### Parameters for decideding if a model is valid ###
#
# the max % of NaN value allowed
## when the face a model is repersenting is not found in a frame, an NaN will
## be added into the model
## a higher NaN rate repersent the location information is unstable, which
## implies the original recognition result is not trustable given the assumption
## we made that the face location should be stable
## when the NaN rate exceed the setting here, the model will be void
nan_max_rate = 0.7
#
# the continue of NaN allowed in a model
## when the model has continuous NaN value, we will consider the face the model
## is repersenting has moved, when the continuous NaN exceed the setting here,
## the model will cut the NaN value
nan_max_continue = 5
#
# the minimum number of frames a model has to persist
## as we build a model whenever we find a face that cannot be matched to an
## existed model, we tend to build a lot of model that only repersent a moment
## not a pattern across frames
## this parameter is used to counter that by setting a lowerst limit on how many
## frames a model has to persist for it to be consider as a pattern
auto_min_continue = 5


### Global Variables ###
results = []
face_to_list_dict = dict()
list_to_face_dict = dict()


### Data loading ###
#
# similarity table is used to translate first and second similarity to
# similarity for all possible matches
# it is also used to determine how many faces the algorithm should match the
# faces to
group_similarity_src = 'data/group5.csv'
#
# the data in the time range that is used to train the neural network
cnn_build_time_range_set = [['2018-01-03 15:30:00', '2018-01-03 16:59:59'], ['2018-01-18 15:30:00', '2018-01-18 15:59:59']]
#
# the data in the time range that is used to test the neural network
predict_time_range_set = [['2018-01-09 15:30:00', '2018-01-09 15:59:59'], ['2018-01-11 15:30:00', '2018-01-11 15:59:59'],
                          ['2018-01-16 15:30:00', '2018-01-16 15:59:59'],
                          ['2018-01-25 15:30:00', '2018-01-25 15:59:59']]
