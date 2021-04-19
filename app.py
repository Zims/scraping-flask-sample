from flask import Flask, render_template, request, Blueprint, jsonify, send_from_directory
from flask import json
from flask.helpers import send_file
import soup_yp_wo_ads
import remove_files
import os
from scrapers.ss_property import scrape_ss, refresh_time
# from scrapers.ss_rajonchiks import scrape_ss, ss_filename

app = Flask(__name__)

UPLOAD_DIRECTORY = "/"

# f = open("roofer.json", "r")
# data = f.read()
admin = Blueprint('admin', __name__, static_folder='static')


@app.route("/", methods=['GET'])
def index():
    # return render_template('/index.html')
    return render_template('ss_input.html')


@app.route('/ss')
def ss():
    return render_template('ss_input.html')


# @app.route('/parse_ss')
# def parse_ss():
#    scrape_ss()
#    return render_template('/ss_parsed.html', file_name=ss_filename)

# working but something is wrong

@app.route('/parse_ss', methods=['POST', 'GET'])
def parse_ss():
    if request.method == 'POST':
        result = request.form
    # how to parse the flask dict:
    # https://stackoverflow.com/questions/23205577/python-flask-immutablemultidict
        chosen_region = request.form.getlist('Name')
        # file_name_chosen = request.form.getlist('Filename')
        scrape_ss(chosen_region)
        return render_template('/ss_parsed.html', file_name=refresh_time())

@app.route('/output')
def make_tree():
    # for f in os.listdir("/Users/zims/Documents/Python/2021/scraping_flask_sample/output/"):
    #     print(f)
    # content = os.listdir("/Users/zims/Documents/Python/2021/scraping_flask_sample/output/")
    # return render_template("output.html", content=content) 
    return render_template('output.html')


@app.route('/input')
def input():
    return render_template('input.html')


@app.route('/result', methods=['POST', 'GET'])
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
            return render_template("result.html", result=result, json_name=soup_yp_wo_ads.json_name)
        else:
            return render_template('error.html')


@app.route('/output/<json_name>', methods=['POST', 'GET'])
def otput_folder(json_name):
    return send_from_directory('./output', f'{json_name}')


if __name__ == '__main__':
    app.run()
