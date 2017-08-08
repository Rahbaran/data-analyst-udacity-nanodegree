**Machine Learning Final Project**

_Summarize for us the goal of this project and how machine learning is useful in trying to accomplish it. As part of your answer, give some background on the dataset and how it can be used to answer the project question. Were there any outliers in the data when you got it, and how did you handle those?  [relevant rubric items: &quot;data exploration&quot;, &quot;outlier investigation&quot;]_

**Intro:**

The [Enron scandal](https://en.wikipedia.org/wiki/Enron_scandal) around 2000 was so severe that even most Germans (where I live) have heard about it. Many executives at Enron were indicted for being heavily interwoven in the scandal due to hiding debt and/or manipulating financial balances.

The dataset at hand is a subset of Enron employees with some of them being part of the scandal. The goal is to identify these suspects. There are:

- a total of **146** employees (i.e., rows/observations) in the data set
- with 21 features (incl. POI)
- the feature **poi** (Person of Interest) is a Boolean and classifies employees if further investigation against fraud is necessary or not.
- the other 20 features are of financial (e.g. salary) or communicational (e.g emails sent from\_this\_person\_to\_poi) nature
- there are 18 &#39;POI&#39;, and 128 &#39;non-POI&#39;
- 20 out of 21 features contain missing values

Here&#39;s the full list from Udacity&#39;s Project Details:

- **financial features** : [&#39;salary&#39;, &#39;deferral\_payments&#39;, &#39;total\_payments&#39;, &#39;loan\_advances&#39;, &#39;bonus&#39;, &#39;restricted\_stock\_deferred&#39;, &#39;deferred\_income&#39;, &#39;total\_stock\_value&#39;, &#39;expenses&#39;, &#39;exercised\_stock\_options&#39;, &#39;other&#39;, &#39;long\_term\_incentive&#39;, &#39;restricted\_stock&#39;, &#39;director\_fees&#39;] (all units are in US dollars)

- **email features** : [&#39;to\_messages&#39;, &#39;email\_address&#39;, &#39;from\_poi\_to\_this\_person&#39;, &#39;from\_messages&#39;, &#39;from\_this\_person\_to\_poi&#39;, &#39;shared\_receipt\_with\_poi&#39;] (units are generally number of emails messages; notable exception is &#39;email\_address&#39;, which is a text string)

**POI label** : [&#39;poi&#39;] (boolean, represented as integer)

**Outliers:**

Via a brief exploratory data analysis and a double check with the file **enron61702insiderpay.pdf** (given by Udacity), the following outliers were detected:

- TOTAL
- THE TRAVEL AGENCY IN THE PARK

Both are aggregated observations and thus no employees. Besides,

- LOCKHART, EUGENE E

can be considered as an outlier was removed as all his values were NaN.

_What features did you end up using in your POI identifier, and what selection process did you use to pick them? Did you have to do any scaling? Why or why not? As part of the assignment, you should attempt to engineer your own feature that does not come ready-made in the dataset -- explain what feature you tried to make, and the rationale behind it. (You do not necessarily have to use it in the final analysis, only engineer and test it.) In your feature selection step, if you used an algorithm like a decision tree, please also give the feature importances of the features that you use, and if you used an automated feature selection function like SelectKBest, please report the feature scores and reasons for your choice of parameter values.  [relevant rubric items: &quot;create new features&quot;, &quot;intelligently select features&quot;, &quot;properly scale features&quot;]_

**New features**

I experimented with two new features, which are ratios (a financial and a communicational one):

- ratio\_tsv\_salary: setting the total stocks value to the annual salary might give some insights if the stock bonus is disproportionate to the base salary.
- poi\_messages\_ratio: setting all poi-related messages to the sum of all messages might give some insights if an employee had continuous contact with POIs.

**Selection Process**

I ranked all the features available (incl. AND excl. the two I created, except the feature email) via select k-best the method _feature\_importances\__ for Decision Trees and Random Forest. These were the TOP-10 ranked by select kBest:

| Feature | Score |
| --- | --- |
| exercised\_stock\_options | 24.815079733218194 |
| total\_stock\_value | 24.182898678566872 |
| bonus | 20.792252047181538 |
| salary | 18.289684043404513 |
| deferred\_income | 11.458476579280697 |
| long\_term\_incentive | 9.9221860131898385 |
| restricted\_stock | 9.212810621977086 |
| total\_payments | 8.7727777300916809 |
| shared\_receipt\_with\_poi | 8.5894207316823774 |
| loan\_advances | 7.1840556582887247 |

The 10th spot, &#39;loan\_advances&#39;, was ditched, as it only had 3 (!) non NaN-values. Besides, its score is 15% lower than the spot above, which seemed a good arbitrary cut. So, I chose to work just with the TOP 9. Except of _shared\_receipt\_with\_poi_, all features were financial.

Eventually, _shared\_receipt\_with\_poi_ was substituted with my own ratio feature _poi\_messages\_ratio_. The same goes for _salary_ and _total\_stock\_value_ features, which are part of my financial ratio. However, my financial ratio wasn&#39;t successful at all, so I removed it and added salary and total\_stock\_value again to the feature list.

**Scaling**

Scaling was not necessary for all tested algorithms (e.g. Random Forest and Decision Tree). However, it was still used as the scales for financial features dwarfed the communicational ones. If no scaling occurred, the financial features would get more weight.

_What algorithm did you end up using? What other one(s) did you try? How did model performance differ between algorithms?  [relevant rubric item: &quot;pick an algorithm&quot;]_

I tried the following algorithms, with the following final results:

- GaussianNB: Accuracy: 0.84100        Precision: 0.38355        Recall: 0.31700
- Decision Tree:  Accuracy: 0.81000        Precision: 0.25686        Recall: 0.22450
- *Kmeans: Accuracy: 0.85593        Precision: 0.31663        Recall: 0.06950

*(This was out of curiosity, as Kmeans is primarily designed for clustering)

- RandomForest:Accuracy: 0.85407        Precision: 0.39936        Recall: 0.18750
- SVM: &quot;Got a divide by zero when trying out&quot;, I assume no employee got labeled as a POI

These are the results _without_ my own feature _poi\_messages\_ratio_, but just taking the best ranked features from above:

- GaussianNB: Accuracy: 0.84067        Precision: 0.37611        Recall: 0.31400
- Decision Tree: Accuracy: 0.80920        Precision: 0.28535        Recall: 0.28150
-  *Kmeans: Accuracy: 0.84807        Precision: 0.32963        Recall: 0.10450

*(This was out of curiosity, as Kmeans is primarily designed for clustering)

- RandomForest:Accuracy: 0.85620        Precision: 0.37025        Recall: 0.15050
- SVM: &quot;Got a divide by zero when trying out&quot;, I assume no employee got labeled as a POI

So, in the end, my feature selection didn&#39;t work out for the tree algorithm but rather made the **GaussianN** B classifier to pass the test.

_What does it mean to tune the parameters of an algorithm, and what can happen if you don&#39;t do this well?  How did you tune the parameters of your particular algorithm? What parameters did you tune? (Some algorithms do not have parameters that you need to tune -- if this is the case for the one you picked, identify and briefly explain how you would have done it for the model that was not your final choice or a different model that does utilize parameter tuning, e.g. a decision tree classifier).  [relevant rubric items: &quot;discuss parameter tuning&quot;, &quot;tune the algorithm&quot;]_

The goal of parameter tuning is to improve the performance of the chosen algorithm. Hyperparameters are parameters whose values are set **before** the beginning of the learning. The optimization of hyperparameters can be done manually or with sklearn&#39;s GridSearchCV. If it&#39;s not done well, the performance of the chosen classifier might be under expectations in practice.

Although, I eventually used GaussianNB, I experimented with tuning the other classifiers to get some experience. The hyperparameters for two classifiers are given here as an example:

- Random Forest
  - criterion= There the options &#39;gini&#39; and &#39;entropy&#39; for measuring how to split
  - bootstrap = Whether bootstrap samples are used when building trees.
  - max\_depth = The maximum depth of the tree. If too deep, you might overfit.
  - min\_samples\_split = The minimum number of samples required to split an internal node. If set too low, you might overfit.

- SVM
  - C: low value is for smooth decision boundary, high value complex boundary (caveat: overfitting),
  - Gamma: if gamma is too large you might also end up overfitting

_What is validation, and what&#39;s a classic mistake you can make if you do it wrong? How did you validate your analysis? [relevant rubric item: &quot;validation strategy&quot;]_

Validation tests the performance of your model. A classic mistake is to forego splitting the data into a training and testing set and thus using the whole dataset for training your model. Consequently, the model will be over fitted and perform poorly on new data. Therefore, I split the data into a train (70% of the data) and a test set (30% of the data).

Furthermore, StratifiedShuffleSplit from tester.py was used. As we are dealing with a small and imbalanced dataset in this project, working with smaller datasets is hard and in order to make validation models robust, we often go with cross-validation. This cross-validation method splits data in train/test sets by shuffling randomized folds. Per defaults, it reshuffles and splits the data 10 times. Moreover, when dealing with small imbalanced datasets, it is possible that some folds contain almost none (or even none!) instances of the minority class. The idea behind stratification is to keep the percentage of the target class as close as possible to the one we have in the complete dataset.



_Give at least 2 evaluation metrics and your average performance for each of them. Explain an interpretation of your metrics that says something human-understandable about your algorithm&#39;s performance. [relevant rubric item: &quot;usage of evaluation metrics&quot;]_

The simplest evaluation metric is accuracy, which divides the correctly labeled observations by all observations. However, a high score might be due to the [accuracy paradox](https://en.wikipedia.org/wiki/Accuracy_paradox). This happens when one class is very rare in the population. For this dataset, where there are only few POIs this might happen, so the recall and precision rates might be more appropriate.

- Precision:  true positive / (true positive + false **positive** )
- Recall: true positive / (true positive + false **negative** )

A good precision means that whenever a POI gets flagged in the test set, we know with a lot of confidence that it&#39;s very likely to be a real POI and not a false alarm. On the other hand, a good recall means that, nearly every time a POI shows up in the test set, we are able to identify the person. We might have some false positives here, but pulling the trigger to early in this case just means further investigations, which is not equal to being directly indicted. So, recall might be more important the precision.

### **References**

- [**http://napitupulu-jon.appspot.com/**](http://napitupulu-jon.appspot.com/) **helped a lot to digest the whole course**
- [http://scikit-learn.org/stable/documentation.html](http://scikit-learn.org/stable/documentation.html) lovely documentation to dig deeper
- [https://github.com/keymanesh/Udacity--Intro-to-Data-Science/blob/master/Code/poi\_id.py](https://github.com/keymanesh/Udacity--Intro-to-Data-Science/blob/master/Code/poi_id.py) /helped me to understand how to use gridsearch
- Udacity reviewers
