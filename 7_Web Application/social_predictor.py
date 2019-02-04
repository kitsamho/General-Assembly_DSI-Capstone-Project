
import pickle
import flask
from flask import render_template
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import regex as re
from functools import reduce
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as esw
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import VotingClassifier
from sklearn import metrics
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
import pickle
from time import time
import io


def nohash(x):
    return re.sub(r'#\S+', '',x)
def nohttp(x):
    return re.sub(r'http\S+', '',x)
def nobitly(x):
    return re.sub(r'bit.ly\S+', '',x)
def nolink(x):
    return re.sub(r'\b\w*[/.]\w*\b','',x)
def cleaner(x):
    return nohash(nohttp(nobitly(nolink(x))))

brand_cues =  ['\n','Terms:' ,'See More', 'store','stores',
             'Sainsburys',"Sainsbury’s",'sainsburys',"sainsbury’s",'sainsbury','Sainsbury','nectar','Nectar','Good Living','Tu','tu',
             'Tesco','tesco',"Tesco's",'clubcard','Clubcard','Tesco Extra','Jamie','Jamie Oliver',
             'Waitrose','waitrose','heston','Heston',
             'Lidl','LidlUk','lidl',"lidl's",'lidluk',
             'Heidi','heidi','klum','Klum',
             'Morrisons','morrisons','msstorefinder','nutmeg','Nutmeg',
             'ASDA','asda','Asda','bestchristmasever','George',
             'M&S','MnS','Marks & Spencer','Marks&Spencer','marks and spencer','marksandspencer','marks&spencer']

#Function that removes any obvious branding cues (above) from the post content i.e. brand names, celebrities
def debrander(x):
    x = re.sub(r'[,.!]',' ',x).split()
    for word in x:
        if word in brand_cues:
            x.remove(word)
    x = [' {} '.format(elem) for elem in x]
    return ''.join(x)

stopWords = set(list(esw)).union(set(brand_cues))

class preproc(BaseEstimator, TransformerMixin):
    def __init__(self, cleaner=None,debrander=None,columns_to_drop=None,):
        self.cleaner = cleaner
        self.debrander = debrander
        self.columns_to_drop = columns_to_drop

    #function as outlined above
    def _cleaner(self, X):
        try:
            for col in self.cleaner:
                try:
                    subset = X.loc[:,col]
                    subset = subset.apply(cleaner)
                    X[col] = subset
                except:
                    pass
        except:
            pass
        return X

    #function as outlined above
    def _debrander(self, X):
        try:
            for col in self.debrander:
                try:
                    subset = X.loc[:,col]
                    subset = subset.apply(debrander)
                    X[col] = subset
                except:
                    pass
        except:
            pass
        return X

    #drops any unwanted columns
    def _drop_unused_cols(self, X):
        for col in self.columns_to_drop:
            try:
                X = X.drop(col, axis=1)
            except:
                pass
        return X

    def transform(self, X, *args):
        X = self._cleaner(X)
        X = self._debrander(X)
        X = self._drop_unused_cols(X)
        return X

    def fit(self, X,*args):
        return self

data = pd.read_csv('./data/data.csv')

X = data['Post_Content']

y = data['Brand']

y.replace({'Sainsburys': 0, 'Tesco': 1, 'Waitrose': 2,
                'Lidl': 3,'Marks and Spencer' : 4,'Morrisons' : 5,'ASDA': 6},inplace = True)

clf1 = LogisticRegression(penalty='l2', solver = 'liblinear', C=10.717048298967093,random_state=100)
clf2 = KNeighborsClassifier(algorithm='ball_tree', leaf_size = 30, metric= 'minkowski', n_neighbors = 19, p= 2, weights= 'uniform')
clf3 = RandomForestClassifier(bootstrap = True,criterion= 'gini', max_depth = 200,
                              min_samples_leaf = 3, min_samples_split = 2, n_estimators = 300, random_state=100)

m = Pipeline([
    ('content_prep', preproc(cleaner=['Post_Content'],
                                         debrander=['Post_Content'],
                                         columns_to_drop=['Date','Year','All_Responses', 'Comments', 'Shares', 'Views', 'Contains_Link', 'Contains_Video', 'Has_Hashtag', 'Hashtag_Count', 'Likes', 'Response_Rate', 'Comments_Rate', 'Shares_Rate', 'Video_Rate'])),
    ('tfidf_vec', TfidfVectorizer(stop_words=stopWords,
                                  sublinear_tf=True,
                                  max_df=0.25)),
    ('VC', VotingClassifier(estimators=[('lr', clf1), ('knn', clf2), ('rf', clf3)],
                            voting='soft'))
])

m.fit(X,y)

app = flask.Flask(__name__)
app._static_folder = '/Users/sam/Google Drive/DSI/DSI7 - Capstone Working Folder/9_Web Application/static/'

@app.route('/')
@app.route('/page')
def page():
    return render_template('page.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    '''Gets prediction using the HTML form'''
    if flask.request.method == 'POST':
        inputs = flask.request.form
        content = inputs['content']

        y_labels = ["Sainsbury's",'Tesco','Waitrose','Lidl','M&S','Morrisons','ASDA']
        prob_frame = pd.DataFrame({'Predicted_Probability' : m.predict_proba([content]).tolist()[0]},index=y_labels)
        colours = ['#ED8B01','#EE1C2E','#7BB135','#015AA2','#00110A','#ffe900','#00FF00']
        fig, ax = plt.subplots(figsize=(25,8))
        b = sns.barplot(x=prob_frame.index,y=prob_frame.Predicted_Probability,palette=colours)
        b.axes.set_title(content,fontsize=20)
        b.set_xlabel("Brand",fontsize=20)
        b.set_ylabel("Predicted Probability",fontsize=20)
        b.tick_params(labelsize=20)
        image = io.BytesIO()
        plt.savefig(image)

        return image.getvalue(), 200, {'Content-Type': 'image/png'}

if __name__ == '__main__':
    '''Connects to the server'''

    HOST = '127.0.0.1'
    PORT = 5000

    app.run(HOST, PORT)
