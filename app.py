from flask import Flask, render_template, request, Blueprint, jsonify, send_from_directory
from flask import json
from flask.helpers import send_file
import soup_yp_wo_ads
import remove_files
import os

app = Flask(__name__)

UPLOAD_DIRECTORY = "/"

# f = open("roofer.json", "r")
# data = f.read()
admin = Blueprint('admin', __name__, static_folder='static')


@app.route("/", methods=['GET'])
def index():
    return render_template('/index.html')


@app.route('/input')
def input():
   return render_template('input.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
         # return render_template("result.html",result = result)
   if request.method == 'POST':
      result = request.form
    # how to parse the flask dict:
    # https://stackoverflow.com/questions/23205577/python-flask-immutablemultidict
      the_url = request.form.getlist('Name')
      file_name_chosen = request.form.getlist('Filename')
      if 'yellowpages' in request.form['Name']:
         remove_files.cleanup()
         soup_yp_wo_ads.output_file(the_url[0], file_name_chosen[0])
         return render_template("result.html",result = result, json_name = soup_yp_wo_ads.json_name)
      else:
         return render_template('error.html')

@app.route('/output/<json_name>', methods=['POST', 'GET'])
def otput_folder(json_name):
   return send_from_directory('./output', f'{json_name}')


if __name__ == '__main__':
   app.run()

