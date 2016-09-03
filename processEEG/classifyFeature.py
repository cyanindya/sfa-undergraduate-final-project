# -*- coding: utf-8 -*-
"""
The module containing the function for feature classification
using Support Vector Machine (SVM).
"""

# Imports necessary modules and defines functions for later
from sklearn import svm


def train_classifier(trainData, classLabels, kernel='linear', C=1):

    classifier = svm.SVC(kernel=kernel, C=C)
    classifier.fit(trainData, classLabels)

    return classifier


def classify_data(testData, classifier):

    result = classifier.predict(testData)

    return result
