1. How to setup environment and run the application

  Create a virtual environment:
    python3 -m venv env

  Install requirements:
    pip install -r requirements.txt

  Instructions to run the application through Command Line locally:

    1. export FLASK_APP=app.py
    2. export FLASK_ENV=development
    3. flask run

2. Link to the hosted application in AWS:

  http://35.182.166.1/
  (Flask Application is served using Nginx and Gunicorn)

3. REST API endpoints:
  http://35.182.166.1/users
  http://35.182.166.1/users/<int: user_id>
  
  examples:
  
  To get all users:
  curl http://35.182.166.1/users
  
  To get specified user:
  curl http://35.182.166.1/users/1
  
  To post user:
  curl http://35.182.166.1/users \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"name":"abc", "age":"15", "address":"Canada"}'
    
  To delete user:
  curl http://35.182.166.1/users/2 -X -DELETE -I

