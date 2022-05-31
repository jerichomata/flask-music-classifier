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

#Class to store prediction
class Concurrency:
    prediction = "Upload Audio File"

# Home page of website
@app.route("/home", methods=['GET', "POST"])
def home():
    
    # Function that checks if we uploaded files        
    if request.method == 'POST':
        #request.files['file']
        f = request.files['file']

        #Code to try and work with MP3
        #Save the file to local storage and pass the path to the librosa.load()
        #For some reason not looking in right directory right now -----------------
        #f.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        #print('flask-music-classifier/static/files/' + f.filename)
        #prediction = get_prediction('flask-music-classifier/static/files/' + f.filename)
        #-----------------------------------

        #Call function to get prediction
        prediction = get_prediction(f)
        print("prediction", prediction)
        print("filename: ", f.filename)

        Concurrency.prediction = prediction[2:-2]
        return {'text': prediction}
    
    else:

        return {'text': Concurrency.prediction}

if __name__ == '__main__':
    # Allows for live debugging and updating
    app.run(debug=True)
    output = "first output2"