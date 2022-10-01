import numpy as np 
import pandas as pd 
import re
import nltk 
import pickle
# import matplotlib.pyplot as plt

data_source = "allcomments.csv"
comments = pd.read_csv(data_source)
features = comments.iloc[:, 1].values
labels = comments.iloc[:, 0].values
processed_features = []
for sentence in range(0, len(features)):
    # Remove all the special characters
    processed_feature = re.sub(r'\W', ' ', str(features[sentence]))
    # remove all single characters
    processed_feature= re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_feature)
    # Remove single characters from the start
    processed_feature = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_feature) 
    # Substituting multiple spaces with single space
    processed_feature = re.sub(r'\s+', ' ', processed_feature, flags=re.I)
    # Removing prefixed 'b'
    processed_feature = re.sub(r'^b\s+', '', processed_feature)
    # Converting to Lowercase
    processed_feature = processed_feature.lower()
    processed_features.append(processed_feature)
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer (max_features=2500,min_df=5,stop_words=stopwords.words('english'))
processed_features = vectorizer.fit_transform(processed_features).toarray()
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(processed_features, labels, test_size=0.18, random_state=4)
from sklearn.ensemble import RandomForestClassifier
model =RandomForestClassifier(random_state=0)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print(type(X_test))
tuple_objects = (model, vectorizer) 
pkl_filename = "pickle_model.pkl"
pickle.dump(tuple_objects, open(pkl_filename, 'wb'))    
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, predictions))
