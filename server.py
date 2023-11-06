# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 01:29:39 2020

@author: nitin
"""

from flask import Flask, request,jsonify
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from t1 import get_transcript
from demo02_diarization import getvoicearr



app = Flask(__name__)
api = Api(app)

CORS(app)

@app.route("/")
def hello():
    return jsonify({'text':'Hello World!'})

@app.route("/speak")
def speak():
    transcript = []
    speaker = []
    dict={}
    transcript = get_transcript()
    speaker = getvoicearr()

    for i in range(len(speaker)):
        key = str(i)+speaker[i]
        value = transcript[i]
        dict[key]=value

    
    f = open("dict.txt","w")
    f.write( str(dict) )
    f.close()
    return jsonify({'result':'sucess'})

 





if __name__ == '__main__':
   app.run(port=5002)