# mongo_euro_teams_2016.py

import csv
import json
import os
import pandas as pd
import sys
from pymongo import MongoClient

def import_content():
	mongo_client = MongoClient('mongodb://mongodb3.isaalab.net', 27017)
	mongo_database = mongo_client['Euro_Soccer']
	mongo_collection = 'pastebins'
	database_command = mongo_database[mongo_collection]

	cDirectory = os.path.dirname(__file__)
	fetch_file = os.path.join(cDirectory, 'C:\Code\Files\Euro_Teams_Info.csv')

	data = pd.read_csv(fetch_file)
	json_content = json.loads(data.to_json(orient='records'))

	database_command.remove()
	database_command.insert(json_content)
	
import_content()
	


