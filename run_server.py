from flask import Flask, render_template, jsonify, request
import logging
import traceback
from logging.handlers import RotatingFileHandler
from time import time, strftime
import os
import dill

dill._dill._reverse_typemap['ClassType'] = type

app = Flask(__name__)

model = None

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def load_model(model_path):
	# load the pre-trained model
	global model
	with open(model_path, 'rb') as f:
		model = dill.load(f)

modelpath = "./models/model_nlp.dill"
load_model(modelpath)

@app.route("/")
def index():
	return "API for predict service"

@app.route("/predict", methods=['POST'])
def predict():
	json_input = request.json

	current_datatime = strftime('[%Y-%b-%d %H:%M:%S]')
	ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
	logger.info(f'{current_datatime} request from {ip_address}: {request.json}')
	start_prediction = time()

	tweet = json_input['tweet']

	result = {
        'ID': tweet,
        'value_Poisson': 1,
        'value_Gamma': 2,
        'value_BurningCost': 'Yesss!'
    }

	end_prediction = time()
	duration = round(end_prediction - start_prediction, 6)
	current_datatime = strftime('[%Y-%b-%d %H:%M:%S]')
	logger.info(f'{current_datatime} predicted for {duration} msec: {result}\n')

	return jsonify(result)

if __name__ == '__main__':
	app.run(debug = True)
