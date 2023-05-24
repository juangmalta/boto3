# !pip install flask

from flask import Flask
import json 
import requests

import boto3
from dotenv import dotenv_values
config = dotenv_values(".env")

bucket_name = 'chumbucket22blueleg'
client = boto3.client('s3', aws_access_key_id=config['AWS_ACCESS_KEY_ID'],
                      aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'],
                      region_name=config['REGION_NAME'])
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'


@app.route("/get_data")
def getdata():
    data = {
        'key1' : 'value 1',
        'key2' : 'value 2'
    }
    return json.dumps(data)

@app.route("/rick")
def rick():
    resp = requests.get('https://rickandmortyapi.com/api/character')

    return resp.json()

@app.route("/create")
def create():
    file_name = "Book1.csv"
    file_path = "data/" + file_name
    with open(file_path, "rb") as f:
        client.put_object(Bucket=bucket_name, Key=file_name, Body=f)
    data = {
        'status' : 'success'
    }
    return json.dumps(data)


@app.route("/delete")
def delete():
    s3 = boto3.resource('s3')
    s3.Object(bucket_name, 'Book1.csv').delete()
    data = {
        'status' : 'success'
    }
    return json.dumps(data)

@app.route("/read")
def read():
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket_name, Key='Book1.csv')
    data = obj['Body'].read().decode('utf-8')
    return data

@app.route("/update")
def update():
    file_name = "Book1.csv"
    file_path = "data/" + file_name
    with open(file_path, "rb") as f:
        client.put_object(Bucket=bucket_name, Key=file_name, Body=f)
    data = {
        'status' : 'success'
    }
    return json.dumps(data)

app.run(host='0.0.0.0', port=3000)