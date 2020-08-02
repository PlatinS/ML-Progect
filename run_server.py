import dill
import pandas as pd
import os
dill._dill._reverse_typemap['ClassType'] = type

from flask import Flask, render_template, jsonify, request
import logging
from logging.handlers import RotatingFileHandler
from time import time, strftime
import re
import string
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()
from prep_def import remove_emoji, clean

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
	result = {"success": False}
	dt = strftime("[%Y-%b-%d %H:%M:%S]")

	json_input = request.json

	current_datatime = strftime('[%Y-%b-%d %H:%M:%S]')
	ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
	logger.info(f'{current_datatime} request from {ip_address}: {request.json}')
	start_prediction = time()

	tweet = json_input['tweet']

	try:
		probs = model.predict_proba(pd.DataFrame(data = {'text': [tweet] }))
	except AttributeError as e:
		logger.warning(f'{dt} Exception: {str(e)}')
		result['predictions'] = str(e)
		result['success'] = False
		return jsonify(result)

	proba = round(probs[:, 1][0], 4)
	if proba > 0.5:
		result['predict'] = "Чрезвычайная ситуация"
	else:
		result['predict'] = "Нет чрезвычайной ситуации"
	result['probability'] = proba
	result['success'] = True

	end_prediction = time()
	duration = round(end_prediction - start_prediction, 6)
	current_datatime = strftime('[%Y-%b-%d %H:%M:%S]')
	logger.info(f'{current_datatime} predicted for {duration} msec: {result}\n')

	return jsonify(result)

if __name__ == '__main__':
	app.run(debug = True)
