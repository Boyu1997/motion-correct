import json, ast
import numpy as np
import math
from parameter import *

cleanup_set = []

class Auto:
    def __init__(self, entry):
        self.status = 'pending'
        self.face_id = entry['person_first_id']
        self.top = []
        self.c_top = 'NA'
        self.left = []
        self.c_left = 'NA'
        self.occupy = False
        self.add_entry(entry)
        self.frames = []

    def dist_check(self, entry, threshold):
        r = ast.literal_eval(entry['face_rectangle'])
        if np.sqrt((r['top']-self.c_top)**2 + (r['left']-self.c_left)**2) < threshold:
            # within distence
            return True
        else:
            return False

    def add_entry(self, entry='NA'):
        global cleanup_set
        if entry is not 'NA':
            r = ast.literal_eval(entry['face_rectangle'])
            self.top.append(r['top'])
            self.left.append(r['left'])
            self.get_center()
            return True
        else:
            self.top.append(np.nan)
            self.left.append(np.nan)
            if self.check_validity() is True:
                return True
            else:
                #print ("add", self, "to cleanup_set")
                cleanup_set.append(self)
                return False

    def get_center(self):
        self.c_top = np.nanmean(self.top)
        self.c_left = np.nanmean(self.left)

    def check_validity(self):
        num_of_nan = 0
        for num in self.top:
            if np.isnan(num):
                num_of_nan += 1
        #print (self.top)
        #print ("check validity: auto for face", self.face_id, "nan rate:", 1-num_of_nan/len(self.top))

        '''delay rate check'''
        
        if 1-num_of_nan/len(self.top) < nan_max_rate:
            #print ("NaN rate too high, invalid")
            self.top.pop(-1)
            self.left.pop(-1)
            return False
        else:
            #print ("np.nansum is", np.nansum(self.top[-1*nan_max_continue:]), "for", self.top[-1*nan_max_continue:])
            if np.nansum(self.top[-1*nan_max_continue:]) == 0:
                #print ("continue NaN, invalid")
                return False
            else:
                #print ("valid")
                return True

    def cleanup(self):
        #print ("cleanup: auto for face", self.face_id, "start with:", self.top)

        # remove NaN at end
        while np.isnan(self.top[-1]):
            self.top.pop(-1)
            self.left.pop(-1)
            self.frames[-1].autos[self.face_id].remove(self)
            if len(self.frames[-1].autos[self.face_id]) is 0:
                del self.frames[-1].autos[self.face_id]
            self.frames.pop(-1)

        # destory short model
        if len(self.top) < auto_min_continue:
            while len(self.top) is not 0:
                self.top.pop(-1)
                self.left.pop(-1)
                self.frames[-1].autos[self.face_id].remove(self)
                if len(self.frames[-1].autos[self.face_id]) is 0:
                    del self.frames[-1].autos[self.face_id]
                self.frames.pop(-1)
        #print ("end with:", self.top)
