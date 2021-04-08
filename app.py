import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [float(k) for k in request.form.values()]

    pre_features = [np.array(int_features)]
    y = np.round(np.reciprocal(pre_features),4)
    tlp = np.array(np.sum(y))
    n = np.round(10**y,2)
    m = [np.array(np.insert(n,3,tlp))]

    prediction = model.predict(m)

    return render_template('index.html', prediction_text='Expected winner of match is  {}'.format(prediction))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)

    #def modify(data):
        #m = data
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)