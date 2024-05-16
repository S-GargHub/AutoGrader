import os
import re
import json
import boto3

from flask_session import Session
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from src.autograder import AutoGrader
from src.utils import parse_problem_file
from src.awsServices import *
import hmac
import hashlib
import base64

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'py'}


def calculate_secret_hash(client_id, client_secret, username):
    message = username + client_id
    dig = hmac.new(str(client_secret).encode('utf-8'), 
                   msg = str(message).encode('utf-8'), 
                   digestmod = hashlib.sha256).digest()
    secret_hash = base64.b64encode(dig).decode()
    return secret_hash

@app.route("/", methods=["GET"])
def welcome():
    return render_template("welcome.html")

@app.route("/login", methods=['POST'])
def login():
    # Get username and password from request
    email = request.form['email']
    password = request.form['password']

    try:
        # Check if the user's email is from @sjsu.edu domain
        if email and re.match(r'.+@sjsu\.edu$', email):
            client = boto3.client('cognito-idp')
            # Authenticate user using AWS Cognito
            response = client.initiate_auth(
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password
                },
                ClientId=os.environ.get('CLIENT_ID')
            )
            print("Access granted to Auto Grader")
            session['logged_in'] = True
            session['user_email'] = email
            return redirect(url_for('problem'))
        else:
            return render_template('welcome.html', error="Access denied: User's email is not from @sjsu.edu domain")
    except client.exceptions.NotAuthorizedException:
        return render_template('welcome.html', error="Invalid username or password")
    except Exception as e:
        return render_template('welcome.html', error=f"Error: {str(e)}")
    

@app.route('/logout', methods=["POST"])
def logout():
    session['logged_in'] = False
    session.pop('user_email', None)
    return redirect(url_for('welcome'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/problem", methods=["GET", "POST"])
def problem():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    student_id = session.get('user_email') 
    if not student_id:
        return jsonify({'message': 'Authentication required'})
    problemNumber = str(2)

    problem = ""
    problem_name, problem, test_cases = parse_problem_file('data/' + problemNumber + '/problemStatement.txt')
    with open('data/' + problemNumber + '/solution.txt', 'r') as file:
        solution_file = file.read()
    if request.method == "POST":

        # Check if the solution is provided by uploading a file
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            if allowed_file(file.filename):
                student_solution = file.read().decode("utf-8")
            else:
                return jsonify({"error_message": "Please upload a .py file"})
        
        # Check if the solution is provided through the text window
        elif 'solution' in request.form:
            student_solution = request.form['solution']
        else:
            return jsonify({"error_message": "No solution provided"})

        auto_grader = AutoGrader(problem, 'data/' + problemNumber + '/testCases.txt')
        test_cases_pass, error, test_results = auto_grader.grade_solution(student_solution)
        grade = auto_grader.get_grade()
        if check_exist_student_id(student_id):
            update_score(student_id, grade)
        else:
            add_score_dynamodb(student_id, str(grade)+'%')
        return jsonify({
            "passCount": test_cases_pass,
            "total": len(auto_grader.test_cases),
            "error_message": error,
            "grade": grade,
            "test_results": test_results,
        })
    else:
        return render_template("problemDescription.html", problem_name=problem_name, problem=problem, test_cases=test_cases, solution=solution_file)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
