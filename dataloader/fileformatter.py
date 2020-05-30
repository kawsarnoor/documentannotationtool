import numpy as np
import pandas as pd
import re, json
import nltk

def getspans(category,index):
    
    spans = re.findall(r'\[(.*?)\]', category[index])
    return spans

def getlabels(category, index):
    sentence = category[index]
    pattern = r'\[.*?\]'
    labels_raw = re.sub(pattern, '', sentence)
    labels = labels_raw.split('\n')
    labels = [l.rstrip() for l in labels]
    return labels

def retrievecategorylabels(category):
    final_labels = []
    for i in range(len(category)):
        if pd.isnull(category[i]):
            final_labels.append([])
        else:
            final_labels.append(getlabels(category,i))
            
    return final_labels


def convertDataframeToDictionary(df, categories):

    renamed_df = df.rename(columns={"Unnamed: 0" : "id",
                     "IN07 Description of what happened": "whathappened", 
                     "IN10 Actions Preventing Reoccurrence": "actionspreventing",
                    "stage of care": "stageofcare",
                    "error": "error",
                    "known allergy": "knownallergy",
                    "certainty or severity of allergy": "certaintyallergy",
                    "themes of causes and contributory factors": "themes"})

    renamed_df['whathappened'] = renamed_df['whathappened'].replace(np.nan, '', regex=True)
    renamed_df['actionspreventing'] = renamed_df['actionspreventing'].replace(np.nan, '', regex=True)

    categorylabels = [retrievecategorylabels(list(renamed_df[category])) for category in categories]
    unique_labels = []
    for cl in categorylabels:
        unique_items = list(set([item for sublist in cl for item in sublist]))
        unique_labels.append(unique_items)

    converted_docs = []
    span_docs = []
    for doc_no in range(renamed_df.shape[0]):
        ul_dictionary = {}
        ul_dictionary['id'] = doc_no
        ul_dictionary['whathappened'] = nltk.word_tokenize(renamed_df['whathappened'][doc_no])
        ul_dictionary['actionspreventing'] = nltk.word_tokenize(renamed_df['actionspreventing'][doc_no])

        ul_dictionary['whathappened'] = [word + ' ' for word in ul_dictionary['whathappened']]
        ul_dictionary['actionspreventing'] = [word + ' ' for word in ul_dictionary['actionspreventing']]

        span_dictionary = {}
        for j, ul in enumerate(unique_labels):
            for label in ul:
                if categories[j] not in ul_dictionary.keys():
                    ul_dictionary[categories[j]] = {}
                    span_dictionary[categories[j]] = {}
                if label in categorylabels[j][doc_no]:
                    ul_dictionary[categories[j]][label] = True
                else:
                    ul_dictionary[categories[j]][label] = False
                
                span_dictionary[categories[j]][label] = []

        converted_docs.append(ul_dictionary)
        span_docs.append(span_dictionary)
    
    return converted_docs, span_docs

categories = ['stageofcare', 'error','knownallergy', 'certaintyallergy', 'themes']
df = pd.read_csv('/Users/kawsarnoor/Desktop/cogstack/projects/allergies/annotationTool/dataloader/temp_2.csv')
converted_docs, span_docs = convertDataframeToDictionary(df, categories)

with open('data.json','w') as fp:
    json.dump(converted_docs, fp)

with open('spandata.json', 'w') as fp:
    json.dump(span_docs, fp)

print('succesfully loaded annotations from excel')