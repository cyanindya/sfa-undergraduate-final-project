# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 20:28:48 2016

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
if 'features' not in globals():
    features = pickle.load(open('../data/dataset2/20160422/features/' +
                                'features.pkl', 'rb'))

clsLabels_1 = np.array([7, 7, 7, 8, 8, 8, 2, 2, 2, 1, 1, 1, 1, 1, 1, 4, 4, 4,
                        3, 3, 3, 5, 5, 5, 6, 6, 6])
clsLabels_2 = np.array([7, 7, 7, 2, 2, 2, 2, 1, 1, 1, 4, 4, 4, 3, 3, 3, 3, 3,
                        3, 5, 5, 5, 5, 6, 6, 6])
clsLabels_3 = np.array([7, 7, 7, 2, 2, 2, 1, 1, 1, 4, 4, 4, 3, 3, 3, 5, 5, 5,
                        6, 6, 6])
clsLabels_4 = np.array([7, 7, 7, 2, 2, 2, 1, 1, 1, 4, 4, 4, 3, 3, 3, 5, 5, 5,
                        6, 6, 6])

X = []
y = np.concatenate((clsLabels_1, clsLabels_2, clsLabels_3,
                                clsLabels_4))

for subj in range(1, 5):
    numtrials = len(features['s' + str(subj)])
    
    for trial in range(1, numtrials + 1):
        feat = [features['s' + str(subj)]['T' + str(trial)][1][1]]

        X.append(feat)

X = np.array(X)

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.3, random_state=14)

del clsLabels_1, clsLabels_2, clsLabels_3, clsLabels_4, subj, numtrials, trial
del feat

#%%
clf = train_classifier(X_train, y_train, kernel='linear')
scores = cross_validation.cross_val_score(clf, X, y, cv=3)
predicted = cross_validation.cross_val_predict(clf, X, y, cv=3)
scr = metrics.accuracy_score(y, predicted)

#%%
with open('../data/dataset2/20160422/features/features_all_lin.csv', 'r') as csin:

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
with open('../data/dataset2/20160422/features/features_all_lin.csv', 'w',
          newline='') as cso:
    csvw = csv.writer(cso, dialect='excel')        

    csvw.writerows(allrows)

#%%
pickle.dump((clf, scr, scores, predicted),
            open('../data/dataset2/20160422/classifier/svm_classifier_lin.pkl',
                 'wb'))
pickle.dump((X_train, y_train, X_test, y_test),
            open('../data/dataset2/20160422/classifier/traintestdata_lin.pkl',
                 'wb'))
