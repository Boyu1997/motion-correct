import pandas as pd
import numpy as np

def find_rate(entries, test_field):
    true_postive = dict()
    false_postive = dict()
    false_negative = dict()
    for entry in entries:
        if entry[test_field] == entry['final_id']:
            true_postive.setdefault(entry['final_id'], 0)
            false_postive.setdefault(entry['final_id'], 0)
            false_negative.setdefault(entry['final_id'], 0)
            true_postive[entry['final_id']] += 1
        elif entry[test_field] !=  entry['final_id']:
            true_postive.setdefault(entry[test_field], 0)
            true_postive.setdefault(entry['final_id'], 0)
            false_postive.setdefault(entry[test_field], 0)
            false_postive.setdefault(entry['final_id'], 0)
            false_negative.setdefault(entry[test_field], 0)
            false_negative.setdefault(entry['final_id'], 0)
            false_postive[entry[test_field]] += 1
            false_negative[entry['final_id']] += 1
    d = {'face_id': [], 'precision': [], 'recall': [], 'true_postive': [], 'false_postive': [], 'false_negative': [], 'total_count': []}
    for face_id, face_tp in sorted(true_postive.items(), key=lambda x: x[0]):
        d['face_id'].append(face_id)
        d['precision'].append(np.divide(face_tp, (face_tp + false_postive[face_id])))
        d['recall'].append(np.divide(face_tp, (face_tp + false_negative[face_id])))
        d['true_postive'].append(face_tp)
        d['false_postive'].append(false_postive[face_id])
        d['false_negative'].append(false_negative[face_id])
        d['total_count'].append(face_tp + false_negative[face_id])
    d['face_id'].append('sum')
    d['precision'].append(np.divide(sum(true_postive.values()), (sum(true_postive.values()) + sum(false_postive.values()))))
    d['recall'].append(np.divide(sum(true_postive.values()), (sum(true_postive.values()) + sum(false_negative.values()))))
    d['true_postive'].append(sum(true_postive.values()))
    d['false_postive'].append(sum(false_postive.values()))
    d['false_negative'].append(sum(false_negative.values()))
    d['total_count'].append(sum(true_postive.values()) + sum(false_negative.values()))
    df = pd.DataFrame(d)
    df = df.set_index('face_id')

    print (df)

    overall_rate = sum(true_postive.values()) / (sum(true_postive.values()) + (sum(false_postive.values())))
    print ("Overall rate is", overall_rate)
