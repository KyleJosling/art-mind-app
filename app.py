from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from getColor import colorz
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

#Gets the whole colour pallette and returns it
def getPallette(filename,k):

    #Get art pallette
    artPallette=colorz(filename,k)
    data={

    "model":"default",
    "input":""

    }
    #JSON
    data["input"]=artPallette
    data=json.dumps(data)
    #Get colours from colorminds api
    r=requests.get('http://colormind.io/api/',data=data,timeout=1)
    # print r
    return r

@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/hello')
def index():
   return "Hi"


@app.route('/stuff', methods = ['GET', 'POST'])
def uploader_file():
   if request.method == 'POST':
	   k = request.form['kMeans']
	   f = request.files['file']
	   f.save(secure_filename(f.filename))
	   raw= getPallette(f.filename,int(k))
	   # print raw.text
	   return raw.text

if __name__ == '__main__':
   app.run(debug = True)
