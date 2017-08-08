# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

import numpy as np
import math

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data, test_classifier

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
#all features raw
# features_list = ['poi', 'salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 'exercised_stock_options', 'long_term_incentive', 'restricted_stock', 'director_fees', 'to_messages', 'from_poi_to_this_person', 'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi']

#top given features Decision Tree
#features_list = ['poi', 'expenses', 'exercised_stock_options', 'restricted_stock', 'total_payments', 'bonus', 'shared_receipt_with_poi', 'deferred_income', 'from_messages']

#top given features Random Forest
# features_list = ['poi', 'exercised_stock_options', 'bonus','deferred_income', 'long_term_incentive', 'restricted_stock', 'total_payments', 'salary', 'total_stock_value']

# final selection
features_list = ['poi', 'expenses', 'exercised_stock_options', 'restricted_stock', 'total_payments', 'bonus', 'deferred_income']


### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "rb") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers (as ≠ not individuals) and LOCKHART (as all his values =  NaN)
outliers = ['TOTAL', 'THE TRAVEL AGENCY IN THE PARK', 'LOCKHART EUGENE E']
for outlier in outliers:
    data_dict.pop(outlier, 0)

print "final number of employees is now", (len(data_dict))


### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.

for employee, features in data_dict.iteritems(): # P 3.x: items()
    if features['total_stock_value'] == "NaN" or features['salary'] == "NaN":
        features['ratio_tsv_salary'] = "NaN"
    else:
        features['ratio_tsv_salary'] = float(features['total_stock_value']) / float(features['salary'])

    all_messages = float(features['to_messages']) + float(features['from_messages'])
    all_poi_messages = float(features['from_poi_to_this_person']) + \
    float(features['from_this_person_to_poi']) + float(features['shared_receipt_with_poi'])
    poi_messages_ratio = all_poi_messages / all_messages

    if math.isnan(poi_messages_ratio):
        features['poi_messages_ratio'] = "NaN"
    else:
        features['poi_messages_ratio'] =  poi_messages_ratio

## add new features
# commented first feature out as it detoriates the model
#features_list.append('ratio_tsv_salary')
features_list.append('poi_messages_ratio')

my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

# removing poi for feature selection
features_list_wo_pio = list(features_list)
features_list_wo_pio.remove('poi')

for i in range(len(features_list_wo_pio)):
    print "feature no.",i, features_list_wo_pio[i]

print "final number of features", len(features_list_wo_pio)
print "all features without pio", features_list_wo_pio



### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

### Scaling and Selecting Features
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest

scaler = MinMaxScaler()
features = scaler.fit_transform(features)

k_best = SelectKBest(k="all").fit(features, labels)
print "k best", sorted(k_best.scores_, reverse=True)
print "Features sorted by score:", [features_list_wo_pio[i] for i in np.argsort(k_best.scores_)[::-1]]

### PCA not used
# from sklearn.decomposition import PCA
# # 2 best components explain .9995 of the variance
# pca = PCA(n_components=2).fit(features)
# print "pca explained"
# print pca.explained_variance_ratio_


### Classifiers ###
### GAUSSIAN
from sklearn.naive_bayes import GaussianNB
clfGNB = GaussianNB().fit(features, labels)

### SVM
from sklearn import svm
clfSVM = svm.SVC(kernel = "rbf", C = 10, gamma = 1).fit(features, labels)

### Decision Tree
from sklearn import tree
clfDT = tree.DecisionTreeClassifier(min_samples_leaf = 1, max_features = 4, min_samples_split = 5, max_depth = None, criterion="gini").fit(features, labels)

#clfDT = tree.DecisionTreeClassifier().fit(features, labels)

importances_DT = clfDT.feature_importances_
indices = np.argsort(importances_DT)[::-1]
for f in range(features.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances_DT[indices[f]]))

### random forest
from sklearn.ensemble import RandomForestClassifier
clfRF = RandomForestClassifier(bootstrap = True, min_samples_leaf = 1, min_samples_split = 6, criterion = 'gini', max_features = 3, max_depth = 5).fit(features, labels)

#clfRF = RandomForestClassifier().fit(features, labels)

importances_RF = clfRF.feature_importances_
std = np.std([tree.feature_importances_ for tree in clfRF.estimators_],
             axis=0)
indices = np.argsort(importances_RF)[::-1]

# Print the feature ranking
print("Feature ranking RandomForest:")

for f in range(features.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances_RF[indices[f]]))


### added XGBoost after writing report – out of curiosity
from xgboost import XGBClassifier
from xgboost import plot_importance
from matplotlib import pyplot

clfXGB = XGBClassifier().fit(features, labels)

# plot feature importance
# plot_importance(clfXGB)
# pyplot.show()

importances_XGB = clfXGB.feature_importances_
indices = np.argsort(importances_XGB)[::-1]

print "XGB ranking"
for f in range(features.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances_XGB[indices[f]]))

### KMeans
from sklearn.cluster import KMeans
clfKmeans = KMeans(n_clusters=2).fit(data)


### Task 5: Tune your classifier to achieve better than .3 precision and recall
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html
from sklearn.model_selection import GridSearchCV

#tunig SVM
Cs = [0.001, 0.01, 0.1, 1, 10]
gammas = [0.001, 0.01, 0.1, 1]
param_grid_SVM = {'C': Cs, 'gamma' : gammas}
grid_search_SVM = GridSearchCV(clfSVM, param_grid_SVM, scoring="f1")
grid_search_SVM.fit(features, labels)
print grid_search_SVM.best_params_

#tunig DT
param_grid_DT = {"max_depth": [1, 3, 4, 5, None],
              "max_features": [ 2, 3, 4, 5, 6],
              "min_samples_split": [2, 3, 4, 5, 6],
              "min_samples_leaf": [1, 2, 3, 4, 5, 6],
              #"min_impurity_split": [1e-6, 1e-7, 1e-8],
              "criterion": ["gini", "entropy"]}


param_grid_DT = GridSearchCV(clfRF, param_grid = param_grid_DT, scoring="f1")
param_grid_DT.fit(features, labels)
print param_grid_DT.best_params_


# using a full grid over all parameters takes longer to run
# tunig RF
param_grid_RF = {"max_depth": [2, 3, 4, 5, 6, None],
              "max_features": [2, 3, 4],
              "min_samples_split": [2, 4, 6],
              "min_samples_leaf": [1, 2, 3],
              "bootstrap": [True, False],
              "criterion": ["gini", "entropy"]}
#
grid_search_RF = GridSearchCV(clfRF, param_grid = param_grid_RF, scoring="f1")
grid_search_RF.fit(features, labels)
print grid_search_RF.best_params_


#tuning Gaussian not possible
print clfGNB.get_params().keys()

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.


print "Gaussian"
test_classifier(clfGNB, my_dataset, features_list)
dump_classifier_and_data(clfGNB, my_dataset, features_list)

print "XBG"
test_classifier(clfXGB, my_dataset, features_list)
dump_classifier_and_data(clfXGB, my_dataset, features_list)

print "Random Forest"
test_classifier(clfRF, my_dataset, features_list)
dump_classifier_and_data(clfRF, my_dataset, features_list)

print "SVM"
test_classifier(clfSVM, my_dataset, features_list)
dump_classifier_and_data(clfSVM, my_dataset, features_list)

print "KMeans"
test_classifier(clfKmeans, my_dataset, features_list)
dump_classifier_and_data(clfKmeans, my_dataset, features_list)

print "Final Classifier: DecisionTree"
test_classifier(clfDT, my_dataset, features_list)
dump_classifier_and_data(clfDT, my_dataset, features_list)
