from flask import Flask, render_template, request
import os 
import numpy as np
import pandas as pd
from WineX.pipeline.prediction import PredictionPipeline
from WineX.utils.DataHandler import DataHandler
import json

app = Flask(__name__) # initializing a flask app



# Route 1 : main route of the flask application

@app.route('/',methods=['GET'])  # route to display the home page
def homePage():
    return render_template("index.html")

# Route 2 : for the training of the model

@app.route('/train',methods=['GET'])  # route to train the pipeline
def training():
    os.system("python main.py")
    with open('artifacts/model_evaluation/metrics.json', 'r') as file:
        metrics_data = json.load(file)

    return render_template('index.html',**metrics_data)


# Route 3 : for the prediction of the model

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
def index():
    if request.method == 'POST':

            #  reading the inputs given by the user
            fixed_acidity =float(request.form['fixed_acidity'])
            volatile_acidity =float(request.form['volatile_acidity'])
            citric_acid =float(request.form['citric_acid'])
            residual_sugar =float(request.form['residual_sugar'])
            chlorides =float(request.form['chlorides'])
            free_sulfur_dioxide =float(request.form['free_sulfur_dioxide'])
            total_sulfur_dioxide =float(request.form['total_sulfur_dioxide'])
            density =float(request.form['density'])
            pH =float(request.form['pH'])
            sulphates =float(request.form['sulphates'])
            alcohol =float(request.form['alcohol'])
       
         
            data = [fixed_acidity,volatile_acidity,citric_acid,residual_sugar,chlorides,free_sulfur_dioxide,total_sulfur_dioxide,density,pH,sulphates,alcohol]
            data = np.array(data).reshape(1, 11)
            
            obj = PredictionPipeline()
            predict = obj.predict(data)
            with open('artifacts/model_evaluation/metrics.json', 'r') as file:
                metrics_data = json.load(file)


            return render_template('index.html', prediction = str(predict),**metrics_data)


    else:
        return render_template('index.html')


# Route 4 : for the feedback of the model

data_handler = DataHandler()

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    name = request.form.get('name')
    email = request.form.get('email')
    feedback = request.form.get('comments')
    satisfied = request.form.get('satisfied')
    data_handler.add_feedback(name, email,feedback,satisfied)
    return render_template('index.html')

if __name__ == "__main__":
	# app.run(host="0.0.0.0", port = 8080, debug=True)
	app.run(host="0.0.0.0", port = 8080)