# Lauch app with local flask backend
## Set up flask backend
### Do the following steps if you don't have flask installed
1. cd into the "flask-music-classifier" directory on your computer
2. Create py venv
3. `pip install flask`

### Run `flask run` if already have flask installed
Check if endpoints are up in http://localhost:5000/

## Lauch app
1. Run `cd frontend` to enter frontend code folder
2. Run `npm install`
3. Run `npm start`
4. See the web interface at http://localhost:5000/

App is ready to use. It can take a while or a short
time to classify songs. If it takes longer
that a minute the first time you try to run the app,
restart the python and react programs and try again.


It should work after restarting once. No prediction
will be returned the first time you try to classify,
but every subsequent try to classify a song will work,
just not the first.
