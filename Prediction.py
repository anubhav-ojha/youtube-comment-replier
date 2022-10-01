import numpy as np
import pickle
import re
import nltk
from sklearn.ensemble import RandomForestClassifier
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd


def predict():
    pkl_filename = "pickle_model.pkl"
    model, vectorize=pickle.load(open(pkl_filename, 'rb'))    
    comment_file = pd.read_csv("./comments.csv")
    flags,comments_id,comments = list(comment_file["flag"]),list(comment_file["comments_id"]),list(comment_file["comments"])   
    processed_comments = []
    # Almost copy-pasted part from line 15 to 28. Removing emojis and other useless information
    for sentence in range(0, len(comments)):
        if(flags[sentence]):
            # Remove all the special characters
            being_processed = re.sub(r'\W', ' ', str(comments[sentence]))
            # remove all single characters
            being_processed= re.sub(r'\s+[a-zA-Z]\s+', ' ', being_processed)
            # Remove single characters from the start
            being_processed = re.sub(r'\^[a-zA-Z]\s+', ' ', being_processed) 
            # Substituting multiple spaces with single space
            being_processed = re.sub(r'\s+', ' ', being_processed, flags=re.I)
            # Removing prefixed 'b'
            being_processed = re.sub(r'^b\s+', '', being_processed)
            # Converting to Lowercase
            being_processed = being_processed.lower()
            processed_comments.append(being_processed)
        else:
            processed_comments.append("empty")
    X_predict = vectorize.transform(processed_comments).toarray()
    Y_predict=model.predict(X_predict)
    # I want this Y_predict to return a list of 0,4
    # 0 -> 
    # 4 -> 
    return Y_predict