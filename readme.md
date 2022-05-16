# Lauch app with local flask backend
## Set up flask backend
### Do the following steps if you don't have flask installed
1. Create py venv
2. `pip install flask`
3. `pip install flask_wtf`
### Run `flask run` if already have flask installed
Check if endpoints are up in http://localhost:5000/

## Lauch app
1. Run `cd frontend` to enter frontend code folder
2. Run 'npm install'
3. Run 'npm start'

# Deploy with HEROKU
1. pip install gunicorn
2. pip install freeze > requirements.txt #create req.txt
3. touch Procfile
4. test
