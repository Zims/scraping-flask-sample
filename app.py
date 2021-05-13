from flask import Flask, render_template, request, Blueprint, jsonify, send_from_directory, make_response
from flask import json
from flask.helpers import send_file
import soup_yp_wo_ads
import remove_files
from functools import wraps
import os
from scrapers.ss_property import scrape_ss, refresh_time
from scrapers.city24_scraper import parse_city24_scraper, refresh_time_24
from scrapers.inch_scraper import parse_inch_scraper, refresh_time_inch

app = Flask(__name__)

UPLOAD_DIRECTORY = "/"
pwd_partial = os.popen('pwd').readline()
pwd = f"{pwd_partial.strip()}/output"

admin = Blueprint('admin', __name__, static_folder='static')


# Auth decorator
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == 'tester' and auth.password == 'infoDUMP00':
            return f(*args, **kwargs)
        return make_response("Could not vertify your login!", 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated


@app.route("/", methods=['GET'])
@auth_required
def index():
    return render_template('index.html')


@app.route("/ss", methods=['GET'])
@auth_required
def ss_page():
    # return render_template('/index.html')
    return render_template('ss_input.html')


@app.route('/city24')
@auth_required
def c24():
    return render_template('city24_input.html')\


@app.route('/inch')
@auth_required
def inch_home():
    return render_template('inch_input.html')


@app.route("/parse_city24")
@auth_required
def parse_city24():
    parse_city24_scraper()
    return render_template("/ss_parsed.html")

@app.route("/parse_inch")
@auth_required
def parse_inch():
    parse_inch_scraper()
    return render_template("/ss_parsed.html")
# @app.route('/parse_ss')
# def parse_ss():
#    scrape_ss()
#    return render_template('/ss_parsed.html', file_name=ss_filename)

# working but something is wrong

@app.route('/parse_ss', methods=['POST', 'GET'])
@auth_required
def parse_ss():
    if request.method == 'POST':
        result = request.form
        # how to parse the flask dict:
        # https://stackoverflow.com/questions/23205577/python-flask-immutablemultidict
        chosen_region = request.form.getlist('Name')
        # file_name_chosen = request.form.getlist('Filename')
        scrape_ss(chosen_region)
        return render_template('/ss_parsed.html', file_name=refresh_time())


#  I can browse the folder now
@app.route('/output', defaults={'req_path': ''})
@app.route('/<path:req_path>')
@auth_required
def dir_listing(req_path):
    BASE_DIR = pwd
    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)
    # Show directory contents
    files = os.listdir(abs_path)
    print(files)
    return render_template('files.html', files=files, pwd=pwd)


@app.route('/input')
@auth_required
def input():
    return render_template('input.html')


@app.route('/result', methods=['POST', 'GET'])
@auth_required
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
@auth_required
def otput_folder(json_name):
    return send_from_directory('./output', f'{json_name}')


if __name__ == '__main__':
    app.run(debug=True)
