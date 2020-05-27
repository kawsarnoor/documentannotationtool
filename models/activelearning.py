from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
from gensim.models import KeyedVectors
import nltk
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
import json 

def cleanwords(words):
    return [word.lower() for word in words]

# Average Embeddings for Documents:
def averageEmbeddings(model, text):
    words = nltk.word_tokenize(text)
    words = cleanwords(words)
    
    vectors = []
    for word in words:
        try:
            vectors.append(model.get_vector(word))
        except:
            continue
    
    average = np.mean(vectors, axis=0)
    return average

def constructEmbeddingsDocument(model, texts):
    return [averageEmbeddings(model, text) for text in texts]


def getUncertaintySum(predictions, X_test):
    uncertainties = []
    for key,item in predictions.items():
        if item == []:
            uncertainties.append([0]*X_test.shape[0])
        else:
            uncertainties.append(np.min(item,axis=1))

    return np.sum(np.array(uncertainties),axis=0)

def labelUncertaintities(labels_df, label, X, completed):
    
    category_df = pd.DataFrame(list(labels_df[label])).astype(int)
    
    X = pd.DataFrame(X)
    X_train = X.iloc[completed]
    X_test = X[~X.index.isin(completed)]
    
    Y_train = category_df.iloc[completed]
    
    pipeline = Pipeline([
                ('clf', OneVsRestClassifier(LogisticRegression(solver='sag'), n_jobs=1)),
            ])
    
    categories = list(Y_train.columns)

    predictions = {}
    for category in categories:
        pipeline.fit(X_train, Y_train[category])
        try:
            prediction_probabilities = pipeline.predict_proba(X_test)
        except:
            prediction_probabilities = []
        predictions[category] = prediction_probabilities
      
    uncertainties = getUncertaintySum(predictions, X_test)
    return uncertainties

def getSample():
    filename = '/Users/kawsarnoor/Desktop/cogstack/projects/allergies/BioWordVec_PubMed_MIMICIII_d200.vec.bin'
    print('start loading model')
    model = KeyedVectors.load_word2vec_format(filename, binary=True)
    print('model loaded succesfully')

    temp = pd.read_csv('temp.csv')
    renamed_df = temp.rename(columns={"Unnamed: 0" : "id",
                        "IN07 Description of what happened": "whathappened", 
                        "IN10 Actions Preventing Reoccurrence": "actionspreventing",
                        "stage of care": "stageofcare",
                        "error": "error",
                        "known allergy": "knownallergy",
                        "certainty or severity of allergy": "certaintyallergy",
                        "themes of causes and contributory factors": "themes"})

    renamed_df['whathappened'] = renamed_df['whathappened'].replace(np.nan, '', regex=True)
    renamed_df['actionspreventing'] = renamed_df['actionspreventing'].replace(np.nan, '', regex=True)

    documents_whathappened = list(renamed_df['whathappened'])
    documents_actionspreventing = list(renamed_df["actionspreventing"])

    X_whathappened = constructEmbeddingsDocument(model, documents_whathappened)
    X_actionspreventing = constructEmbeddingsDocument(model, documents_actionspreventing)

    with open('data.json') as json_file:
        data = json.load(json_file)

    labels_df = pd.DataFrame(data)
    labels_df_only = labels_df.drop(['whathappened','actionspreventing','id'], 1)
    labels = list(labels_df_only.columns)

    completed = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
    uncertainties = []
    for label in labels:
        uncertainties.append(labelUncertaintities(labels_df, label, X_whathappened, completed))

    sampled_idx = np.argmax(np.sum(np.array(uncertainties),axis=0))
    X_test = X_whathappened[~X_whathappened.index.isin(completed)]
    return X_test.iloc[sampled_idx].name