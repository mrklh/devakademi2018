# -*- coding: utf-8 -*-

from preprocess import get_scikit_data
from sklearn.preprocessing import Imputer
import numpy as np
from sklearn import tree
import graphviz

def create_dt():
	data, cat_dct, job_dct = get_scikit_data()
	my_data = np.array(data, dtype='str')

	imp = Imputer(missing_values='NaN', strategy='median', axis=0)
	new_data = imp.fit_transform(my_data)


	X = new_data[:,:-1]
	Y = new_data[:,-1]

	clf = tree.DecisionTreeClassifier()
	clf.fit(X, Y)

	"""
	dot_data = tree.export_graphviz(clf, feature_names=['Gender', 'Age', 'Education', 'Marital', 'Job', 'Part of Day', 'Category'])
	graph = graphviz.Source(dot_data)
	graph.render("Sahibinden")
	"""

	return clf, cat_dct, job_dct