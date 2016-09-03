# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 10:49:43 2016

@author: Cynanthia
"""

#%%
from processEEG.classifyFeature import train_classifier, classify_data
import numpy as np
import pickle
import csv
from sklearn import cross_validation
from sklearn import metrics

#%%
# Dataset 1
if 'features' not in globals():
    features = pickle.load(open('../data/dataset1/20160422/common/features/' +
                                'fft_all.pkl', 'rb'))

clsLabels_one = np.empty(5)
clsLabels_one.fill(1)
clsLabels_two = np.empty(5)
clsLabels_two.fill(2)
clsLabels_three = np.empty(5)
clsLabels_three.fill(3)
clsLabels = np.concatenate((clsLabels_one, clsLabels_two, clsLabels_three))

X = []
y = np.tile(clsLabels, 4)

for subj in range(1, 5):
    for frq in ['8Hz', '14Hz', '28Hz']:
        for trial in range(1, 6):
            feat = []
            for ch in range(0, 4):
                ft = features['s' + str(subj)][frq]['T' + str(trial)][ch][1][1]

                feat.append(ft)

            X.append(feat)

X = np.array(X)

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.3, random_state=14)

del clsLabels, clsLabels_one, clsLabels_two, clsLabels_three, subj, frq
del trial, feat, ft, ch

#%%
clf = train_classifier(X_train, y_train, kernel='linear')
scores = cross_validation.cross_val_score(clf, X, y, cv=3)
predicted = cross_validation.cross_val_predict(clf, X, y, cv=3)
scr = metrics.accuracy_score(y, predicted)

#%%
with open('../data/dataset1/20160422/common/features/features_all_lin.csv', 'r') as csin:

    csvr = csv.reader(csin)
        
    allrows = []
    ln = next(csvr)
    ln.append('Label Target')
    ln.append('Hasil Klasifikasi SVM')
    allrows.append(ln)

    for i in range(0, len(y)):
        try:
            ln = next(csvr)
        except StopIteration:
            break
        ln.append(y[i])
        ln.append(predicted[i])
        allrows.append(ln)

#%%
with open('../data/dataset1/20160422/common/features/features_all_lin.csv', 'w',
          newline='') as cso:
    csvw = csv.writer(cso, dialect='excel')        

    csvw.writerows(allrows)

#%%
pickle.dump((clf, scr, scores, predicted),
            open('../data/dataset1/20160422/common/classifier/svm_classifier_lin.pkl',
                 'wb'))
pickle.dump((X_train, y_train, X_test, y_test),
            open('../data/dataset1/20160422/common/classifier/traintestdata_lin.pkl',
                 'wb'))
