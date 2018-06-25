import json, ast
import numpy as np
import math
import copy
from automaton import Auto, cleanup_set
from parameter import *

class Collection:
    def __init__(self):
        self.last = 'NA'
        self.next = 'NA'
        self.raw = 'NA'
        self.autos = dict()

    def next_frame(self, face_dict):
        n = Collection()
        self.next = n
        n.last = self
        n.raw = copy.deepcopy(face_dict)
        return n

    def add_auto(self, auto):
        auto.frames.append(self)
        self.autos.setdefault(auto.face_id, []).append(auto)


def collection_builder(face_dict, c='NA'):
    global cleanup_set

    #print ("Start with:", len(face_dict))
    #print ("C is:", c)

    # validate automatons in the last frame using observed data in this frame
    if c is not 'NA':
        c = c.next_frame(face_dict)
        for face_id, face_autos in c.last.autos.items():
            values = face_dict.get(face_id)
            for face_auto in face_autos:
                match = False
                if values is not None:
                    for value in values:
                        if face_auto.dist_check(value, build_dist_threshold):
                            face_auto.add_entry(value)
                            c.add_auto(face_auto)
                            try:
                                face_dict[face_id].remove(value)
                            except ValueError:
                                pass
                            if len(face_dict[face_id]) is 0:
                                del face_dict[face_id]
                            match = True
                            break
                if match is False:
                    if face_auto.add_entry():
                        c.add_auto(face_auto)
        for cleanup in cleanup_set:
            cleanup.cleanup()
        while len(cleanup_set) is not 0:
            cleanup_set.pop()
    # this is the first frame, initialize
    else:
        c = Collection()

    #print ("End with:", len(face_dict))
    for face_id, face_datas in face_dict.items():
        for face_data in face_datas:
            c.add_auto(Auto(face_data))
    #print (sorted(c.autos))
    return c
