from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/submit', methods=['POST'])
def submit():
    answers = request.json.get('answers')
    response = requests.post('http://localhost:8000/analyze', json={'answers': answers})
    career = response.json().get('career')
    return {'career': career}

@app.route('/result')
def result():
    career = request.args.get('career')
    return render_template('result.html', career=career)

if __name__ == '__main__':
    app.run(debug=True)
