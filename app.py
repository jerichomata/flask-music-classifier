from get_prediction import *
from flask import Flask, redirect, url_for, render_template, request, send_file
from datetime import timedelta
from werkzeug.utils import secure_filename
from flask_cors import CORS #comment this on deployment
import os
import io
import pydub
from flask import jsonify
#from app import output

# Configuration stuff
app = Flask(__name__)

# cannot send request to localhost:5000 from localhost:3000 without this line
CORS(app) # comment this on deployment

# File path to put uploaded file
app.config['UPLOAD_FOLDER'] = 'static/files'

# Secret key thats needed for some reason
app.config['SECRET_KEY'] = 'bobross'
app.secret_key = "bobross"

# Only delete webpage data after 5 days
app.permanent_session_lifetime = timedelta(days=5)


class Concurrency:
    output = "Upload Audio File"

# Home page of website
@app.route("/home", methods=['GET', "POST"])
def home():
    
        # Function that checks if we uploaded files        
    if request.method == 'POST':
        #request.files['file']
        f = request.files['file']

        prediction = get_prediction(f)
        print("prediction", prediction)
        print("filename: ", f.filename)

        #Only get index 2 to (2 from the end)
        Concurrency.output = prediction[2:-2]
        return {'text': prediction}
    
    else:

        print("IN LOOP")
        return {'text': Concurrency.output}
    
# For Downloading a file
@app.route('/download')
def download_file():
    p = "prediction.csv"
    return send_file(p, as_attachment=True)


if __name__ == '__main__':
    # Allows for live debugging and updating
    app.run(debug=True)
    output = "first output2"