# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 12:47:39 2016

@author: Cynanthia
"""

from sklearn import svm

# Defines SVC instance we'll use to classify data
cls = svm.SVC()

# Defines the training data (X) and the desired output (y).
# Because each input can be of any dimension, they have to be
# in separate lists.
trainData = [[0], [1], [2], [3], [4], [5]]
labels = [0, 0, 1, 1, 2, 2]

# Defines testing data. Like training data, each input is separated
# in lists.
testData = [[3], [2], [3.5], [4]]

# Trains the classifier.
cls.fit(trainData, labels)

# Predicts the output of testing data
out = cls.predict(testData)
