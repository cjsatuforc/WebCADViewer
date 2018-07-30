# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 23:41:31 2018
@author: Hualin Xiao, dr.hualin.xiao@gmail.com
"""



from flask import Flask, render_template, request, session, abort, redirect,flash,Response,url_for,abort,json,send_from_directory
from werkzeug.utils import secure_filename
import core.ConfigParser as conf
from core.CadParser import CadParser
import os

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = conf.max_content_length()
CAD_FILE_EXTENSIONS=set(['stp','step','STEP','STP','iv','iges','igs',
    'FCstd','obj','ply','vrml','dae','poly',
    'brep','brp','stl','fcstd'])


@app.route("/")
def main():
    return render_template('index.html',view=False, fid='')




@app.route('/document/<fuuid>')
def get_stat(fuuid):
    js="{'status':'error'}"
    try:
        server_filename=os.path.join(conf.project_directory(), '{}/stat.json'.format(fuuid))
        with open(server_filename) as f:
            #js=json.load(f)
            js=f.read()
            print type(js)
    except:
        pass
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@app.route('/view/<fuuid>')
def view(fuuid):
    return render_template('index.html',view=True, fid=fuuid)

    

@app.route('/document/<fuuid>/<puuid>')
def load_data(fuuid,puuid):
    js="{'status':'error'}"
    try:
        server_filename=os.path.join(conf.project_directory(), '{}/{}.json'.format(fuuid,puuid))
        with open(server_filename) as f:
            #js=json.load(f)
            js=f.read()
            print type(js)
    except:
        pass
    resp = Response(js, status=200, mimetype='application/json')
    return resp





def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in CAD_FILE_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            server_filename=os.path.join(conf.project_directory(), filename)
            file.save(server_filename)
            print('process step file:%s'%server_filename)
            cp=CadParser()
            js=cp.importCAD(server_filename)
            resp = Response(js, status=200, mimetype='application/json')
            return resp
            
    #return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True,port='80',host='0.0.0.0')

