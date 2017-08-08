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
features_list = ['poi','salary', 'total_stock_value', 'bonus']

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "rb") as data_file:
    data_dict = pickle.load(data_file)

print(data_dict.len)

sys.exit("enough!")

### Task 2: Remove outliers (as ≠ not individuals) and LOCKHART (as all his values =  NaN)
outliers = ['TOTAL', 'THE TRAVEL AGENCY IN THE PARK', 'LOCKHART EUGENE E']
for outlier in outliers:
    data_dict.pop(outlier, 0)

### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
# for name in data_dict:
#     # Add news ratios as features total.
#     try:
#         data_dict[name]["ratio_tsv_salary"] = float(data_dict[name]["total_stock_value"])/ float(data_dict[name]["bonus"])
#     except (data_dict[name]['total_stock_value'] == 0 , data_dict[name]['bonus'] == 0):
#         pass

for employee, features in data_dict.items(): # P 2.7: iteritems()
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
features_list.append('ratio_tsv_salary')
features_list.append('poi_messages_ratio')

my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

from sklearn.decomposition import PCA
pca = PCA(n_components=None).fit(features)

print("pca explained")
print(pca.explained_variance_ratio_)

# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# try:
#     plt.plot(ages, reg.predict(ages), color = "blue")
# except NameError:
#     pass


# for obs in range(len(features)):
#     plt.scatter(features[obs][1], features[obs][5])
    # if features[obs][4] > 10:
    #     print(features[obs][4]


#plt.plot(np.array(features[:,0]),np.array(features[:,1]))

# for k in data_dict:
#     for j in data_dict[k]:
#         print(data_dict["salary"][j]


# for k in data_dict:
#     print(data_dict[k]["bonus"]

###GAUSSIAN
from sklearn.naive_bayes import GaussianNB
clfGAU = GaussianNB().fit(features, labels)
print("Gaussian cf score is %f " % clfGAU.score(features, labels))

###SVM
from sklearn import svm
clfSVM = svm.SVC(kernel = "rbf", C = 0.001, gamma = 0.001).fit(features, labels)
print("classic SVM score is %f " % clfSVM.score(features, labels))
# predSVM = clfSVM.fit(features, labels)
#print("classic accuracy_score score is %f " % accuracy_score(labels, predSVM)

###Decision Tree
from sklearn import tree
clfDT = tree.DecisionTreeClassifier(min_samples_split=50).fit(features, labels)
print("decision tree score % f" % clfDT.score(features,labels))

print("features_list", features_list)
print('most important features DT', clfDT.feature_importances_)

### random forest
from sklearn.ensemble import RandomForestClassifier
clfRF = RandomForestClassifier(bootstrap = True, min_samples_leaf = 10, min_samples_split = 3, criterion = 'gini', max_features = 2, max_depth = 3).fit(features, labels)
print("random forest score %f" % clfRF.score(features,labels))
print('most important features RF', clfRF.feature_importances_)

###K-Clusters
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

kmeans = KMeans(n_clusters=2).fit(data)
pred = kmeans.labels_


allExStOptions = []
for person in data_dict:
    val = data_dict[person]["exercised_stock_options"]
    if val == 'NaN':
        continue
    allExStOptions.append(float(val))

# print(max(allExStOptions)
# print(min(allExStOptions)

allSalaries = []
for person in data_dict:
    val = data_dict[person]["salary"]
    if val == 'NaN':
        continue
    allSalaries.append(float(val))

# print(max(allSalaries)
# print(min(allSalaries)

someSalary = [min(allSalaries), 200000, max(allSalaries)]
someExStOptions = [min(allExStOptions), 1000000, max(allExStOptions)]

print(someSalary)
print(someExStOptions)

allSalaries = np.array([[e] for e in allSalaries])
someExStOptions = np.array([[e] for e in someExStOptions])


scaler_salary = MinMaxScaler()
scaler_stok = MinMaxScaler()

rescaled_salary = scaler_salary.fit_transform(someSalary)
rescaled_stock = scaler_salary.fit_transform(someExStOptions)

print(rescaled_salary)
print("")
print(rescaled_stock)


### trying some regression here

# from sklearn.linear_model import LinearRegression
#
# reg = LinearRegression()
# reg.fit(features, labels)
#
# print(reg.coef_
# print("now intercept"
# print(reg.intercept_
# print("now score r2"
# print(reg.score(features, labels)
#
# try:
#     plt.plot(features, reg.predict(features), color="red")
# except NameError:
#     pass

#plt.show()
### end regression

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
param_grid = {'C': Cs, 'gamma' : gammas}
grid_search = GridSearchCV(svm.SVC(kernel='rbf'), param_grid)
grid_search.fit(features, labels)
print(grid_search.best_params_)

#tuning Random forest
from time import time
from scipy.stats import randint as sp_randint
from sklearn.model_selection import RandomizedSearchCV


### Utility function to report best scores
def report(results, n_top=3):
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                  results['mean_test_score'][candidate],
                  results['std_test_score'][candidate]))
            print("Parameters: {0}".format(results['params'][candidate]))
            print("")


# specify parameters and distributions to sample from
param_dist = {"max_depth": [3, None],
              "max_features": sp_randint(1, 4),
              "min_samples_split": sp_randint(2, 11),
              "min_samples_leaf": sp_randint(2, 11),
              "bootstrap": [True, False],
              "criterion": ["gini", "entropy"]}

# run randomized search
n_iter_search = 10
random_search = RandomizedSearchCV(clfRF, param_distributions=param_dist,
                                   n_iter=n_iter_search)

start = time()
random_search.fit(features, labels)
print("RandomizedSearchCV took %.2f seconds for %d candidates"
      " parameter settings." % ((time() - start), n_iter_search))
report(random_search.cv_results_)

# use a full grid over all parameters
param_grid_2 = {"max_depth": [3, None],
              "max_features": [1, 2, 4],
              "min_samples_split": [2, 3, 10],
              "min_samples_leaf": [1, 3, 10],
              "bootstrap": [True, False],
              "criterion": ["gini", "entropy"]}

# run grid search
grid_search = GridSearchCV(clfRF, param_grid = param_grid_2)
start = time()
grid_search.fit(features, labels)

print("GridSearchCV took %.2f seconds for %d candidate parameter settings."
      % (time() - start, len(grid_search.cv_results_['params'])))
report(grid_search.cv_results_)
### end tuning for RF

#tuning Gaussian



# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.


print("final Gaussian")
test_classifier(clfGAU, my_dataset, features_list)
dump_classifier_and_data(clfGAU, my_dataset, features_list)

print("final RF")
test_classifier(clfRF, my_dataset, features_list)
dump_classifier_and_data(clfRF, my_dataset, features_list)

print("final SVM")
test_classifier(clfSVM, my_dataset, features_list)
dump_classifier_and_data(clfRF, my_dataset, features_list)
