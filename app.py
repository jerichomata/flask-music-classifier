

from flask import Flask, redirect, url_for, render_template, request, session, flash, send_file
from datetime import timedelta
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask import Flask, redirect, url_for, render_template, request, session, flash, send_file
from datetime import timedelta
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os 

#Configuration stuff
app = Flask(__name__)

#File path to put uploaded file
app.config['UPLOAD_FOLDER'] = 'static/files'

#Secret key thats needed for some reason
app.config['SECRET_KEY'] = 'bobross'
app.secret_key = "bobross"

#Only delete webpage data after 5 days
app.permanent_session_lifetime = timedelta(days=5)


def model():

    return 0

#Home page of website
@app.route("/", methods=['GET', "POST"])
def home():
    if request.method == 'POST':
        
        #Check if we press the "GetGenre button"
        if request.form.get("GetGenre") == "GENRE":
            #Call model
            model()
            return redirect(url_for("home")) 
        
        #Function that checks if we uploaded files        
        elif request.files.getlist('files'):
            
            #Retreives file(s) and puts them at specified location
            for f in request.files.getlist('files'):
                if f.filename:
                    f.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
                else:
                    return render_template("home.html")
        
        #If not button pressed, load home page again
        else:
            return render_template("home.html")
    return render_template("home.html")
    
    
#For Downloading a file
@app.route('/download')
def download_file():
    p = "prediction.csv"
    return send_file(p, as_attachment=True)


if __name__ == '__main__':
    #Allows for live debugging and updating
    app.run(debug=True)
    