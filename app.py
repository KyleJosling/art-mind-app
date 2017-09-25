from flask import Flask, render_template, request
from werkzeug import secure_filename
from getColor import colorz
import requests
import json


app = Flask(__name__)

def getPallette(filename):

    artPallette=colorz(filename)
    data={

    "model":"default",
    "input":""

    }

    data["input"]=artPallette
    data=json.dumps(data)

    r=requests.get('http://colormind.io/api/',data=data,timeout=1)
    print r
    return r

@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/stuff', methods = ['GET', 'POST'])
def uploader_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      raw= getPallette(f.filename)
      print raw.text
      return raw.text

if __name__ == '__main__':
   app.run(debug = True)
