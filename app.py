from flask import Flask, jsonify, request, json
from flask_cors import CORS
import nltk, csv
from random import sample 
import os.path
from dataloader import fileformatter

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

if not os.path.exists('data.json'):
    fileformatter.run()

# Load all data at runtime
with open('data.json') as json_file:
    LABELS = json.load(json_file)

with open('spandata.json') as json_file:
    SPANS = json.load(json_file)

with open('completed.csv') as csvfile:
    COMPLETED = [int(item) for item in list(csv.reader(csvfile,delimiter=','))[0]]


def saveProgress():

    with open('data.json','w') as fp:
        json.dump(LABELS, fp)

    with open('spandata.json', 'w') as fp:
        json.dump(SPANS, fp)

    with open('completed.csv','w') as fp:
        wr = csv.writer(fp, quoting=csv.QUOTE_ALL)
        wr.writerow(COMPLETED)


def getspanvalueslist(idx):
    span_values = []
    for key in SPANS[COMPLETED[idx]].keys():
        if key != 'id':
            for value in SPANS[COMPLETED[idx]][key].values():
                span_values.extend(value)

    return span_values

@app.route('/getnextdocument', methods=['GET'])
def getnextdocument():
    # Here we implement active learning
    return jsonify({
        'status': 'success',
        'labels': LABELS[COMPLETED[-1]],
        'spans': SPANS[COMPLETED[-1]],
        'span_values': getspanvalueslist(-1)
    })

@app.route('/getpreviousdocument', methods=['GET'])
def getpreviousdocument():
    return jsonify({
        'status': 'success',
        'labels': LABELS[COMPLETED[-1]]
    })

@app.route('/updateSpans', methods=['POST'])
def updateSpans():
    response_object = {'status': 'success'}
    req_data = request.get_json()
    spans = req_data['newspans']
    category = req_data['category']
    label = req_data['label']     
    id = req_data['id'] 
    combinedspans = list(set(spans + SPANS[id][category][label]))  
    SPANS[id][category][label] = combinedspans

    saveProgress()
    return response_object

@app.route('/changelabel', methods=['POST'])
def changelabel():
    response_object = {'status': 'success'}
    req_data = request.get_json()
    category = req_data['category']
    label = req_data['label']
    id = req_data['id']   
    LABELS[id][category][label] = not LABELS[id][category][label]
    SPANS[id][category][label] = []

    saveProgress()
    return response_object

@app.route('/addlabel', methods=['POST'])
def addlabel():
    response_object = {'status': 'success'}
    req_data = request.get_json()
    newlabel = req_data['newlabel']
    category = req_data['category']

    for idx, span in enumerate(SPANS):
        span[category][newlabel] = []
        LABELS[idx][category][newlabel] = False

    saveProgress()

    return response_object

@app.route('/changecurrentid', methods=['POST'])
def changecurrentid():
    response_object = {'status': 'success'}
    req_data = request.get_json()
    new_id = int(req_data['newid'])
    COMPLETED.append(new_id)
    return response_object

@app.route('/getCurrentId', methods=['GET'])
def getcurrentid():
    return jsonify({
        'status': 'success',
        'currentid': COMPLETED[-1]
    })    

@app.route('/getHistory', methods=['GET'])
def gethistory():
    print('returning history')
    return jsonify({
        'status': 'success',
        'history': COMPLETED
    })  

@app.route('/getDocumentviaIndex', methods=['POST'])
def getdocumentviaindex():
    print('returning document using idx')
    req_data = request.get_json()
    req_idx = int(req_data['newIdx'])

    return jsonify({
        'status': 'success',
        'labels': LABELS[COMPLETED[req_idx]],
        'spans': SPANS[COMPLETED[req_idx]],
        'span_values': getspanvalueslist(req_idx)
    })

@app.route('/sampleNewDocument', methods=['GET'])
def samplenewdocument():
    all_documents= set(list(range(len(LABELS))))
    incomplete = list(all_documents.difference(set(COMPLETED)))

    #random sampling one atm
    sampled_id = sample(incomplete,1)[0]
    COMPLETED.append(sampled_id)
    saveProgress()
    
    return jsonify({
        'status': 'success'
    })  

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0' ,port='5001')