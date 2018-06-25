import pymysql.cursors
import csv
import json

from datetime import date, datetime
import dateutil.parser

# JSON serializer for objects not serializable by default json code
def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='azure_person_db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def get_data(start_time, end_time):
    ### Obtain data from SQL database ###
    #
    #with connection.cursor() as cursor:
    #    sql = "SELECT `id`, `person_first_id`, `person_first_similarity`, `person_second_id`, \
    #           `person_second_similarity`, `face_rectangle`, `right_person_id`, `monitor_time`, \
    #           `img_path` FROM `azure_person_identity_checkout` WHERE `checkout_status` != 0 AND `monitor_time` \
    #           BETWEEN %s AND %s ORDER BY `monitor_time`"
    #    cursor.execute(sql, (start_time, end_time))
    #    datas = cursor.fetchall()

    ### Data pre-processing ###
    # This is used to counter a name difference
    #
    #for data in datas:
    #    data['final_id'] = data['right_person_id']

    ### Use to save data to JSON ###
    #
    #with open('data/azure_face_recognition_result_data.json', 'w') as f:
    #    for obj in datas:
    #        json.dump(obj, f, default=json_serial)
    #        f.write('\n')

    ### Load demo data from local JSON file ###

    datas = []
    start_time = dateutil.parser.parse(start_time)
    end_time = dateutil.parser.parse(end_time)

    with open('data/azure_face_recognition_result_data.json') as f:
        for line in f:
            this_data = json.loads(line)
            if start_time < dateutil.parser.parse(this_data['monitor_time']) < end_time:
                datas.append(this_data)

    return datas


def get_face_count(group_similarity_src):
    with open(group_similarity_src, 'r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        input_list = list(csv.reader(csvfile))

    index_array = input_list.pop(0)
    index_array.pop(0)   # pop the 0th empty field

    face_count = []
    for face_id in index_array:
        face_count.append(int(face_id))
    face_count.append(0)
    face_count = sorted(face_count)
    print ('face_count', face_count)
    return face_count
