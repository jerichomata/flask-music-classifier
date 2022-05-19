from extractFeatures import *
from flask import Flask, redirect, url_for, render_template, request, send_file
from datetime import timedelta
from werkzeug.utils import secure_filename
from flask_cors import CORS #comment this on deployment
import os
import io
import pydub

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


def model():

    return 0




# Home page of website
@app.route("/", methods=['GET', "POST"])
def home():
    if request.method == 'POST':
        print(request.files['file'])
        # Check if we press the "GetGenre button"
        if request.form.get("GetGenre") == "GENRE":
            # Call model
            model()
            return redirect(url_for("home")) 
        
        # Function that checks if we uploaded files        
        elif request.files['file']:
            f = request.files['file']
            # Retreives the file and puts it at specified location
            if f.filename:
                
                #Code to potential convert mp3 to .wav
                #wav = io.BytesIO()
                #f.seek() = lambda *args: None
                #pydub.AudioSegment.from_file(f.seek(0)).export(wav, "wav")
                #wav.seek(0)
                #ExtractFeatures(wav)

                #Upload file from reach
                #Re-save this file
                ExtractFeatures(f)

                #To save to local file system
                #f.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
                
                #filename = f.filename
                #ExtractFeatures("/static/files/" + filename)
                #'static/files/extraction_files_1.mp3'

            else:
                return render_template("home.html")
        
        # If not button pressed, load home page again
        else:
            return render_template("home.html")
    return render_template("home.html")
    
    
# For Downloading a file
@app.route('/download')
def download_file():
    p = "prediction.csv"
    return send_file(p, as_attachment=True)


if __name__ == '__main__':
    # Allows for live debugging and updating
    app.run(debug=True)
    